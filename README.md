# Restaurant Recommender

### Premise

### Setup
I collected the data from Yelp and saved it into a MongoDB database. Once I got the data, I converted the data into csv format. This file shows the setup: `src/convert_to_csv.py`

### Data

### EDA
I grouped the restaurants based on the neighborhood and did an analysis of the number of reviews per neighborhood

![](images/popularity_neighborhood.png)

From the graphs, the Mission Neighborhood has the highest number of reviews.

Here is a breakdown based on:

1. Ambience
![](images/ambience_popularity.png)

2. Noise Level
![](images/noise_popularity.png)

3. Alcohol
![](images/alcohol_popularity.png)

Here is a graph of the number of reviews based on ratings
![](images/restaurants_ratings.png)


#### Reviewers by City
![](images/reviewers_city.png)
