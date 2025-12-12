const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

// Models
const Student = require('../model/student');
const Teacher = require('../model/teacher');
const Complaint = require('../model/complaints');

// DB Connect
mongoose.connect('mongodb://127.0.0.1:27017/complaint_system')
    .then(() => console.log("MongoDB connected"))
    .catch(err => console.log("MongoDB connection error:", err));

async function seed() {
    try {
        // Clear existing data
        await Student.deleteMany({});
        await Teacher.deleteMany({});
        await Complaint.deleteMany({});

        // Seed Students
        const students = await Student.insertMany([
            {
                user_id: "12315567",
                name: "Satyam Tomar",
                email: "satyamtomar23@lpu.in",
                password: bcrypt.hashSync("123123", 10),
                hostel: "BH6",
                mess: "Mess1",
                block: "A",
                room_number: "A713"
            },
            {
                user_id: "12315589",
                name: "Shivam Tomar",
                email: "shivamtomar23@lpu.in",
                password: bcrypt.hashSync("123123", 10),
                hostel: "BH3",
                mess: "Mess2",
                block: "B",
                room_number: "B315"
            }
        ]);

        // Seed Teachers
        const teachers = await Teacher.insertMany([
            {
                user_id: "12345",
                name: "Dr. Arvindar Singh",
                password: bcrypt.hashSync("123123", 10),
                department: "Computer Science"
            },
            {
                user_id: "54321",
                name: "Mr. Rahul Sharma",
                password: bcrypt.hashSync("123123", 10),
                department: "Hostel Warden"
            }
        ]);

        // Seed Complaints
        const complaints = await Complaint.insertMany([
            {
                studentId: students[0].user_id,
                studentName: students[0].name,
                email: students[0].email,
                subject: "WiFi not working",
                complaintText: "The WiFi in BH6 Block A floor 7 is not working.",
                aiDraft: "The WiFi appears to be malfunctioning in the BH6 hostel, kindly resolve the issue.",
                teacherResponse: null,
                finalResponse: null,
                status: "pending",
                history: [{ action: "submitted", content: "WiFi complaint submitted." }]
            },
            {
                studentId: students[1].user_id,
                studentName: students[1].name,
                email: students[1].email,
                subject: "Mess food quality issue",
                complaintText: "The dinner quality in Mess2 has been poor for the last few days.",
                aiDraft: "There seems to be a decline in the food quality in Mess2, please look into it.",
                teacherResponse: null,
                finalResponse: null,
                status: "pending",
                history: [{ action: "submitted", content: "Mess food complaint submitted." }]
            }
        ]);

        console.log("Seeding completed successfully!");
    } catch (err) {
        console.error("Seeding error:", err);
    } finally {
        mongoose.connection.close();
    }
}

seed();
