from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

df = pd.read_csv("final.csv")

df = df[df["soup"].notna()]
count = CountVectorizer(stop_words = "english")
count_matrix = count.fit_transform(df["soup"])

cosin_sim = cosine_similarity(count_matrix, count_matrix)

df = df.reset_index()

indices = pd.Series(df.index, index = df["original_title"])

def get_recommendation(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosin_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df[["original_title", "vote_count", "vote_average", "poster_link", "release_date", "overview", "runtime"]].iloc[movie_indices].values.tolist()
