# ==============================================================================
# SafeX AI FAQ Chatbot - Similarity Engine (Skeleton)
# ==============================================================================
from typing import List, Tuple

class FAQSimilarityModel:
    """
    Fits representation vectors over FAQ questions and computes cosine similarity
    against incoming queries to identify closest matches.
    """
    def __init__(self):
        """
        TODO (Owner: Muhammad Faozan Mujtaba):
        - Initialize term vector representation settings (e.g., TF-IDF Vectorizer).
        """
        self.questions = []
        
    def fit(self, questions: List[str]):
        """
        Fits the similarity model on the FAQ questions list.

        Parameters:
            questions (List[str]): List of all FAQ questions.

        TODO (Owner: Muhammad Faozan Mujtaba):
        - Train/fit vectorizer on the database.
        - Create the reference embedding matrix.
        """
        # TODO: Implement fitting/indexing logic here
        pass
        
    def find_best_match(self, query: str) -> Tuple[int, float]:
        """
        Calculates cosine similarity and returns the best matching FAQ item.

        Parameters:
            query (str): Cleaned user input query.

        Returns:
            Tuple[int, float]: index of the matched question and its similarity score.

        TODO (Owner: Muhammad Faozan Mujtaba):
        - Transform user query to vector space.
        - Compute Cosine Similarity between query and reference matrix.
        - Return max score index and similarity score value.
        """
        # TODO: Implement similarity calculation logic here
        return 0, 0.0
