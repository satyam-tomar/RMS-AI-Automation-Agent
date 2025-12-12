const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const axios = require('axios');
const path = require('path');
const session = require('express-session');
const bcrypt = require('bcryptjs');
const mongoose = require('mongoose');

// Models
const Student = require('./model/student');
const Teacher = require("./model/teacher");
const Complaint = require('./model/complaints');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// MongoDB Connection
mongoose.connect("mongodb://127.0.0.1:27017/complaint_system")
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.log(err));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(session({
    secret: 'complaint-system-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
}));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));

const STATUS = { PENDING: "pending", RESOLVED: "resolved" };
const FLASK_URL = "http://localhost:5000";

const teacherConnections = new Set();
const studentConnections = new Map();


// Middleware
const requireStudentAuth = (req, res, next) =>
    req.session.studentId ? next() : res.redirect("/login");

const requireTeacherAuth = (req, res, next) =>
    req.session.teacherId ? next() : res.redirect("/login");


// Routes
app.get('/', (req, res) => res.render('home'));

app.get('/login', (req, res) => res.render('index'));

app.post("/login", async (req, res) => {
    const { role } = req.body;

    if (role.toLowerCase() === "student") {
        const { user_id, password } = req.body;

        const student = await Student.findOne({ user_id });
        if (!student) return res.render("index", { error: "Invalid credentials" });

        const ok = bcrypt.compareSync(password, student.password);
        if (!ok) return res.render("index", { error: "Invalid credentials" });

        req.session.studentId = student.user_id;
        req.session.studentName = student.name;
        req.session.studentEmail = student.email;

        res.redirect('/student');
        
    } else {
        const { user_id, password } = req.body;

        const teacher = await Teacher.findOne({ user_id });
        if (!teacher) return res.render("index", { error: "Invalid credentials" });

        const ok = bcrypt.compareSync(password, teacher.password);
        if (!ok) return res.render("index", { error: "Invalid credentials" });

        req.session.teacherId = teacher.user_id;
        req.session.teacherName = teacher.name;

        res.redirect('/teacher');
    }
});


app.get("/student", async (req, res) => {
    const studentComplaints = await Complaint.find({ studentId: req.session.studentId });

        res.render('student', {
            studentName: req.session.studentName,
            studentEmail: req.session.studentEmail,
            studentId: req.session.studentId,
            complaints: studentComplaints,
            STATUS
        });
});

app.get("/teacher", async(req, res) => {

    const pending = await Complaint.find({ status: STATUS.PENDING });
    const resolved = await Complaint.find({ status: STATUS.RESOLVED });

    res.render("teacher", {
        teacherName: req.session.teacherName,
        teacherId: req.session.teacherId,
        pendingComplaints: pending,
        resolvedComplaints: resolved,
        STATUS
    });
})
// --------------------------------------------------
// STUDENT LOGIN
// --------------------------------------------------
// app.get('/student/login', (req, res) => {
//     res.render('student-login', { error: null });
// });

app.get('/student/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/login');
});

// --------------------------------------------------
// TEACHER LOGIN
// --------------------------------------------------
// app.get('/teacher/login', (req, res) => {
//     res.render('teacher-login', { error: null });
// });

app.get('/teacher/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/teacher/login');
});


// --------------------------------------------------
// SUBMIT COMPLAINT
// --------------------------------------------------
app.post('/submit-complaint', requireStudentAuth, async (req, res) => {
    const { subject, complaintText } = req.body;

    const complaint = new Complaint({
        studentId: req.session.studentId,
        studentName: req.session.studentName,
        email: req.session.studentEmail,
        subject,
        complaintText,
        status: STATUS.PENDING,
        aiDraft: null,
        finalResponse: null,
        teacherResponse: null,
        createdAt: new Date(),
        history: []
    });

    await complaint.save();

    // AI draft
    try {
        const aiResp = await axios.post(`${FLASK_URL}/generate-draft`, {
            studentName: complaint.studentName,
            subject: subject,
            complaint: complaintText,
            studentEmail: complaint.email,
            studentId: complaint.studentId
        });

        complaint.aiDraft = aiResp.data.draft;
        complaint.history.push({
            timestamp: new Date(),
            action: "ai_draft_generated",
            content: complaint.aiDraft
        });

        await complaint.save();

        broadcastToTeachers({
            type: "NEW_COMPLAINT",
            data: complaint
        });

    } catch (err) {
        console.error("AI draft error:", err);
    }

    res.redirect('/student');
});


// --------------------------------------------------
// TEACHER ACTION
// --------------------------------------------------
app.post('/teacher-action', requireTeacherAuth, async (req, res) => {
    const { complaintId, action, manualResponse, shouldPolish } = req.body;

    const complaint = await Complaint.findById(complaintId);
    if (!complaint) return res.status(404).send("Complaint not found");

    let finalResp = action === 'approve'
        ? complaint.aiDraft
        : manualResponse;

    // Polishing
    if (action === 'manual' && shouldPolish === 'true') {
        try {
            const polish = await axios.post(`${FLASK_URL}/polish-response`, {
                original: manualResponse,
                complaint: complaint.complaintText,
                context: { aiDraft: complaint.aiDraft }
            });

            finalResp = polish.data.polished;
        } catch (err) {
            console.error("Polish failed:", err);
        }
    }

    complaint.finalResponse = finalResp;
    complaint.teacherResponse = finalResp;
    complaint.status = STATUS.RESOLVED;

    complaint.history.push({
        timestamp: new Date(),
        action: action === "approve" ? "teacher_approved_ai" : "teacher_manual",
        content: finalResp
    });

    await complaint.save();

    // Notify student
    const studentWs = studentConnections.get(complaint.studentId);
    if (studentWs && studentWs.readyState === WebSocket.OPEN) {
        studentWs.send(JSON.stringify({
            type: "COMPLAINT_UPDATED",
            data: complaint
        }));
    }

    broadcastToTeachers({
        type: "COMPLAINT_UPDATED",
        data: complaint
    });

    res.redirect('/teacher');
});

// --------------------------------------------------
// WEBSOCKETS
// --------------------------------------------------
wss.on("connection", (ws, req) => {
    const url = req.url;

    if (url.includes("/teacher-ws")) {
        teacherConnections.add(ws);
        ws.on("close", () => teacherConnections.delete(ws));
    } else if (url.includes("/student-ws")) {
        const params = new URLSearchParams(url.split("?")[1]);
        const studentId = params.get("studentId");
        if (studentId) studentConnections.set(studentId, ws);
        ws.on("close", () => studentConnections.delete(studentId));
    }
});

function broadcastToTeachers(msg) {
    const data = JSON.stringify(msg);
    teacherConnections.forEach(ws => {
        if (ws.readyState === WebSocket.OPEN) ws.send(data);
    });
}

server.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});
