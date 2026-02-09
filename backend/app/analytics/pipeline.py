from .loader import load_interactions
from .features import apply_weights
from .user_based_recommend import UserBasedRecommender
from .product_based_recommend import ProductBasedRecommender
from .hybrid_product_user_recommend import HybridProductUserRecommender

def run_recommendation(user_id: int, mode: str, k: int = 5, alpha: float = 1):
    """
    Chạy recommender và trả về kết quả + metadata
    """
    # 1️⃣ Load data
    df = load_interactions()

    # 2️⃣ Feature engineering
    df = apply_weights(df)
    # 1️⃣ Tạo model user-based
    user_rec = UserBasedRecommender(df)
    user_rec.fit()

    # 2️⃣ Tạo model product-based
    product_rec = ProductBasedRecommender(df)
    product_rec.fit()

    if mode == "user":
        recs = user_rec.recommend(user_id, k)
        meta = {"strategy": "user-based"}

    elif mode == "product":
        recs = product_rec.recommend(user_id, k)
        meta = {"strategy": "product-based"}

    elif mode == "hybrid":
        hybrid_rec = HybridProductUserRecommender(
            user_rec=user_rec,
            product_rec=product_rec,
            alpha=alpha
        )
        recs = hybrid_rec.recommend(user_id, k)
        meta = {
            "strategy": "hybrid",
            "alpha": alpha
        }

        # fallback nếu hybrid không có kết quả
        if not recs:
            recs = product_rec.recommend(user_id, k)
            meta["strategy"] = "hybrid_fallback_product"

    else:
        raise ValueError(f"Invalid mode: {mode}")

    return recs, meta

