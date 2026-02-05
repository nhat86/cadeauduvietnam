import pandas as pd
from .user_based_recommend import UserBasedRecommender
from .product_based_recommend import ProductBasedRecommender


class HybridProductUserRecommender:
    def __init__(self, interactions_df, alpha=0.5):
        """
        alpha: trọng số user-based
        (1 - alpha): trọng số product-based
        """
        self.alpha = alpha
        self.user_rec = UserBasedRecommender(interactions_df)
        self.product_rec = ProductBasedRecommender(interactions_df)
        self.interactions = interactions_df

    def fit(self):
        self.user_rec.fit()
        self.product_rec.fit()

    def recommend(self, user_id, k=5):
        """
        Trả về top-k product cho user
        """

        # 1️⃣ User-based: user giống user nào
        similar_users = self.user_rec.get_top_k_similar(user_id, k=10)

        user_based_scores = {}
        for sim_user_id, sim_score in similar_users:
            user_products = self.interactions[
                self.interactions["user_id"] == sim_user_id
            ]
            for _, row in user_products.iterrows():
                pid = row["product_id"]
                user_based_scores[pid] = user_based_scores.get(pid, 0) + sim_score * row["score"] #predicted_score(item) = Σ (similarity(user, other_user) × interaction_score)


        # 2️⃣ product-based: product user đã tương tác
        user_products = self.interactions[
            self.interactions["user_id"] == user_id
        ]

        product_based_scores = {}
        for _, row in user_products.iterrows():
            product_id = row["product_id"]
            similar_products = self.product_rec.get_top_k_similar(product_id, k=10)
            for sim_product_id, sim_score in similar_products:
                product_based_scores[sim_product_id] = product_based_scores.get(sim_product_id, 0) + sim_score * row["score"]

        # 3️⃣ Kết hợp hybrid
        hybrid_scores = {}

        all_products = set(user_based_scores.keys()) | set(product_based_scores.keys())
        for product_id in all_products:
            u_score = user_based_scores.get(product_id, 0)
            i_score = product_based_scores.get(product_id, 0)
            hybrid_scores[product_id] = self.alpha * u_score + (1 - self.alpha) * i_score

        # 4️⃣ Sort & top-k
        ranked_products = sorted(
            hybrid_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked_products[:k]
