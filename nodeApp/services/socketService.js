const WebSocket = require('ws');

const teacherConnections = new Set();
const studentConnections = new Map();

const initWebSocket = (server) => {
    const wss = new WebSocket.Server({ server });

    wss.on("connection", (ws, req) => {
        const url = req.url;

        if (url.includes("/teacher-ws")) {
            teacherConnections.add(ws);
            ws.on("close", () => teacherConnections.delete(ws));
        } 
        else if (url.includes("/student-ws")) {
            const params = new URLSearchParams(url.split("?")[1]);
            const studentId = params.get("studentId");
            if (studentId) {
                studentConnections.set(studentId, ws);
                ws.on("close", () => {
                    if (studentConnections.get(studentId) === ws) {
                        studentConnections.delete(studentId);
                    }
                });
            }
        }
    });

    return wss;
};


const broadcastToTeachers = (msg) => {
    const data = JSON.stringify(msg);
    teacherConnections.forEach(ws => {
        if (ws.readyState === WebSocket.OPEN) ws.send(data);
    });
};


const notifyStudent = (studentId, msg) => {
    const ws = studentConnections.get(studentId);
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(msg));
    }
};

module.exports = {
    initWebSocket,
    broadcastToTeachers,
    notifyStudent
};