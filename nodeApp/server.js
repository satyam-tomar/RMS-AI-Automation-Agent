require('dotenv').config();

const express = require('express');
const http = require('http');
const path = require('path');
const session = require('express-session');
const mongoose = require('mongoose');

const client = require("./lib/redis");
const { initWebSocket } = require("./services/socketService");
const userRouter = require("./routes/user");
const complaintRouter = require("./routes/complaint");

// -------------------------------
// GLOBAL ERROR SAFETY
// -------------------------------
process.on('uncaughtException', (err) => {
    console.error('UNCAUGHT EXCEPTION:', err.message);
    console.error(err.stack);
});

process.on('unhandledRejection', (reason) => {
    console.error('UNHANDLED REJECTION:', reason);
});

// -------------------------------
// APP INIT
// -------------------------------
const app = express();
const server = http.createServer(app);

// -------------------------------
// WEBSOCKET INIT
// -------------------------------
initWebSocket(server);

// -------------------------------
// DB CONNECTION
// -------------------------------
mongoose.connect(process.env.MONGODB_URL)
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.log(err));

// -------------------------------
// MIDDLEWARE
// -------------------------------
app.set('trust proxy', 1); // required for Render

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(session({
    secret: 'complaint-system-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: true,          // required on Render (HTTPS)
        sameSite: "lax",       // best for same-origin apps
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000
    }
}));

// -------------------------------
// VIEW ENGINE
// -------------------------------
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));

// -------------------------------
// ROUTES
// -------------------------------
app.get('/', (req, res) => {
    res.render('home');
});

app.get('/b', (req, res) => {
    res.render('best_ui');
});

app.use("/", userRouter);
app.use("/", complaintRouter);

// -------------------------------
// ERROR HANDLER
// -------------------------------
app.use((err, req, res, next) => {
    if (res.headersSent) return next(err);

    const statusCode = err.statusCode || 500;
    const message = err.message || "Something went wrong";

    console.error(`[ERROR ${statusCode}]:`, message);
    res.status(statusCode).render("error", { statusCode, message });
});

// -------------------------------
// SERVER START
// -------------------------------
async function startServer() {
    try {
        if (process.env.REDIS_URL) {
            await client.connect();
            console.log("Redis Connected");
        } else {
            console.log("Redis not configured, skipping...");
        }

        const PORT = process.env.PORT || 3000;

        server.listen(PORT, () => {
            console.log(`Server running on port ${PORT}`);
        });

    } catch (err) {
        console.error("Startup error:", err);

        const PORT = process.env.PORT || 3000;
        server.listen(PORT);
    }
}

startServer();



// require('dotenv').config();

// const express = require('express');
// const redis = require('redis');

// const http = require('http');
// const WebSocket = require('ws');
// const axios = require('axios');
// const path = require('path');
// const session = require('express-session');
// const bcrypt = require('bcryptjs');
// const mongoose = require('mongoose');

// // Models
// const Student = require('./model/student');
// const Teacher = require("./model/teacher");
// const Complaint = require('./model/complaints');

// const app = express();
// const server = http.createServer(app);
// const wss = new WebSocket.Server({ server });

// const wrapAsync = require("./utils/wrapAsync");
// const ExpressError = require("./utils/ExpressError");
// const { requireStudentAuth, requireTeacherAuth } = require("./middleware");
// const { initWebSocket } = require("./services/socket");

// const client = redis.createClient({
//     password: process.env.REDIS_PASSWORD,
//     socket: {
//         host: process.env.REDIS_HOST,
//         port: process.env.REDIS_PORT
//     }
// })

// client.on('error', (err) => { console.error("Redis Client Error: ", err) });

// const client = require("./lib/redis");

// async function startServer() {
//     try {
//         await client.connect();
//         console.log("Redis Connected");
//         server.listen(3000, () => console.log("Server on http://localhost:3000"));
//     } catch (err) {
//         console.error("Failed to connect to Redis", err);
//     }
// }
// startServer();

// initWebSocket(server);

// // MongoDB Connection
// mongoose.connect("mongodb://127.0.0.1:27017/complaint_system")
//     .then(() => console.log("MongoDB connected"))
//     .catch(err => console.log(err));

