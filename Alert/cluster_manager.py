from sklearn.cluster import MiniBatchKMeans
import numpy as np

class ClusterManager:
    """
    Manages streaming cluster assignment using MiniBatchKMeans.
    Supports incremental learning and real-time cluster assignment.
    """
    
    def __init__(self, n_clusters=7, batch_size=10):
        """
        Initialize the cluster manager.
        
        Args:
            n_clusters (int): Number of clusters to maintain
            batch_size (int): Batch size for mini-batch updates
        """
        self.n_clusters = n_clusters
        self.batch_size = batch_size
        self.model = MiniBatchKMeans(
            n_clusters=n_clusters,
            batch_size=batch_size,
            n_init=10,
            random_state=42
        )
        self.is_fitted = False
        self.sample_buffer = []
        self.init_samples = []
        
    def add_initial_sample(self, embedding):
        """
        Add samples for initial training before going live.
        
        Args:
            embedding (np.ndarray): Input embedding vector
        """
        self.init_samples.append(embedding)
        
    def initialize(self):
        """
        Initialize the model with collected seed samples.
        Must be called after adding at least n_clusters samples.
        """
        if len(self.init_samples) < self.n_clusters:
            raise ValueError(
                f"Need at least {self.n_clusters} samples to initialize. "
                f"Got {len(self.init_samples)}"
            )
        
        # Fit the model with initial samples
        init_data = np.vstack(self.init_samples)
        self.model.fit(init_data)
        self.is_fitted = True
        self.init_samples = []  # Clear to free memory
        
    def assign_cluster(self, embedding):
        """
        Assign an embedding to the nearest cluster.
        Uses partial_fit for incremental learning.
        
        Args:
            embedding (np.ndarray): Input embedding vector
            
        Returns:
            int: Cluster ID
        """
        if not self.is_fitted:
            raise RuntimeError(
                "ClusterManager not initialized. Call initialize() first."
            )
        
        # Add to buffer for batch training
        self.sample_buffer.append(embedding)
        
        # Perform partial fit when buffer reaches batch size
        if len(self.sample_buffer) >= self.batch_size:
            batch = np.vstack(self.sample_buffer)
            self.model.partial_fit(batch)
            self.sample_buffer = []
        
        # Predict cluster
        cluster_id = self.model.predict(embedding)[0]
        return cluster_id
    
    def get_cluster_centers(self):
        """
        Returns current cluster centers.
        
        Returns:
            np.ndarray: Cluster centers
        """
        if self.is_fitted:
            return self.model.cluster_centers_
        return None
