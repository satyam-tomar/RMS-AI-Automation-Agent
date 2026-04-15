const mongoose = require('mongoose');

const teacherSchema = new mongoose.Schema({
    user_id: {
        type: String,
        required: true,
        unique: true
    },

    name: {
        type: String,
        required: true
    },

    password: {
        type: String,
        required: true
    },

    department: {
        type: String,
        required: true,
        enum: [
            // Academic
            'Computer Science',
            'Information Technology',
            'Electronics',
            'Electrical Engineering',
            'Mechanical Engineering',
            'Civil Engineering',
            'Chemical Engineering',
            'AI & Data Science',
            'Mathematics',
            'Physics',
            'Chemistry',
            'Humanities',
            'Management',

            // Hostel / Residential
            'Hostel Administration',
            'Hostel Warden',
            'Assistant Warden',
            'Mess Supervisor',
            'Mess Management',
            'Maintenance & Facilities',

            'Examination Cell',
            'Student Affairs',
            'Admissions',
            'Library',
            'Transport',
            'Sports Department',
            'Training & Placement',
            'Accounts & Finance',
            'IT Support',
            'Security Department',
            'Health Center'
        ]
    }

}, { timestamps: true });

module.exports = mongoose.model('Teacher', teacherSchema);
