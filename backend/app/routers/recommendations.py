from fastapi import APIRouter, Query
from app.analytics.pipeline import run_recommendation

router = APIRouter()


@router.get("/recommendations/{user_id}")
def get_recommendations(
    user_id: int,
    mode: str = Query("hybrid", enum=["user", "product", "hybrid"]),
    k: int = Query(5, ge=1)
):
    recommendations = run_recommendation(
        user_id=user_id,
        mode=mode,
        k=k
    )

    return {
        "user_id": user_id,
        "mode": mode,
        "recommended_products": recommendations
    }
