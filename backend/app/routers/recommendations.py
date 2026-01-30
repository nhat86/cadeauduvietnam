from fastapi import APIRouter
from app.analytics.pipeline import run_recommendation


router = APIRouter()


@router.get("/recommendations/{user_id}")
def get_recommendations(user_id: int):
    return {
        "user_id": user_id,
        "recommended_products": run_recommendation(user_id)
    }