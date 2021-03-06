from flask import Flask, url_for, request, redirect, render_template
from recommendations import get_restaurants_df, \
                            cosine_similarity_recommendations, \
                            reviews_recommender, \
                            description_recommender, \
                            get_reviews_cond_df, \
                            get_reviews_df, \
                            get_all_restaurant_names, \
                            get_doc_sim, \
                            get_desc_sim
import pandas as pd

'''
  Create a Web Application Using Flask
'''

app = Flask(__name__,  template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
  restaurants_df = get_restaurants_df()
  reviews_df = get_reviews_df()
  restaurant_names = get_all_restaurant_names(restaurants_df, reviews_df)
  if request.method == 'POST':
    text = request.form['text']
    return redirect(url_for('recommendations', text=text))
  return render_template('index.html', restaurant_names=restaurant_names)

@app.route('/recommendations/<text>')
def recommendations(text):
  restaurants_df = get_restaurants_df()
  reviews_condensed_df = get_reviews_cond_df()
  reviews_df = get_reviews_df()
  doc_sim = get_doc_sim()
  desc_sim = get_desc_sim()
  df1 = cosine_similarity_recommendations(restaurants_df, title=text, n=12)
  df2 = reviews_recommender(restaurants_df, reviews_df, reviews_condensed_df, doc_sim, title=text)
  df3 = description_recommender(restaurants_df, desc_sim, title=text)
  recommended_df = pd.concat([df1[:1], df2[:1], df3[:1]])
  return render_template('recommendations.html', \
                          df_rec = recommended_df, 
                          df1_other=df1[1:11],
                          df2_other=df2[1:11],
                          df3_other=df3[1:11])

@app.errorhandler(500)
def error_page(e):
    return render_template('500.html')

if __name__ == '__main__':
    app.run()