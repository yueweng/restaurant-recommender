import pymongo
from pymongo import MongoClient
import pandas as pd

"""
  This script gets the data from MongoDB 
  and store the data in a csv format
"""

def convert_db_data_to_csv():
  user_reviews, restaurants = extract_data_from_db()
  save_restaurants_csv(restaurants)
  save_user_reviews_csv(user_reviews)

def extract_data_from_db():
  """""
    Get the data from Mongo and store it as a variable
    
    Parameters
    ----------
    None
    

    Returns
    -------
    users: collection from MongoDB
    restaurants: collection from MongoDB
    
  """
  client = MongoClient('localhost', 27017)
  yelp = client['yelp']
  restaurants = yelp['restaurants']
  processed = yelp['processed']
  users = yelp['users']

  return users, restaurants

def save_restaurants_csv(restaurants):
  """""
    Save restaurant collection into a csv file
    
    Parameters
    ----------
    restaurants: collection
    

    Returns
    -------
    None
    
  """
  # convert into dataframe
  restaurants_df = pd.DataFrame(list(restaurants.find()))
  # remove duplicate restaurants
  restaurants_df.drop_duplicates(inplace=True)
  # store into csv
  print("Saving restaurants dataframe into csv format!")
  restaurants_df.to_csv('data/restaurants.csv', ",")
  print("Saved!")

def save_user_reviews_csv(user_reviews):
   """""
    Save users, reviews collection into a csv file
    
    Parameters
    ----------
    user_reviews: collection
    

    Returns
    -------
    None
    
  """

  # convert into dataframe
  user_reviews_df = pd.DataFrame(list(users.find()))
  # break up dataframe into users table and reviews table
  users_df = get_users_dataframe(user_reviews_df)
  reviews_df = get_reviews_dataframe(user_reviews_df)
  # remove duplicate restaurants
  restaurants_df.drop_duplicates(inplace=True)
  # store into csv
  print("Saving restaurants dataframe into csv format!")
  restaurants_df.to_csv('data/restaurants.csv', ",")
  print("Saved!")

def get_users_dataframe(user_reviews_df):
  """""
    Get users dataframe from user_reviews dataframe
    
    Parameters
    ----------
    user_reviews: DataFrame
    

    Returns
    -------
    users: DataFrame
  """

  user_att = ['userid', 'name', 'url', 'city', 'state', 'friends', 'reviews', 'photos']
  user = {}
  for att in user_att:
      user[att] = user_reviews_df[att]

  users_df = pd.DataFrame(user)
  users_df.drop_duplicates(inplace=True)
  return users_df

def get_reviews_dataframe(user_reviews_df):
  """""
    Get reviews dataframe from user_reviews dataframe
    
    Parameters
    ----------
    user_reviews: DataFrame
    

    Returns
    -------
    reviews: DataFrame
  """

  reviews_att = ['userid', 'restaurant_id', 'review', 'date', 'stars', 'Useful', 'Funny', 'Cool']
  reviews = {}
  for att in reviews_att:
      reviews[att] = user_reviews_df[att]


  reviews_df = pd.DataFrame(reviews)

  return reviews_df

convert_db_data_to_csv()