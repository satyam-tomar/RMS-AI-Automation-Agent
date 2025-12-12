from datetime import datetime, timedelta
from collections import defaultdict, deque

class AlertManager:
    """
    Manages sliding time windows and threshold-based alerting
    for complaint clusters.
    """
    
    def __init__(self, window_minutes=10, threshold=3):
        """
        Initialize the alert manager.
        
        Args:
            window_minutes (int): Time window size in minutes
            threshold (int): Number of complaints to trigger alert
        """
        self.window_minutes = window_minutes
        self.threshold = threshold
        
        # Store complaints per cluster with timestamps
        # Structure: {cluster_id: deque([(timestamp, complaint_text), ...])}
        self.cluster_complaints = defaultdict(deque)
        
        # Track if alert was already triggered for a cluster
        self.alerted_clusters = set()
        
    def record_complaint(self, cluster_id, complaint_text):
        """
        Record a new complaint in the specified cluster.
        
        Args:
            cluster_id (int): Cluster identifier
            complaint_text (str): Complaint text
        """
        timestamp = datetime.now()
        self.cluster_complaints[cluster_id].append((timestamp, complaint_text))
        
    def _clean_old_complaints(self, cluster_id):
        """
        Remove complaints outside the sliding window.
        
        Args:
            cluster_id (int): Cluster identifier
        """
        cutoff_time = datetime.now() - timedelta(minutes=self.window_minutes)
        complaints = self.cluster_complaints[cluster_id]
        
        # Remove old entries from the left
        while complaints and complaints[0][0] < cutoff_time:
            complaints.popleft()
            
    def check_alert(self, cluster_id):
        """
        Check if alert threshold is met for the cluster.
        
        Args:
            cluster_id (int): Cluster identifier
            
        Returns:
            tuple: (alert_triggered: bool, alert_data: dict)
        """
        # Clean expired complaints
        self._clean_old_complaints(cluster_id)
        
        complaints = self.cluster_complaints[cluster_id]
        current_count = len(complaints)
        
        # Check if threshold is met
        if current_count >= self.threshold:
            # Extract recent complaint texts
            recent_complaints = [text for _, text in complaints]
            
            alert_data = {
                'count': current_count,
                'complaints': recent_complaints[-self.threshold:]
            }
            
            # Mark cluster as alerted (optional: can reset periodically)
            self.alerted_clusters.add(cluster_id)
            
            return True, alert_data
        
        return False, {}
    
    def get_cluster_counts(self):
        """
        Get current complaint counts per cluster within window.
        
        Returns:
            dict: {cluster_id: count}
        """
        counts = {}
        for cluster_id in self.cluster_complaints:
            self._clean_old_complaints(cluster_id)
            counts[cluster_id] = len(self.cluster_complaints[cluster_id])
        return counts
    
    def reset_alerts(self):
        """
        Reset all alert states. Useful for testing or periodic resets.
        """
        self.alerted_clusters.clear()