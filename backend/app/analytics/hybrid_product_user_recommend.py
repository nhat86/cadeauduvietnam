# hybrid_recommender.py

import pandas as pd

class HybridProductUserRecommender:
    def __init__(self, user_rec, product_rec, alpha=0.5):
        """
        user_rec: UserBasedRecommender (đã fit)
        product_rec: ProductBasedRecommender (đã fit)
        alpha: trọng số user-based
        """
        self.user_rec = user_rec
        self.product_rec = product_rec
        self.alpha = alpha

    def recommend(self, user_id, k=5):
        # --- USER-BASED PART ---
        user_based_items = self._user_based_scores(user_id)

        # --- PRODUCT-BASED PART ---
        product_based_items = self._product_based_scores(user_id)

        # --- MERGE ---
        all_items = set(user_based_items) | set(product_based_items)
        final_scores = {}

        for item in all_items:
            u_score = user_based_items.get(item, 0.0)
            p_score = product_based_items.get(item, 0.0)

            final_scores[item] = (
                self.alpha * u_score +
                (1 - self.alpha) * p_score
            )

        # --- SORT & TOP-K ---
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        recommendations = [item for item, score in ranked[:k]]

        print("User-based scores:", user_based_items)
        print("Product-based scores:", product_based_items)
        print("Final hybrid scores:", final_scores)
        print("Top-k hybrid:", recommendations)

        return recommendations

    # =========================
    # INTERNAL METHODS
    # =========================

    def _user_based_scores(self, user_id):
        """
        Trả về dict: {product_id: score}
        """
        similar_users = self.user_rec.get_top_k_similar(
            user_id, k=10, kind="user"
        )

        user_products = set(
            self.user_rec.interactions[
                self.user_rec.interactions["user_id"] == user_id
            ]["product_id"]
        )

        user_ids_similar = [int(u[0]) for u in similar_users]

        candidate_interactions = self.user_rec.interactions[
            self.user_rec.interactions["user_id"].astype(int).isin(user_ids_similar)
        ]

        candidate_interactions = candidate_interactions[
            ~candidate_interactions["product_id"].isin(user_products)
        ]

        scores = (
            candidate_interactions
            .groupby("product_id")["score"]
            .sum()
        )

        return scores.to_dict()

    def _product_based_scores(self, user_id):
        """
        Trả về dict: {product_id: predicted_score}
        """
        user_products = self.product_rec.interactions[
            self.product_rec.interactions['user_id'] == user_id
        ]['product_id'].astype(int).tolist()

        if not user_products:
            return {}

        all_products = set(self.product_rec.product_user_matrix.index.astype(int))
        products_to_score = all_products - set(user_products)

        scores = {}

        for product in products_to_score:
            total_score = 0.0
            for purchased in user_products:
                sim = self.product_rec.similarity_product.loc[product, purchased]

                purchased_score = self.product_rec.interactions[
                    (self.product_rec.interactions['user_id'] == user_id) &
                    (self.product_rec.interactions['product_id'] == purchased)
                ]['score'].sum()

                total_score += sim * purchased_score

            scores[product] = total_score

        return scores
