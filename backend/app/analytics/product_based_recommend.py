import pandas as pd
from .recommender_base import RecommenderBase

class ProductBasedRecommender(RecommenderBase):
    def __init__(self, interactions_df):
        super().__init__(interactions_df)

        # product × user matrix
        self.product_user_matrix = (
            self.interactions
            .pivot_table(index='product_id', columns='user_id', values='score')
            .fillna(0)
        )

    def fit(self):
        # compute product-product similarity
        self.compute_cosine_similarity(self.product_user_matrix, kind="product")
        self.similarity_product = pd.DataFrame(
            self.sim_matrix,
            index=self.product_user_matrix.index,
            columns=self.product_user_matrix.index
        )

    def recommend(self, user_id, k=5):
        """
        Recommend top-k products for a specific user using item-based method.
        """
        # 1️⃣ Lấy các sản phẩm user đã mua
        user_products = self.interactions[
            self.interactions['user_id'] == user_id
        ]['product_id'].astype(int).tolist()

        if not user_products:
            return []  # user chưa mua sản phẩm nào

        # 2️⃣ Lấy tất cả sản phẩm chưa mua
        all_products = set(self.product_user_matrix.index.astype(int))
        products_to_score = all_products - set(user_products)

        # 3️⃣ Tính điểm dự đoán cho từng sản phẩm chưa mua
        predicted_scores = {}
        for product in products_to_score:
            score = 0.0
            for purchased in user_products:
                # lấy similarity giữa sản phẩm mới và từng sản phẩm đã mua
                sim = self.similarity_product.loc[product, purchased]
                # cộng điểm theo score gốc của sản phẩm đã mua
                purchased_score = self.interactions[
                    (self.interactions['user_id'] == user_id) &
                    (self.interactions['product_id'] == purchased)
                ]['score'].sum()
                score += sim * purchased_score
            predicted_scores[product] = score

        # 4️⃣ Sắp xếp và lấy top-k
        recommended = sorted(predicted_scores.items(), key=lambda x: x[1], reverse=True)
        top_k = [p for p, s in recommended[:k]]
        print("Initialized product-user matrix:\n", self.product_user_matrix)
        print("Product-product similarity matrix:\n", self.similarity_product)
        print(f"User {user_id} products:", user_products)
        print(f"Products to score for user {user_id}:", products_to_score)
        print(f"Predicted scores for user {user_id}:", predicted_scores)
        print(f"Top-{k} recommendations for user {user_id}:", top_k)
        return top_k
