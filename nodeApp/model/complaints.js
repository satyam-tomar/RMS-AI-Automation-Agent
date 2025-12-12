const mongoose = require('mongoose');

const historySchema = new mongoose.Schema({
    timestamp: {
        type: Date,
        default: Date.now
    },
    action: {
        type: String,
        required: true
    },
    content: {
        type: String,
        required: true
    }
}, { _id: false });

const complaintSchema = new mongoose.Schema({
    studentId: {
        type: String,   // matches req.session.studentId
        required: true
    },
    studentName: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },

    subject: {
        type: String,
        required: true
    },
    complaintText: {
        type: String,
        required: true
    },

    aiDraft: {
        type: String,
        default: null
    },
    teacherResponse: {
        type: String,
        default: null
    },
    finalResponse: {
        type: String,
        default: null
    },

    status: {
        type: String,
        enum: ['pending', 'resolved'],
        default: 'pending'
    },

    history: [historySchema],

    createdAt: {
        type: Date,
        default: Date.now
    }

}, { timestamps: true });

module.exports = mongoose.model('Complaint', complaintSchema);
