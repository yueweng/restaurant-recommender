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

def cosine_similarity_recommendations(restaurants_df, title='Noosh', n=12):
  """
    Calculate the cosine similarity and return the top n recommendations
    
    Parameters
    ----------
    restaurants_df: DataFrame
    title: String
    n: Top n recommendations

    Returns
    -------
    selected_df: DataFrame
    
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
  """
    Calculate the cosine similarity based on reviews and return the top n recommendations
    
    Parameters
    ----------
    restaurants_df: DataFrame
    reviews_df: DataFrame
    reviews_condensed_df: DataFrame
    doc_sim: Numpy Array
    title: String
    n: Number of Recommendations

    Returns
    -------
    selected_df: DataFrame
    
  """
  restid = restaurants_df[restaurants_df['title'] == title]['_id'].values[0]
  gein = reviews_condensed_df[reviews_condensed_df['restaurant_id'] == restid].index
  if gein.any():
    all_indices = doc_sim[gein][0].argsort()[::-1][:n+1]

    selected_df = restaurants_df[(restaurants_df.index.isin(all_indices)) & ~(restaurants_df.index.isin(gein))]
    return selected_df
  else:
    return pd.DataFrame()

def description_recommender(restaurants_df, desc_sim, title='Noosh', n=12):
  """
    Calculate the cosine similarity from restaurant descriptions and return the top n recommendations
    
    Parameters
    ----------
    restaurants_df: DataFrame
    desc_sim: Numpy Array
    title: String
    n: Top n recommendations

    Returns
    -------
    selected_df: DataFrame
    
  """
  rest_descid = restaurants_df[restaurants_df['title'] == title]['_id'].values[0]
  desc_in = restaurants_df[restaurants_df['_id'] == rest_descid].index
  if desc_in.any():
    all_descs = desc_sim[desc_in][0].argsort()[::-1][:n+1]
    
    selected_df = restaurants_df[(restaurants_df.index.isin(all_descs)) & ~(restaurants_df.index.isin(desc_in))]

    return selected_df
  else:
    return pd.DataFrame()

# text = input("Enter a Restaurant: ")
# restaurants_df = get_restaurants_df()
# reviews_condensed_df = get_reviews_cond_df()
# reviews_df = get_reviews_df()
# doc_sim = get_doc_sim()
# desc_sim = get_desc_sim()
# df1 = cosine_similarity_recommendations(restaurants_df, title=text, n=12)
# df2 = reviews_recommender(restaurants_df, reviews_df, reviews_condensed_df, doc_sim, title=text)
# df3 = description_recommender(restaurants_df, desc_sim, title=text)
# recommended_df = pd.concat([df1[:1], df2[:1], df3[:1]])