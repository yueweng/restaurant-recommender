import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from methods import get_restaurants_df, get_users_df, get_reviews_df, get_reviews_cond_df
from nltk.corpus import stopwords
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk
from sklearn.feature_extraction.text import CountVectorizer

def get_ratings_df(users_df, ratings_df):
  ratings_df = pd.DataFrame({'userid': reviews_df['userid'], 'restaurant_id': reviews_df['restaurant_id'], 'stars': reviews_df['stars']})
  return ratings_df

def cosine_similarity_recommendations(restaurants_df, title='Noosh', n=10):
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
  recommendation_list = []
  for ind in indices:
    if ind != index:
      recommendation_list.append(restaurants_df.iloc[ind]['title'])
  return recommendation_list

# def get_list_reviews(reviews_df, title='Noosh', n=10):
#   res_df = reviews_df.groupby('restaurant_id').agg({"userid": "count"})[5:].reset_index()
#   nltk.download('words')
#   words = set(nltk.corpus.words.words())

#   stopwords_ = set(stopwords.words('english'))
#   punctuation_ = set(string.punctuation)

#   def filter_tokens(sent):
#     return([w for w in sent if not w in stopwords_ and not w in punctuation_])

#   rest_id = res_df['restaurant_id'].unique()
#   reviews_condensed = {}
#   print(len(rest_id))
#   for idx, i in enumerate(rest_id):
#       rst_df = reviews_df[reviews_df['restaurant_id'] == i]
#       re = []
#       print("Index {}: {}".format(idx, i))
#       for idx, row in rst_df.iterrows():
#           sent_tokens = sent_tokenize(row['review'])
#           tokens = [sent for sent in map(word_tokenize, sent_tokens)]
#           tokens_lower = [[word.lower() for word in sent]
#                    for sent in tokens]
#           tokens_filtered = list(map(filter_tokens, tokens_lower))
#           for sent in tokens_filtered:
#               for w in sent:
#                   if len(w) >= 4:
#                       re.append(w)
#       res = " ".join(set(re))
#       reviews_condensed[i] = res
#   return reviews_condensed

def reviews_recommender(reviews_df, reviews_condensed_df, title='Noosh', n=10):  
  corpus = reviews_condensed_df['reviews'].fillna('')

  tf = CountVectorizer()

  document_tf_matrix = tf.fit_transform(corpus)

  doc_sim = cosine_similarity(document_tf_matrix, document_tf_matrix)

  restid = restaurants_df[restaurants_df['title'] == title]['_id'].values[0]
  gein = reviews_condensed_df[reviews_condensed_df['restaurant_id'] == restid].index
  all_indices = doc_sim[gein][0].argsort()[::-1][:n+1]
  res = []
  for ind in all_indices:
      if ind != gein:
          ind_res_id = reviews_condensed_df.iloc[ind]['restaurant_id']
          res.append(restaurants_df[restaurants_df['_id'] == ind_res_id]['title'].values[0])

  return res

def description_recommender(restaurants_df, title='Noosh', n=10):
  desc_restaurants_df = restaurants_df[restaurants_df['description'] != ' ']
  corpus_desc = desc_restaurants_df['description']

  tf = CountVectorizer()

  desc_matrix = tf.fit_transform(corpus_desc)
  desc_sim = cosine_similarity(desc_matrix, desc_matrix)

  rest_descid = restaurants_df[restaurants_df['title'] == title]['_id'].values[0]
  desc_in = desc_restaurants_df[desc_restaurants_df['_id'] == rest_descid].index
  all_descs = desc_sim[desc_in][0].argsort()[::-1][:n+1]
  
  res_desc = []
  for ind in all_descs:
      if ind != desc_in:
          ind_res_id = desc_restaurants_df.iloc[ind]['_id']
          res_desc.append(restaurants_df[restaurants_df['_id'] == ind_res_id]['title'].values[0])
  return res_desc

n = 20
restaurants_df = get_restaurants_df()
users_df = get_users_df()
reviews_df = get_reviews_df()
reviews_condensed_df = get_reviews_cond_df()
ratings_df = get_ratings_df(users_df, reviews_df)
title = input("Enter a Restaurant:")
print("                          ")
print("Recommender 1 Result: ")
print("---------------------------")
print(cosine_similarity_recommendations(restaurants_df, title, n))
print("                          ")
print("Recommender 2 Result: ")
print("---------------------------")
print(reviews_recommender(reviews_df, reviews_condensed_df, title, n))
print("                          ")
print("Recommender 3 Result: ")
print("---------------------------")
print(description_recommender(restaurants_df, title, n))

