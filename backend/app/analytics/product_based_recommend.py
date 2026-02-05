import pandas as pd
from .recommender_base import RecommenderBase

class ProductBasedRecommender(RecommenderBase):
    def __init__(self, interactions_df):
        super().__init__(interactions_df)
        self.product_user_matrix = self.interactions.pivot_table(index='product_id', columns='user_id', values='score').fillna(0)

    def fit(self):
        self.compute_cosine_similarity(self.product_user_matrix, kind="product")

    def recommend(self, product_id, k=5):
        similar_products = self.get_top_k_similar(product_id, k=k, kind="product")
        return similar_products
