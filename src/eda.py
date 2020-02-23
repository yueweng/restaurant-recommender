import pandas as pd
import matplotlib.pyplot as plt


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

def plot_neighborhood_popularity(neighborhood_group, n=20):
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

restaurants_df = get_restaurants_df()
neighborhood_dynamics(restaurants_df)