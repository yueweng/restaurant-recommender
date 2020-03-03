import pandas as pd
import csv
from functools import lru_cache

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
  restaurants_df = pd.read_csv('https://restaurant-recommender-flask.s3.amazonaws.com/restaurants.csv')
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
  users_df = pd.read_csv('https://restaurant-recommender-flask.s3.amazonaws.com/users.csv', encoding='utf-8')
  users_df.drop(columns=['Unnamed: 0'], inplace=True)
  return users_df

@lru_cache(maxsize=32)
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
  reviews_df = pd.read_csv('https://restaurant-recommender-flask.s3.amazonaws.com/reviews.csv', encoding='utf-8', engine='python')
  reviews_df.drop(columns=['Unnamed: 0'], inplace=True)
  return reviews_df

def get_reviews_cond_df():
  """
    Get reviews condensed from csv file
    
    Parameters
    ----------
    None
    

    Returns
    -------
    reviews_condensed_df: DataFrame
    
  """
  reviews_condensed_df = pd.read_csv('https://restaurant-recommender-flask.s3.amazonaws.com/reviews_cond.csv', encoding='utf-8', engine='python')
  reviews_condensed_df.drop(columns=['Unnamed: 0'], inplace=True)
  return reviews_condensed_df

def get_doc_sim():
  """
    Get similarity matrix from csv file
    
    Parameters
    ----------
    None
    

    Returns
    -------
    doc_sim: Numpy Array
    
  """
  doc_sim_df = pd.read_csv('https://restaurant-recommender-flask.s3.amazonaws.com/doc_sim.csv', encoding='utf-8')
  doc_sim_df.drop(columns=['Unnamed: 0'], inplace=True)
  return doc_sim_df.to_numpy()

def get_desc_sim():
  """
    Get similarity matrix from csv file
    
    Parameters
    ----------
    None
    

    Returns
    -------
    desc_sim: Numpy Array
    
  """
  desc_sim_df = pd.read_csv('https://restaurant-recommender-flask.s3.amazonaws.com/desc_sim.csv', encoding='utf-8')
  desc_sim_df.drop(columns=['Unnamed: 0'], inplace=True)
  return desc_sim_df.to_numpy()

def create_dataframe(attributes, original_df):
  """""
    Convert a dataframe into a smaller dataframe with the attributes given
    
    Parameters
    ----------
    attributes: list
    original_df: DataFrame
    

    Returns
    -------
    df: DataFrame
  """
  dict_df = {}
  for att in attributes:
    dict_df[att] = original_df[att]

  df = pd.DataFrame(dict_df)
  return df

def get_all_restaurant_names(restaurants_df):
  return restaurants_df['title'].values.tolist()

