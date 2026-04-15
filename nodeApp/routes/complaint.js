const express = require("express"); 
const router = express.Router(); 
const {requireStudentAuth, requireTeacherAuth} = require("../middleware"); 
const complaintController = require("../controllers/complaint"); 
const wrapAsync = require("../utils/wrapAsync");

router.post('/submit-complaint', requireStudentAuth, wrapAsync(complaintController.submitComplaint)); 
router.post('/teacher-action', requireTeacherAuth, wrapAsync(complaintController.teacherAction));
router.post('/internal/ai-callback', wrapAsync(complaintController.internalAPI)); 
router.delete('/complaints/:id', requireStudentAuth, wrapAsync(complaintController.delete)); 

module.exports = router; 