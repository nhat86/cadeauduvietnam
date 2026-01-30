from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def build_matrix(df):
    return df.pivot_table(
    index="user_id",
    columns="product_id",
    values="score",
    aggfunc="sum",
    fill_value=0
    )




def compute_similarity(matrix):
    sim = cosine_similarity(matrix)
    return pd.DataFrame(sim, index=matrix.index, columns=matrix.index)




def recommend(user_id, matrix, similarity, top_n=5):
    if user_id not in matrix.index:
        return []


    sim_users = similarity[user_id].drop(user_id).sort_values(ascending=False)
    similar_users = sim_users.head(3).index


    owned_products = set(matrix.loc[user_id][matrix.loc[user_id] > 0].index)


    scores = {}
    for u in similar_users:
        for product_id, score in matrix.loc[u].items():
            if score > 0 and product_id not in owned_products:
                scores[product_id] = scores.get(product_id, 0) + score


    return sorted(scores, key=scores.get, reverse=True)[:top_n]