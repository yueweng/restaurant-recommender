import pandas as pd

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