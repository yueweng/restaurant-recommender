import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from methods import get_restaurants_df, \
                    get_users_df, \
                    get_reviews_df, \
                    get_reviews_cond_df, \
                    get_all_restaurant_names, \
                    get_doc_sim, \
                    get_desc_sim
from nltk.corpus import stopwords
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk
from sklearn.feature_extraction.text import CountVectorizer

def get_ratings_df(users_df, ratings_df):
  ratings_df = pd.DataFrame({'userid': reviews_df['userid'], 'restaurant_id': reviews_df['restaurant_id'], 'stars': reviews_df['stars']})
  return ratings_df

def cosine_similarity_recommendations(restaurants_df, title='Noosh', n=12):
  """
    Calculate the cosine similarity and return the top n recommendations
    
    Parameters
    ----------
    restaurants_df: DataFrame
    title: String

    Returns
    -------
    None
    
  """
  cui = restaurants_df['cuisines'].str.split(", ")
  cuisines_dummies = pd.get_dummies(cui.apply(pd.Series).stack()).sum(level=0)
  condensed_df = pd.DataFrame({'price': restaurants_df['price'], 'stars': restaurants_df['stars']})
  condensed_df.fillna(0, inplace=True)

  sim_df = pd.concat([cuisines_dummies, condensed_df], axis=1)
  cos_sim = cosine_similarity(sim_df, sim_df)

  print("Restaurant: {}".format(title))

  index = restaurants_df[restaurants_df['title'] == title].index
  
  indices = cos_sim[index][0].argsort()[::-1][:n+1]
  selected_df = restaurants_df[(restaurants_df.index.isin(indices)) & ~(restaurants_df.index.isin(index))]
  return selected_df

def reviews_recommender(restaurants_df, reviews_df, reviews_condensed_df, doc_sim, title='Noosh', n=12):  
  restid = restaurants_df[restaurants_df['title'] == title]['_id'].values[0]
  gein = reviews_condensed_df[reviews_condensed_df['restaurant_id'] == restid].index
  all_indices = doc_sim[gein][0].argsort()[::-1][:n+1]
  recommendation_list = []
  for ind in all_indices:
      if ind != gein:
          recommendation_list.append(reviews_condensed_df.iloc[ind]['restaurant_id'])

  selected_df = restaurants_df[(restaurants_df.index.isin(all_indices)) & ~(restaurants_df.index.isin(gein))]
  return selected_df

def description_recommender(restaurants_df, desc_sim, title='Noosh', n=12):
  desc_restaurants_df = restaurants_df[restaurants_df['description'] != ' ']

  rest_descid = restaurants_df[restaurants_df['title'] == title]['_id'].values[0]
  desc_in = desc_restaurants_df[desc_restaurants_df['_id'] == rest_descid].index
  all_descs = desc_sim[desc_in][0].argsort()[::-1][:n+1]
  
  recommendation_list = []
  for ind in all_descs:
      if ind != desc_in:
          recommendation_list.append(desc_restaurants_df.iloc[ind]['_id'])
  selected_df = restaurants_df[(restaurants_df.index.isin(all_descs)) & ~(restaurants_df.index.isin(desc_in))]

  return selected_df

# n = 20
# restaurants_df = get_restaurants_df()
# users_df = get_users_df()
# reviews_df = get_reviews_df()
# reviews_condensed_df = get_reviews_cond_df()
# ratings_df = get_ratings_df(users_df, reviews_df)
# print("                          ")
# print("Recommender 1 Result: ")
# print("---------------------------")
# print(cosine_similarity_recommendations(restaurants_df))
# print("                          ")
# print("Recommender 2 Result: ")
# print("---------------------------")
# print(reviews_recommender(restaurants_df, reviews_df, reviews_condensed_df))
# print("                          ")
# print("Recommender 3 Result: ")
# print("---------------------------")
# print(description_recommender(restaurants_df))