// app.use(express.json());
// app.use(express.urlencoded({ extended: true }));
// app.use(session({
//     secret: 'complaint-system-secret-key',
//     resave: false,
//     saveUninitialized: false,
//     cookie: {
//         secure: process.env.NODE_ENV === 'production',
//         httpOnly: true,
//         maxAge: 24 * 60 * 60 * 1000 // 24 hours
//     }
// }));

// app.set('view engine', 'ejs');
// app.set('views', path.join(__dirname, 'views'));
// app.use(express.static(path.join(__dirname, 'public')));


// const STATUS = { PENDING: "pending", RESOLVED: "resolved" };
// const FLASK_URL = "http://localhost:5000";

// const teacherConnections = new Set();
// const studentConnections = new Map();


// // Routes
// // app.get('/', (req, res) => res.render('home'));

// app.get('/login', (req, res) => res.render('index'));

// app.post("/login", wrapAsync(async (req, res) => {

// }));


// app.get("/student", requireStudentAuth, wrapAsync(async (req, res) => {
//     const studentComplaints = await Complaint.find({ studentId: req.session.studentId }).sort({ createdAt: -1 });

//     res.render('student', {
//         studentName: req.session.studentName,
//         studentEmail: req.session.studentEmail,
//         studentId: req.session.studentId,
//         complaints: studentComplaints,
//         STATUS
//     });
// }));

// app.get("/teacher", requireTeacherAuth, wrapAsync(async (req, res) => {
//     const pending = await Complaint.find({ status: STATUS.PENDING }).sort({ createdAt: -1 });
//     const resolved = await Complaint.find({ status: STATUS.RESOLVED }).sort({ createdAt: -1 });

//     res.render("teacher", {
//         teacherName: req.session.teacherName,
//         teacherId: req.session.teacherId,
//         pendingComplaints: pending,
//         resolvedComplaints: resolved,
//         STATUS
//     });
// }));

// app.get('/student/logout', requireStudentAuth, (req, res) => {
//     req.session.destroy(() => {
//         res.redirect('/login');
//     });
// });

// app.get('/teacher/logout', requireTeacherAuth, (req, res) => {
//     req.session.destroy(() => {
//         res.redirect('/login');
//     });
// });


// // --------------------------------------------------
// // SUBMIT COMPLAINT
// // --------------------------------------------------
// app.post('/submit-complaint', requireStudentAuth, wrapAsync(async (req, res) => {
//     const { subject, complaintText } = req.body;

//     if (!subject || !complaintText) {
//         throw new ExpressError(400, "Incomplete Complaint");
//     }

//     const complaint = new Complaint({
//         studentId: req.session.studentId,
//         studentName: req.session.studentName,
//         email: req.session.studentEmail,
//         subject,
//         complaintText,
//         status: STATUS.PENDING,
//         aiDraft: null,
//         finalResponse: null,
//         teacherResponse: null,
//         createdAt: new Date(),
//         history: []
//     });

//     await complaint.save();

//     try {
//         await client.lPush('task_queue', JSON.stringify(complaint));
//     } catch (e) {
//         throw new ExpressError(500, "Queueing failed, please try again.");
//     }
//     res.status(200).json({
//         success: true,
//         message: "RMS submited Successfully"
//     })

//     // // AI draft
//     //     const aiResp = await axios.post(`${FLASK_URL}/generate-draft`, {
//     //         studentName: complaint.studentName,
//     //         subject: subject,
//     //         complaint: complaintText,
//     //         studentEmail: complaint.email,
//     //         studentId: complaint.studentId
//     //     });

//     //     complaint.aiDraft = aiResp.data.draft;
//     //     complaint.history.push({
//     //         timestamp: new Date(),
//     //         action: "ai_draft_generated",
//     //         content: complaint.aiDraft
//     //     });

//     //     await complaint.save();

//     //     broadcastToTeachers({
//     //         type: "NEW_COMPLAINT",
//     //         data: complaint
//     //     });

//     // res.redirect('/student');
// }));

