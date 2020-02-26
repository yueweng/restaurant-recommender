import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

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

def cosine_similarity_recommendations(restaurants_df):
  cui = restaurants_df['cuisines'].str.split(", ")
  cuisines_dummies = pd.get_dummies(cui.apply(pd.Series).stack()).sum(level=0)
  cos_sim = cosine_similarity(cuisines_dummies, cuisines_dummies)

  title = 'Noosh'
  print("Restaurant: {}".format(title))

  index = restaurants_df[restaurants_df['title'] == title].index
  compare_sim = cos_sim[index]
  # print(compare_sim)

  sim = {}
  # iterate each row of cosine similarity matrix and compute the distance
  for idx, row in enumerate(cos_sim):
  #     print(row)
      if index != idx:
          sim[idx] = cosine_similarity(compare_sim.reshape(1, -1), row.reshape(1, -1))[0][0].astype(float)

  sort_values = sorted(sim.items(), key=lambda kv: kv[1], reverse=True)
  top_n = sort_values[:10]

  print("Recommendations")
  for row, value in top_n:
  #     print(value)
      print(restaurants_df.iloc[row]['title'])

  print("-------------------")

restaurants_df = get_restaurants_df()
cosine_similarity_recommendations(restaurants_df)
