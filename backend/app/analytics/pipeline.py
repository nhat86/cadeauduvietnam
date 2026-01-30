from .loader import load_interactions
from .features import apply_weights
from .recommender import build_matrix, compute_similarity, recommend


def run_recommendation(user_id):
    df = load_interactions()
    df = apply_weights(df)


    matrix = build_matrix(df)
    similarity = compute_similarity(matrix)


    return recommend(user_id, matrix, similarity)