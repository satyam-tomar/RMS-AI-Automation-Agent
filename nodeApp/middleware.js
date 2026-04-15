const ExpressError = require("./utils/ExpressError");

module.exports.requireStudentAuth = (req, res, next) => {
    if (!req.session || !req.session.studentId) {
        return res.redirect("/login");
    }
    next();
};

module.exports.requireTeacherAuth = (req, res, next) => {
    if (!req.session || !req.session.teacherId) {
        return res.redirect('/login');
    }
    next();
};