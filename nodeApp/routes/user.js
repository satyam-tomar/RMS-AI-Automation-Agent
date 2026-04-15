const express = require("express");
const router = express.Router(); 
const wrapAsync = require("../utils/wrapAsync");
const {requireStudentAuth, requireTeacherAuth} = require("../middleware"); 
const userController = require("../controllers/user"); 

router.route("/login")
.get(wrapAsync(userController.renderLogin))
.post(wrapAsync(userController.login));

router.get('/student/logout', requireStudentAuth, userController.studentLogout);
router.get('/teacher/logout', requireTeacherAuth, userController.teacherLogout); 

router.get('/student', requireStudentAuth, wrapAsync(userController.student)); 
router.get('/teacher', requireTeacherAuth, wrapAsync(userController.teacher)); 

module.exports = router; 