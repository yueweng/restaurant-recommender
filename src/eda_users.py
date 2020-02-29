import pandas as pd
import matplotlib.pyplot as plt
import random
from src.methods import get_users_df

def reviewers_by_city(users_df, n=25):
  """
    Group reviewers by city and plot graph
    
    Parameters
    ----------
    users_df: DataFrame
    n: number of cities
    

    Returns
    -------
    None
    
  """
  reviews_group = users_df.sort_values(by='reviews', ascending=False)
  city_review = reviews_group.groupby('city').agg({'state': 'first','userid': 'count'}).reset_index()
  top_cities_reviews = city_review.sort_values(by='userid', ascending=False)[:n]

  st = get_colors_st(top_cities_reviews)
  plot_cities_reviews(top_cities_reviews, st)

def get_colors_st(top_cities_reviews):
  """
    For plotting purpose. Randomize color plotting for states
    
    Parameters
    ----------
    top_cities_reviews: DataFrame
    

    Returns
    -------
    st: Dictionary
    
  """
  unique_states = top_cities_reviews['state'].unique()

  st = {}
  for state in unique_states:
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    st[state] = [r, g, b]

  return st

def plot_cities_reviews(top_cities_reviews, st):
  """
    Plot Reviewers by City
    
    Parameters
    ----------
    top_cities_reviews: DataFrame
    st: Dictionary
    

    Returns
    -------
    None
    
  """
  fig, ax = plt.subplots(figsize=[20, 10])

  top_cities_reviews.sort_values('userid', inplace=True)

  for idx, city in top_cities_reviews.iterrows():
      ax.barh(city['city'], city['userid'], color=st[city['state']], label=city['state'])
      
  hand, labl = ax.get_legend_handles_labels()
  lablout = []
  handout = []
  for h,l in zip(hand,labl):
    if l not in lablout:
      lablout.append(l)
      handout.append(h)

  ax.set_title('Reviewers by City', fontsize=20, pad=20)
  ax.set_xlabel('Num of Users', fontsize=20)
  ax.set_ylabel('Cities', fontsize=20)

  plt.tick_params(axis='x', which='major', labelsize=18)
  plt.tick_params(axis='y', which='major', labelsize=15)
  plt.legend(handout, lablout, fontsize=20)

  plt.savefig('images/reviewers_city.png', bbox_inches = "tight")


users_df = get_users_df()
reviewers_by_city(users_df)