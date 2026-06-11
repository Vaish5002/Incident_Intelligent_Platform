"""
Embedding Service
Converts text into vector embeddings for similarity search
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from loguru import logger
import json


class EmbeddingService:
    """
    Service for generating and managing text embeddings
    
    Uses TF-IDF for lightweight, fast embeddings
    Can be upgraded to use sentence transformers or OpenAI embeddings later
    """
    
    def __init__(self, max_features: int = 1000):
        """
        Initialize embedding service
        
        Args:
            max_features: Maximum number of features for TF-IDF
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1
        )
        self.is_fitted = False
        self.model_name = "tfidf-sklearn"
        self.vocabulary_size = 0
        self.embedding_dim = max_features
        logger.info(f"Embedding service initialized with {max_features} features")
    
    def fit(self, texts: List[str]):
        """
        Fit the vectorizer on a corpus of texts
        
        Args:
            texts: List of texts to fit on
        """
        if texts:
            self.vectorizer.fit(texts)
            self.is_fitted = True
            self.vocabulary_size = len(self.vectorizer.vocabulary_)
            logger.info(f"Vectorizer fitted on {len(texts)} texts, vocabulary size: {self.vocabulary_size}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text
        
        Args:
            text: Input text
            
        Returns:
            List of floats representing the embedding vector (fixed dimension)
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return [0.0] * self.embedding_dim
            
            # If not fitted, fit on this single text
            if not self.is_fitted:
                self.vectorizer.fit([text])
                self.is_fitted = True
                self.vocabulary_size = len(self.vectorizer.vocabulary_)
            
            # Generate embedding
            embedding_matrix = self.vectorizer.transform([text])
            embedding_dense = embedding_matrix.toarray()[0]
            
            # Ensure fixed dimension
            result = [0.0] * self.embedding_dim
            for i in range(min(len(embedding_dense), self.embedding_dim)):
                result[i] = float(embedding_dense[i])
            
            logger.debug(f"Generated embedding of size {len(result)}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector on error
            return [0.0] * self.embedding_dim
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors (all same dimension)
        """
        try:
            if not texts:
                return []
            
            # Fit vectorizer if not fitted
            if not self.is_fitted:
                self.vectorizer.fit(texts)
                self.is_fitted = True
                self.vocabulary_size = len(self.vectorizer.vocabulary_)
            
            # Generate embeddings
            embedding_matrix = self.vectorizer.transform(texts)
            embeddings_dense = embedding_matrix.toarray()
            
            # Ensure all embeddings have fixed dimension
            results = []
            for embedding in embeddings_dense:
                result = [0.0] * self.embedding_dim
                for i in range(min(len(embedding), self.embedding_dim)):
                    result[i] = float(embedding[i])
                results.append(result)
            
            logger.info(f"Generated {len(results)} embeddings")
            return results
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [[0.0] * self.embedding_dim] * len(texts)
    
    def calculate_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1).reshape(1, -1)
            vec2 = np.array(embedding2).reshape(1, -1)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(vec1, vec2)[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_similar(
        self,
        query_embedding: List[float],
        candidate_embeddings: List[List[float]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find most similar embeddings from candidates
        
        Args:
            query_embedding: Query embedding vector
            candidate_embeddings: List of candidate embeddings
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries with index and similarity score
        """
        try:
            if not candidate_embeddings:
                return []
            
            # Calculate similarities
            query_vec = np.array(query_embedding).reshape(1, -1)
            candidate_matrix = np.array(candidate_embeddings)
            
            similarities = cosine_similarity(query_vec, candidate_matrix)[0]
            
            # Get top k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = [
                {
                    "index": int(idx),
                    "similarity": float(similarities[idx])
                }
                for idx in top_indices
                if similarities[idx] > 0  # Only return non-zero similarities
            ]
            
            logger.info(f"Found {len(results)} similar items")
            return results
            
        except Exception as e:
            logger.error(f"Error finding similar embeddings: {e}")
            return []
    
    def embed_incident(
        self,
        incident_description: str,
        logs: Optional[str] = None,
        rca_text: Optional[str] = None
    ) -> Dict[str, List[float]]:
        """
        Generate embeddings for different parts of an incident
        
        Args:
            incident_description: Incident description
            logs: Log data
            rca_text: RCA report text
            
        Returns:
            Dictionary with embeddings for each part
        """
        try:
            embeddings = {}
            
            # Embed incident description
            if incident_description:
                embeddings["incident"] = self.generate_embedding(incident_description)
            
            # Embed logs
            if logs:
                embeddings["logs"] = self.generate_embedding(logs)
            
            # Embed RCA
            if rca_text:
                embeddings["rca"] = self.generate_embedding(rca_text)
            
            # Create combined embedding
            if incident_description and logs:
                combined_text = f"{incident_description} {logs}"
                embeddings["combined"] = self.generate_embedding(combined_text)
            elif incident_description:
                embeddings["combined"] = embeddings["incident"]
            
            logger.info(f"Generated {len(embeddings)} embeddings for incident")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error embedding incident: {e}")
            return {}
    
    def save_to_json(self, embedding: List[float]) -> str:
        """
        Convert embedding to JSON string for storage
        
        Args:
            embedding: Embedding vector
            
        Returns:
            JSON string
        """
        return json.dumps(embedding)
    
    def load_from_json(self, json_str: str) -> List[float]:
        """
        Load embedding from JSON string
        
        Args:
            json_str: JSON string
            
        Returns:
            Embedding vector
        """
        try:
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error loading embedding from JSON: {e}")
            return []
    
    def get_embedding_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding model
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "is_fitted": self.is_fitted,
            "dimensions": self.embedding_dim,
            "vocabulary_size": self.vocabulary_size
        }


# Alternative: Sentence Transformer Embedding Service (for future upgrade)
class SentenceTransformerEmbeddingService:
    """
    Advanced embedding service using sentence transformers
    Uncomment and use this for better quality embeddings
    
    Requires: pip install sentence-transformers
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with sentence transformer model"""
        # from sentence_transformers import SentenceTransformer
        # self.model = SentenceTransformer(model_name)
        # self.model_name = model_name
        pass
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using sentence transformer"""
        # return self.model.encode(text).tolist()
        pass
