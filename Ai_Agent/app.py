from flask import Flask, request, jsonify
from main import UniversityComplaintAgent
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)

# Initialize agent once
agent = UniversityComplaintAgent(
    api_key=API_KEY,
    rebuild_index=False,
    embedding_model="all-MiniLM-L6-v2"
)

@app.route("/generate-draft", methods=["POST"])
def generate_draft():
    data = request.json
    student_name = data.get("studentName") or data.get("student_name")
    subject = data.get("subject")
    complaint = data.get("complaint")

    if not (student_name and subject and complaint):
        return jsonify({"error": "Missing student_name, subject, or complaint"}), 400

    # Call the AI agent
    result = agent.handle_complaint(
        student_name=student_name,
        subject=subject,
        complaint=complaint
    )

    # Return draft only
    return jsonify({"draft": result["result"], "status": result["status"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



















# from main import UniversityComplaintAgent
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env
# load_dotenv()

# def main():
#     # Get API key from .env
#     API_KEY = os.getenv("GOOGLE_API_KEY")
#     if not API_KEY:
#         print("⚠️ GOOGLE_API_KEY not found in .env")
#         return

#     # Initialize the AI agent
#     agent = UniversityComplaintAgent(
#         api_key=API_KEY,
#         rebuild_index=False,  # True if first time
#         embedding_model="all-MiniLM-L6-v2"
#     )

#     # Manually provide student details
#     student_name = "John Doe"
#     subject = "Attendance Shortage"
#     complaint = (
#         "I have 70% attendance due to medical issues. "
#         "I have valid medical certificates. Can I appear for exams?"
#     )

#     # Call the agent function
#     result = agent.handle_complaint(
#         student_name=student_name,
#         subject=subject,
#         complaint=complaint
#     )

#     # Print the result
#     print("="*60)
#     print(f"Student: {result['student_name']}")
#     print(f"Subject: {result['subject']}")
#     print(f"Complaint: {result['complaint']}")
#     print(f"Resolution: {result['result']}")
#     print(f"Status: {result['status']}")
#     print("="*60)

# if __name__ == "__main__":
#     main()