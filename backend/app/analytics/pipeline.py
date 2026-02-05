from .loader import load_interactions
from .features import apply_weights
from .user_based_recommend import UserBasedRecommender
from .product_based_recommend import ProductBasedRecommender
from .hybrid_product_user_recommend import HybridProductUserRecommender


def run_recommendation(user_id, mode="hybrid", k=5):
    # 1️⃣ Load data
    df = load_interactions()

    # 2️⃣ Feature engineering
    df = apply_weights(df)

    # 3️⃣ Init model
    if mode == "user":
        model = UserBasedRecommender(df)
    elif mode == "product":
        model = ProductBasedRecommender(df)
    elif mode == "hybrid":
        model = HybridProductUserRecommender(df)
    else:
        raise ValueError("Mode must be: user | product | hybrid")

    # 4️⃣ Train (fit)
    model.fit()

    # 5️⃣ Recommend
    return model.recommend(user_id, k=k)
