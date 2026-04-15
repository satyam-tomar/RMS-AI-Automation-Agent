const Complaint = require("../model/complaints");
const { broadcastToTeachers, notifyStudent } = require("../services/socketService");
const client = require("../lib/redis");
const ExpressError = require("../utils/ExpressError");

const STATUS = { PENDING: "pending", RESOLVED: "resolved" };

module.exports.submitComplaint = async (req, res) => {
    const { subject, complaintText } = req.body;
    if (!subject || !complaintText) {
        throw new ExpressError(400, "Incomplete Complaint");
    }

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

    try {
        await client.lPush('task_queue', JSON.stringify(complaint));
    } catch (e) {
        throw new ExpressError(500, "Queueing failed, please try again.");
    }

    return res.status(200).json({
        success: true,
        message: "RMS submitted Successfully"
    });
};

module.exports.internalAPI = async (req, res) => {
    const { complaintId, aiDraft } = req.body;
    const complaint = await Complaint.findById(complaintId);

    if (!complaint) {
        throw new ExpressError(404, "Complaint Not found");
    }

    complaint.aiDraft = aiDraft;
    complaint.history.push({
        timestamp: new Date(),
        action: "ai_draft_generated",
        content: aiDraft
    });

    await complaint.save();

    broadcastToTeachers({
        type: "NEW_COMPLAINT",
        data: complaint
    });

    console.log(`AI Draft updated and broadcasted for: ${complaintId}`);
    return res.status(200).json({ success: true });
};

module.exports.delete = async (req, res) => {
    const { id } = req.params;
    const studentId = req.session.studentId;

    if (!studentId) {
        throw new ExpressError(401, "Unauthorized");
    }

    const complaint = await Complaint.findOne({
        _id: id,
        studentId,
        status: STATUS.PENDING
    });

    if (!complaint) {
        throw new ExpressError(404, "Complaint not found or cannot be withdrawn");
    }

    await Complaint.deleteOne({ _id: id });
    return res.json({ message: 'Complaint withdrawn successfully' });
};

module.exports.teacherAction = async (req, res) => {
    const { complaintId, action, manualResponse } = req.body;

    const complaint = await Complaint.findById(complaintId);
    if (!complaint) throw new ExpressError(404, "Complaint not found");

    let finalResp = action === 'approve'
        ? complaint.aiDraft
        : manualResponse;

    complaint.finalResponse = finalResp;
    complaint.teacherResponse = finalResp;
    complaint.status = STATUS.RESOLVED;
    complaint.history.push({
        timestamp: new Date(),
        action: action === "approve" ? "teacher_approved_ai" : "teacher_manual",
        content: finalResp
    });

    await complaint.save();

    notifyStudent(complaint.studentId, {
        type: "COMPLAINT_UPDATED",
        data: complaint
    });

    broadcastToTeachers({
        type: "COMPLAINT_UPDATED",
        data: complaint
    });

    return res.redirect('/teacher');
};