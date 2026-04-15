const Student = require("../model/student");
const Teacher = require("../model/teacher");
const Complaint = require("../model/complaints");
const bcrypt = require("bcryptjs");
const ExpressError = require("../utils/ExpressError");

const STATUS = { PENDING: "pending", RESOLVED: "resolved" };

module.exports.renderLogin = (req, res) => {
    if (req.session && req.session.studentId) {
        return res.redirect('/');
    }
    if (req.session && req.session.teacherId) {
        return res.redirect('/teacher');
    }
    return res.render('index', { error: null });
};

module.exports.login = async (req, res) => {
    const { role, user_id, password } = req.body;

    if (!role) {
        return res.render("index", { error: "Please select a role" });
    }

    if (role.toLowerCase() === "student") {
        const student = await Student.findOne({ user_id });
        if (!student) {
            return res.render("index", { error: "Invalid credentials" });
        }

        const ok = bcrypt.compareSync(password, student.password);
        if (!ok) {
            return res.render("index", { error: "Invalid credentials" });
        }

        req.session.studentId = student.user_id;
        req.session.studentName = student.name;
        req.session.studentEmail = student.email;
        return res.redirect('/');

    } else if (role.toLowerCase() === "teacher") {
        const teacher = await Teacher.findOne({ user_id });
        if (!teacher) {
            return res.render("index", { error: "Invalid credentials" });
        }

        const ok = bcrypt.compareSync(password, teacher.password);
        if (!ok) {
            return res.render("index", { error: "Invalid credentials" });
        }

        req.session.teacherId = teacher.user_id;
        req.session.teacherName = teacher.name;
        return res.redirect('/teacher');

    } else {
        return res.render("index", { error: "Invalid role selected" });
    }
};

module.exports.studentLogout = (req, res) => {
    req.session.destroy(() => {
        return res.redirect('/login');
    });
};

module.exports.teacherLogout = (req, res) => {
    req.session.destroy(() => {
        return res.redirect('/login');
    });
};

module.exports.teacher = async (req, res) => {
    const pending = await Complaint.find({ 
        status: STATUS.PENDING,
        aiDraft: { $ne: null }
    }).sort({ createdAt: -1 });

    const resolved = await Complaint.find({ 
        status: STATUS.RESOLVED,
        aiDraft: { $ne: null }
    }).sort({ createdAt: -1 });

    return res.render("teacher", {
        teacherName: req.session.teacherName,
        teacherId: req.session.teacherId,
        pendingComplaints: pending,
        resolvedComplaints: resolved,
        STATUS
    });
};

module.exports.student = async (req, res) => {
    const studentComplaints = await Complaint.find({
        studentId: req.session.studentId
    }).sort({ createdAt: -1 });

    return res.render('student', {
        studentName: req.session.studentName,
        studentEmail: req.session.studentEmail,
        studentId: req.session.studentId,
        complaints: studentComplaints,
        STATUS
    });
};