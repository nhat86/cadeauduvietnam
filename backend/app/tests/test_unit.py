# backend/app/tests/test_unit.py
import pytest
import pandas as pd

from app.analytics.user_based_recommend import UserBasedRecommender
from app.analytics.product_based_recommend import ProductBasedRecommender
from app.analytics.hybrid_product_user_recommend import HybridProductUserRecommender


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "user_id": [1, 1, 2, 2, 3, 3],
        "product_id": [100, 101, 100, 102, 101, 102],
        "score": [5, 1, 2, 1, 2, 5]
    })


def test_user_based(sample_data):
    recommender = UserBasedRecommender(
        interactions_df=sample_data
    )

    recommender.fit()

    recs = recommender.recommend(user_id=1, k=2)
    print("Recommendations for user 1:", recs)
    assert isinstance(recs, list)
    assert all(isinstance(r, int) for r in recs)

def test_product_based(sample_data):
    recommender = ProductBasedRecommender(
        interactions_df=sample_data
    )

    recommender.fit()

    recs = recommender.recommend(user_id=1, k=2)
    print("Recommendations for user 1:", recs)
    assert isinstance(recs, list)
    assert all(isinstance(r, int) for r in recs)

def test_hybrid_product_user(sample_data):
    user_rec = UserBasedRecommender(sample_data)
    user_rec.fit()

    product_rec = ProductBasedRecommender(sample_data)
    product_rec.fit()

    hybrid = HybridProductUserRecommender(
        user_rec=user_rec,
        product_rec=product_rec,
        alpha=0.5
    )

    recs = hybrid.recommend(user_id=1, k=2)

    assert isinstance(recs, list)
    assert len(recs) <= 2
    assert all(isinstance(r, int) for r in recs)