// app.post('/internal/ai-callback', wrapAsync(async (req, res) => {
//     const { complaintId, aiDraft } = req.body;

//     const complaint = await Complaint.findById(complaintId);
//     if (!complaint) {
//         throw new ExpressError(404, "Complaint Not found");
//     }

//     complaint.aiDraft = aiDraft;
//     complaint.history.push({
//         timestamp: new Date(),
//         action: "ai_draft_generated",
//         content: aiDraft
//     });
//     await complaint.save();

//     broadcastToTeachers({
//         type: "NEW_COMPLAINT",
//         data: complaint
//     });

//     console.log(`AI Draft updated and broadcasted for: ${complaintId}`);
//     res.status(200).json({ success: true });
// }));

// app.delete('/complaints/:id', wrapAsync(async (req, res) => {
//     const { id } = req.params;
//     const studentId = req.session.studentId;

//     if (!studentId) {
//         throw new ExpressError(401, "Unauthorized");
//     }

//     const complaint = await Complaint.findOne({
//         _id: id,
//         studentId,
//         status: 'pending'
//     });

//     if (!complaint) {
//         throw new ExpressError(404, "Complaint not found or cannot be withdrawn");
//     }

//     await Complaint.deleteOne({ _id: id });

//     return res.json({ message: 'Complaint withdrawn successfully' });
// }));

// // --------------------------------------------------
// // TEACHER ACTION
// // --------------------------------------------------
// app.post('/teacher-action', requireTeacherAuth, async (req, res) => {
//     const { complaintId, action, manualResponse, shouldPolish } = req.body;

//     const complaint = await Complaint.findById(complaintId);
//     if (!complaint) return res.status(404).send("Complaint not found");

//     let finalResp = action === 'approve'
//         ? complaint.aiDraft
//         : manualResponse;

//     // Polishing
//     if (action === 'manual' && shouldPolish === 'true') {
//         try {
//             const polish = await axios.post(`${FLASK_URL}/polish-response`, {
//                 original: manualResponse,
//                 complaint: complaint.complaintText,
//                 context: { aiDraft: complaint.aiDraft }
//             });

//             finalResp = polish.data.polished;
//         } catch (err) {
//             console.error("Polish failed:", err);
//         }
//     }

//     complaint.finalResponse = finalResp;
//     complaint.teacherResponse = finalResp;
//     complaint.status = STATUS.RESOLVED;

//     complaint.history.push({
//         timestamp: new Date(),
//         action: action === "approve" ? "teacher_approved_ai" : "teacher_manual",
//         content: finalResp
//     });

//     await complaint.save();

//     // Notify student
//     const studentWs = studentConnections.get(complaint.studentId);
//     if (studentWs && studentWs.readyState === WebSocket.OPEN) {
//         studentWs.send(JSON.stringify({
//             type: "COMPLAINT_UPDATED",
//             data: complaint
//         }));
//     }

//     broadcastToTeachers({
//         type: "COMPLAINT_UPDATED",
//         data: complaint
//     });

//     res.redirect('/teacher');
// });

// // --------------------------------------------------
// // WEBSOCKETS
// // --------------------------------------------------
// wss.on("connection", (ws, req) => {
//     const url = req.url;

//     if (url.includes("/teacher-ws")) {
//         teacherConnections.add(ws);
//         ws.on("close", () => teacherConnections.delete(ws));
//     } else if (url.includes("/student-ws")) {
//         const params = new URLSearchParams(url.split("?")[1]);
//         const studentId = params.get("studentId");
//         if (studentId) studentConnections.set(studentId, ws);
//         ws.on("close", () => studentConnections.delete(studentId));
//     }
// });

// function broadcastToTeachers(msg) {
//     const data = JSON.stringify(msg);
//     teacherConnections.forEach(ws => {
//         if (ws.readyState === WebSocket.OPEN) ws.send(data);
//     });
// }

// app.use((err, req, res, next) => {
//     let { statusCode = 500, message = "Something went wrong" } = err;
//     res.status(statusCode).render("error", { message });
// });

// server.listen(3000, () => {
//     console.log("Server running on http://localhost:3000");
// });
