# user_based.py

import pandas as pd
from .recommender_base import RecommenderBase

class UserBasedRecommender(RecommenderBase):
    def __init__(self, interactions_df):
        super().__init__(interactions_df)
        self.user_product_matrix = self.interactions.pivot_table(index='user_id', columns='product_id', values='score',aggfunc="sum").fillna(0)

    def fit(self):
        self.compute_cosine_similarity(self.user_product_matrix, kind="user")

    def recommend(self, user_id, k=5):
        similar_users = self.get_top_k_similar(user_id, k=k, kind="user")
        return similar_users
