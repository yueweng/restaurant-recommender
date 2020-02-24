import pandas as pd
import matplotlib.pyplot as plt
from src.methods import create_dataframe

def get_restaurants_df():
  """""
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
  
def neighborhood_dynamics(restaurants_df):
  """""
    Plot Neighborhood Dynamics Graph
    
    Parameters
    ----------
    restaurants_df: DataFrame
    

    Returns
    -------
    None
    
  """
  neighborhood_group = restaurants_df.groupby('neighborhood').agg({'price': 'mean', 'stars': 'mean', 'reviewCount': 'sum', '_id': 'count'}).reset_index()
  neighborhood_group.sort_values(by=['reviewCount'], ascending=False, inplace=True)
  plot_neighborhood_popularity(neighborhood_group)

def plot_neighborhood_popularity(neighborhood_group, n=25):
  """""
    Plot Popularity of restaurants based on Neighborhood
    
    Parameters
    ----------
    neighborhood_group: DataFrame
    n: number of neighborhoods

    Returns
    -------
    None
    
  """
  top_n = neighborhood_group[:n]
  fig, ax = plt.subplots(figsize=[20, 10])
  
  top_n.sort_values('reviewCount', inplace=True)
  
  ax.barh(top_n['neighborhood'], top_n['reviewCount'])
  ax.set_title('Popularity of Restaurants broken down by Neighborhood', fontsize=20, pad=20)
  ax.set_xlabel('Number of Reviews', fontsize=20)
  ax.set_ylabel('Neighborhood', fontsize=20)
  
  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=20)

  plt.tight_layout()
  plt.savefig('images/popularity_neighborhood.png')

def plot_restaurant_ratings(restaurants_df):
  """""
    Plot Num of Restaurants based on Ratings of Restaurants
    
    Parameters
    ----------
    restaurants_df: DataFrame

    Returns
    -------
    None
    
  """
  reviews_group = restaurants_df.groupby('stars').agg({'_id': 'count', 'reviewCount': 'sum'}).reset_index().rename(columns={'_id': 'count'})
  fig, ax = plt.subplots(figsize=[20, 10])

  ax.bar(reviews_group['stars'], reviews_group['count'], width=0.4)
  ax.set_title('Popularity vs Ratings', fontsize=20, pad=20)
  ax.set_xlabel('Ratings', fontsize=20)
  ax.set_ylabel('Num of Reviews', fontsize=20)

  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=15)

  plt.savefig('images/restaurants_ratings.png')

def factors_overview(restaurants_df):
  """""
    Look into Different Factors and Plot Graph against Restaurants and Popularity
    
    Parameters
    ----------
    restaurants_df: DataFrame

    Returns
    -------
    None
    
  """
  s = restaurants_df['ambience'].str.split(", ")
  ambience_dummies, ambience_cols = get_ambience_info(s)
  rest_att = ['_id', 'title', 'price', 'stars', 'reviewCount']
  rest_condensed_df = create_dataframe(rest_att, restaurants_df)
  ambience_df = pd.concat([rest_condensed_df, ambience_dummies], axis=1)

  ambience_restaurants(ambience_cols, ambience_df)
  ambience_popularity(ambience_cols, ambience_df)
  noise_overview(restaurants_df, rest_condensed_df)
  alcohol_overview(restaurants_df, rest_condensed_df)
  
def ambience_restaurants(ambience_cols, ambience_df):
  """""
    Get count of restaurants with respective ambience and plot graph
    
    Parameters
    ----------
    ambience_cols: Index
    ambience_df: DataFrame

    Returns
    -------
    None
    
  """
  amb = {}
  for col in ambience_cols:
      column = col.strip()
      for k, v in ambience_df[column].value_counts().items():
          if k == 1.0:
              amb[column] = v
  amb_df = pd.DataFrame(list(amb.items()), columns=['Ambience', 'Count'])
  amb_df.sort_values(by=['Count'], ascending=False, inplace=True)
  plot_ambience_overview(amb_df)

def ambience_popularity(ambience_cols, ambience_df):
  """""
    Get count of reviews with respective ambience and plot grpah
    
    Parameters
    ----------
    ambience_cols: Index
    ambience_df: DataFrame

    Returns
    -------
    None
    
  """
  ar = {}
  for col in ambience_cols:
      amb_rev = ambience_df.groupby(col).agg({'reviewCount': 'sum'}).reset_index()
      ar[col] = amb_rev[amb_rev[col] == 1.0]['reviewCount'][1]
  ambrvco_df = pd.DataFrame(list(ar.items()), columns=['Ambience', 'Popularity'])
  ambrvco_df.sort_values(by=['Popularity'], ascending=False, inplace=True)
  plot_ambience_popularity(ambrvco_df)   

def get_ambience_info(s):
  """""
    Get Dummified Ambience Cols
    
    Parameters
    ----------
    s: pd Series

    Returns
    -------
    ambience_dummies: DataFrame
    ambience_cols: Index
    
  """
  ambience_dummies = pd.get_dummies(s.apply(pd.Series).stack()).sum(level=0)
  ambience_cols = ambience_dummies.columns
  return ambience_dummies, ambience_cols
    
def plot_ambience_overview(amb_df):
  """""
    Plot Ambience Breakdown vs Num of Restaurants
    
    Parameters
    ----------
    amb_df: DataFrame

    Returns
    -------
    None
    
  """
  fig, ax = plt.subplots(figsize=[20, 10])
  ax.bar(amb_df['Ambience'], amb_df['Count'])

  ax.set_title('Ambience Overview', fontsize=20, pad=20)
  ax.set_xlabel('Ambience', fontsize=20)
  ax.set_ylabel('Num of Restaurants', fontsize=20)

  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=15)

  plt.savefig('images/ambience_overview.png')

def plot_ambience_popularity(ambrvco_df):
  """""
    Plot Popularity of Restaurants based on Ambience
    
    Parameters
    ----------
    ambrvco_df: DataFrame

    Returns
    -------
    None
    
  """
  fig, ax = plt.subplots(figsize=[20, 10])
  ax.bar(ambrvco_df['Ambience'], ambrvco_df['Popularity'])

  ax.set_title('Ambience vs Popularity', fontsize=20, pad=20)
  ax.set_xlabel('Ambience', fontsize=20)
  ax.set_ylabel('Num of Reviews', fontsize=20)

  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=15)

  plt.savefig('images/ambience_popularity.png')

def noise_overview(restaurants_df, rest_condensed_df):
  """""
    Get review counts of restaurants with respective noise level and plot graph
    
    Parameters
    ----------
    restaurants_df: DataFrame
    rest_condensed_df: DataFrame

    Returns
    -------
    None
    
  """
  noise_dummies = pd.get_dummies(restaurants_df['noise_level'])
  noise_df = pd.concat([rest_condensed_df, noise_dummies], axis=1)
  noise_cols = noise_dummies.columns

  nl_df = noise_popularity(noise_cols, noise_df)
  plot_noise_popularity(nl_df)

def alcohol_overview(restaurants_df, rest_condensed_df):
  """""
    Get count of restaurants with respective alcohol value and plot graph
    
    Parameters
    ----------
    restaurants_df: DataFrame
    rest_condensed_df: DataFrame

    Returns
    -------
    None
    
  """
  alcohol_dummies = pd.get_dummies(restaurants_df['alcohol'])
  alcohol_df = pd.concat([rest_condensed_df, alcohol_dummies], axis=1)
  al_df = get_alcohol_popularity(restaurants_df, alcohol_df)
  plot_alcohol_popularity_graph(al_df)

def noise_popularity(noise_cols, noise_df):
  """""
    Get noise level dataframe
    
    Parameters
    ----------
    noise_cols: Index
    noise_df: DataFrame

    Returns
    -------
    nl_df: DataFrame
    
  """
  nl = {}
  for col in noise_cols:
      nl_rev = noise_df.groupby(col).agg({'reviewCount': 'sum'}).reset_index()
      nl[col] = nl_rev[nl_rev[col] == 1.0]['reviewCount'][1]

  nl_df = pd.DataFrame(list(nl.items()), columns=['Noise', 'Popularity'])
  nl_df.sort_values(by=['Noise'], inplace=True)

  return nl_df

def get_alcohol_popularity(restaurants_df, alcohol_df):
  """""
    Get alcohol dataframe from restaurants dataframe
    
    Parameters
    ----------
    restaurants_df: DataFrame
    alcohol_df: DataFrame

    Returns
    -------
    al_df: DataFrame
    
  """
  alcohol_dummies = pd.get_dummies(restaurants_df['alcohol'])
  alcohol_cols = alcohol_dummies.columns
  aldf = {}
  for col in alcohol_cols:
      al_rev = alcohol_df.groupby(col).agg({'reviewCount': 'sum'}).reset_index()
      aldf[col] = al_rev[al_rev[col] == 1.0]['reviewCount'][1]

  al_df = pd.DataFrame(list(aldf.items()), columns=['Alcohol', 'Popularity'])
  al_df.sort_values(by=['Alcohol'], inplace=True)
  return al_df

def plot_noise_popularity(nl_df):
  """""
    Plot Noise Level vs Num of Reviews
    
    Parameters
    ----------
    nl_df: DataFrame

    Returns
    -------
    None
    
  """
  fig, ax = plt.subplots(figsize=[20, 10])
  ax.bar(nl_df['Noise'], nl_df['Popularity'])

  ax.set_title('Noise Level vs Popularity', fontsize=20, pad=20)
  ax.set_xlabel('Noise Level', fontsize=20)
  ax.set_ylabel('Num of Reviews', fontsize=20)

  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=15)

  plt.savefig('images/noise_popularity.png')

def plot_alcohol_popularity_graph(al_df):
  """""
    Plot Alcohol vs Num of Reviews
    
    Parameters
    ----------
    al_df: DataFrame

    Returns
    -------
    None
    
  """
  fig, ax = plt.subplots(figsize=[20, 10])
  ax.bar(al_df['Alcohol'], al_df['Popularity'])

  ax.set_title('Alcohol vs Popularity', fontsize=20, pad=20)
  ax.set_xlabel('Alcohol', fontsize=20)
  ax.set_ylabel('Num of Reviews', fontsize=20)

  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=15)

  plt.savefig('images/alcohol_popularity.png')

restaurants_df = get_restaurants_df()
neighborhood_dynamics(restaurants_df)
plot_restaurant_ratings(restaurants_df)
factors_overview(restaurants_df)
