const mongoose = require('mongoose');

const studentSchema = new mongoose.Schema({
    user_id: {
        type: String,
        required: true,
        unique: true
    },
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },

    // New fields
    hostel: {
        type: String,
        enum: ['BH1','BH2','BH3','BH4','BH5','BH6','BH7','BH8','BH9','BH10'],
        required: true
    },
    mess: {
        type: String,
        enum: ['Mess1', 'Mess2'],
        required: true
    },
    block: {
        type: String,
        enum: ['A','B','C'],
        required: true
    },
    room_number: {
        type: String,
        match: /^[A-Z]\d{3}$/,   // Example: A712, B304, C125
        required: true
    },

    // Combined for quick access (optional)
    fullRoomCode: {
        type: String,
        default: function () {
            return `${this.hostel}-${this.room_number}`;
        }
    }

}, { timestamps: true });

module.exports = mongoose.model('Student', studentSchema);
