import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds

def get_restaurants_df():
  """
    Get restaurants dataframe from csv file
    
    Parameters
    ----------
    None
    

    Returns
    -------
    restaurants_df: DataFrame
    
  """
  restaurants_df = pd.read_csv('data/restaurants.csv')
  restaurants_df.drop(columns=['Unnamed: 0'], inplace=True)
  return restaurants_df

def get_users_df():
  """
    Get users dataframe from csv file
    
    Parameters
    ----------
    None
    

    Returns
    -------
    users_df: DataFrame
    
  """
  users_df = pd.read_csv('data/users.csv')
  users_df.drop(columns=['Unnamed: 0'], inplace=True)
  return users_df

def get_reviews_df():
  """
    Get reviews dataframe from csv file
    
    Parameters
    ----------
    None
    

    Returns
    -------
    reviews_df: DataFrame
    
  """
  reviews_df = pd.read_csv('data/reviews.csv', encoding='utf-8', engine='python')
  reviews_df.drop(columns=['Unnamed: 0'], inplace=True)
  return reviews_df

def get_ratings_df(users_df, ratings_df):
  ratings_df = pd.DataFrame({'userid': reviews_df['userid'], 'restaurant_id': reviews_df['restaurant_id'], 'stars': reviews_df['stars']})
  return ratings_df

def cosine_similarity_recommendations(restaurants_df, title='Noosh'):
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
  
  indices = cos_sim[index][0].argsort()[::-1][:11]
  recommendation_list = []
  for ind in indices:
    if ind != index:
      recommendation_list.append(restaurants_df.iloc[ind]['title'])
  return recommendation_list

# def get_predictions(restaurants_df, users_df):
#   restaurants_name_df = pd.DataFrame({'id': restaurants_df['_id'], 'title': restaurants_df['title']})
#   users_name_df = pd.DataFrame({'userid': users_df['userid'], 'name': users_df['name']})

#   combine_df = ratings_df.merge(restaurants_name_df, left_on='restaurant_id', right_on='id')
#   combine_df = combine_df.merge(users_name_df, left_on='userid', right_on='userid')
#   combine_df.drop(columns=['id'], inplace=True)

#   ratings_matrix = combine_df.pivot_table(index='userid', columns='title', values='stars').fillna(0)
#   u, s, vt = svds(ratings_matrix, 10)
#   sigma = np.diag(s)
#   predictions = u @ sigma @ vt

# def collaborative_filtering_recommendations(users_df, ratings_df, restaurants_df, predictions):
#   for idx, row in users_df.iterrows():
#     remove_ids = []
#     print("{} Recommendations".format(row['name']))
#     print("----------------------------------")
#     reviews_by_user = ratings_df[ratings_df['userid'] == row['userid']]
#     for jdx, row in reviews_by_user.iterrows():
#         rest_row = restaurants_df[restaurants_df['_id'] == row['restaurant_id']]
#         remove_ids.append(rest_row.index)
#         print("{} has a rating of {}".format(rest_row['title'].values[0], row['stars']))
#     print("----------------------------------")
#     pred = predictions[idx]
#     for i in remove_ids:
#         pred = np.delete(pred, i)
# #     print(pred.argsort())
# #     print(pred)
# #     print(len(pred))
#     print(pred)
#     print(pred.argsort()[-10:][::-1])
#     break
#     index = pred.argsort()[-10:][::-1]

#     for ind in index:
#         print(sub_ratings_matrix.columns.to_list()[ind])
#     print("                                ")

restaurants_df = get_restaurants_df()
users_df = get_users_df()
reviews_df = get_reviews_df()
ratings_df = get_ratings_df(users_df, reviews_df)
print(cosine_similarity_recommendations(restaurants_df))
