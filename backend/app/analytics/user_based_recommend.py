# user_based.py

import pandas as pd
from .recommender_base import RecommenderBase

class UserBasedRecommender(RecommenderBase):

    def __init__(self, interactions_df):
        super().__init__(interactions_df)

        # user × product matrix
        self.user_product_matrix = (
            self.interactions
            .pivot_table(
                index="user_id",
                columns="product_id",
                values="score",
                aggfunc="sum"
            )
            .fillna(0)
        )

    def fit(self):
        # compute user-user similarity
        self.compute_cosine_similarity(
            self.user_product_matrix,
            kind="user"
        )

    def recommend(self, user_id, k=5):
        """
        k : số sản phẩm đề xuất
        """

        # 1️⃣ user giống nhất
        similar_users = self.get_top_k_similar(
            user_id,
            k=10, # số user tương tự
            kind="user"
        )

        # 2️⃣ sản phẩm user hiện tại đã tương tác
        user_products = set(
            self.interactions[
                self.interactions["user_id"] == user_id
            ]["product_id"]
        )

        # 3️⃣ interactions của user tương tự
        user_ids_similar = [int(u[0]) for u in similar_users]
        candidate_interactions = self.interactions[
        self.interactions["user_id"].astype(int).isin(user_ids_similar)
]


        # 4️⃣ loại bỏ sản phẩm đã mua
        candidate_interactions = candidate_interactions[
            ~candidate_interactions["product_id"].isin(user_products)
        ]

        # 5️⃣ gộp & rank sản phẩm
        recommendations = (
            candidate_interactions
            .groupby("product_id")["score"]
            .sum()
            .sort_values(ascending=False)
            .head(k)
            .index
            .tolist()
        )
        print("User-product matrix:\n", self.user_product_matrix)
        print("Similar users:", similar_users)
        print("User products:", user_products)
        print("Candidate interactions:\n", candidate_interactions)

        return recommendations

