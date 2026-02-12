# src/api/routes.py

from flask import request, jsonify

def register_routes(app, agent):
    
    @app.route("/generate-draft", methods=["POST"])
    def generate_draft():
        data = request.json
        
        student_name = data.get("studentName") or data.get("student_name")
        subject = data.get("subject")
        complaint = data.get("complaint")
        
        if not student_name or not subject or not complaint:
            return jsonify({
                "error": "Missing required fields: student_name, subject, complaint"
            }), 400
        
        result = agent.handle_complaint(
            student_name=student_name,
            subject=subject,
            complaint=complaint
        )
        
        return jsonify({
            "draft": result["result"],
            "status": result["status"]
        })
    
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"})