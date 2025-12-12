import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
#why??????

from flask import Flask, request, jsonify, render_template
from embedding import embed_text
from cluster_manager import ClusterManager
from alert_manager import AlertManager
import random

app = Flask(__name__)

# Initialize components
cluster_manager = ClusterManager(n_clusters=5)
alert_manager = AlertManager(window_minutes=10, threshold=3)

SEED_COMPLAINTS = [
    # College infrastructure
    "The classroom lights are not working",
    "Projectors in lecture halls are broken",
    "Library resources are outdated",
    "Labs are not well-maintained",
    "Insufficient seating in lecture halls",

    # Hostel issues
    "Room cleaning is not done regularly",
    "Water supply in the hostel is inconsistent",
    "Mess food quality is poor",
    "WiFi in hostel rooms is very slow",
    "Hostel staff is unhelpful",

    # Examination
    "Exam schedule was not announced on time",
    "Question papers were leaked",
    "Grading of answer sheets is unfair",
    "Exam halls are overcrowded",
    "Re-evaluation process takes too long",

    # Holidays and events
    "Holiday notifications are late",
    "Festivals and events are not organized properly",
    "No notice about college closure",
    "Extra classes are scheduled on holidays",
    "Insufficient break between exams",

    # Mess and cafeteria
    "Mess menu is repetitive",
    "Food portions are very small",
    "Hygiene in the cafeteria is poor",
    "Water in the mess is not clean",
    "Mess timings are inconvenient"
]

DUMMY_COMPLAINTS = [
    "Room cleaning is not done regularly",
    "Water supply in the hostel is inconsistent",
    "Mess food quality is poor",
    "WiFi in hostel rooms is very slow",
    "Exam schedule was not announced on time",
    "Question papers were leaked",
    "Grading of answer sheets is unfair",
    "Holiday notifications are late",
    "Mess menu is repetitive",
    "Food portions are very small"
]

def initialize_clusters():
    """
    Initialize cluster model with seed data before accepting live complaints.
    """
    print("Initializing cluster model with seed complaints...")
    
    for complaint in SEED_COMPLAINTS:
        embedding = embed_text(complaint)
        cluster_manager.add_initial_sample(embedding)
    
    cluster_manager.initialize()
    print(f"Cluster model initialized with {len(SEED_COMPLAINTS)} seed complaints.")

# Initialize on startup
with app.app_context():
    initialize_clusters()

@app.route('/ingest', methods=['POST'])
def ingest_complaint():
    """
    Receives a complaint, processes it through the pipeline,
    and returns JSON or HTML alert based on threshold detection.
    """
    data = request.get_json()
    complaint_text = data.get('complaint', '')
    
    if not complaint_text:
        return jsonify({'error': 'No complaint text provided'}), 400
    
    # Step 1: Embed the complaint
    embedding = embed_text(complaint_text)
    
    # Step 2: Assign to nearest cluster
    cluster_id = cluster_manager.assign_cluster(embedding)
    
    # Step 3: Record in alert manager
    alert_manager.record_complaint(cluster_id, complaint_text)
    
    # Step 4: Check for alert condition
    alert_triggered, alert_data = alert_manager.check_alert(cluster_id)
    
    if alert_triggered:
        return render_template(
            'alert.html',
            cluster_id=cluster_id,
            complaint_count=alert_data['count'],
            recent_complaints=alert_data['complaints']
        )
    
    return jsonify({
        'status': 'processed',
        'complaint': complaint_text,
        'cluster_id': int(cluster_id),
        'alert': False
    })

@app.route('/simulate', methods=['GET'])
def simulate():
    """
    Simulates complaint ingestion by randomly selecting
    from dummy data and calling the pipeline.
    """
    complaint = random.choice(DUMMY_COMPLAINTS)
    
    embedding = embed_text(complaint)
    cluster_id = cluster_manager.assign_cluster(embedding)
    alert_manager.record_complaint(cluster_id, complaint)
    alert_triggered, alert_data = alert_manager.check_alert(cluster_id)
    
    if alert_triggered:
        return render_template(
            'alert.html',
            cluster_id=cluster_id,
            complaint_count=alert_data['count'],
            recent_complaints=alert_data['complaints']
        )
    
    return jsonify({
        'status': 'simulated',
        'complaint': complaint,
        'cluster_id': int(cluster_id),
        'alert': False
    })

@app.route('/status', methods=['GET'])
def status():
    """
    Returns current system status including cluster counts.
    """
    cluster_counts = alert_manager.get_cluster_counts()
    
    # Convert keys and values to native Python types
    cluster_counts = {int(k): int(v) for k, v in cluster_counts.items()}
    
    return jsonify({
        'active_clusters': len(cluster_counts),
        'cluster_counts': cluster_counts,
        'total_complaints': sum(cluster_counts.values())
    })

@app.route('/test_alert', methods=['GET'])
def test_alert():
    """
    Test endpoint to quickly trigger an alert by sending similar complaints.
    """
    test_complaint = "Internet connection is not working"
    results = []
    
    for i in range(3):
        embedding = embed_text(test_complaint)
        cluster_id = cluster_manager.assign_cluster(embedding)
        alert_manager.record_complaint(cluster_id, test_complaint)
        alert_triggered, alert_data = alert_manager.check_alert(cluster_id)
        
        results.append({
            'iteration': i + 1,
            'cluster_id': int(cluster_id),
            'alert_triggered': alert_triggered
        })
        
        if alert_triggered:
            return render_template(
                'alert.html',
                cluster_id=cluster_id,
                complaint_count=alert_data['count'],
                recent_complaints=alert_data['complaints']
            )
    
    return jsonify({
        'status': 'test_completed',
        'results': results,
        'message': 'Alert not triggered (complaints may be in different clusters)'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)