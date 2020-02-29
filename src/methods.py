import pandas as pd
import sys
import csv

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
  reviews_condensed_df = pd.read_csv('data/reviews_cond.csv', encoding='utf-8', engine='python')
  reviews_condensed_df.drop(columns=['Unnamed: 0'], inplace=True)
  return reviews_condensed_df

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