# recommender_base.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class RecommenderBase:
    def __init__(self, interactions_df):
        """
        interactions_df: DataFrame với các cột ['user_id', 'product_id', 'score']
        """
        self.interactions = interactions_df
        self.sim_matrix = None
        self.id_to_index = {}
        self.index_to_id = {}

    def compute_cosine_similarity(self, matrix, kind="user"):
        """
        kind: "user" hoặc "item"
        """
        self.sim_matrix = cosine_similarity(matrix.values)
        ids = list(matrix.index)
        self.id_to_index = {id_: idx for idx, id_ in enumerate(ids)}
        self.index_to_id = {idx: id_ for idx, id_ in enumerate(ids)}

    def get_top_k_similar(self, entity_id, k=5, kind="user"):
        """
        entity_id: user_id hoặc product_id
        """
        if self.sim_matrix is None:
            raise ValueError("Bạn cần tính sim_matrix trước")
        if entity_id not in self.id_to_index:
         return []

        idx = self.id_to_index[entity_id]
        # giả sử entity_id là index trong matrix
        # Crée une liste de tuples (index, score) pour garder l'identifiant de chaque user/item.
        sim_scores = list(enumerate(self.sim_matrix[idx]))
        # Trie les tuples par score décroissant tout en conservant les index d'origine.
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # bỏ chính nó
        sim_scores = sim_scores[1:k+1]

        return [
            (self.index_to_id[i], score)
            for i, score in sim_scores
        ]
