from flask import Flask, url_for, request, render_template
from recommendations import get_restaurants_df, \
                            cosine_similarity_recommendations, \
                            reviews_recommender, \
                            description_recommender, \
                            get_reviews_cond_df, \
                            get_reviews_df, \
                            get_all_restaurant_names

app = Flask(__name__,  template_folder='templates')

@app.route('/')
def index():
  restaurants_df = get_restaurants_df()
  # df = cosine_similarity_recommendations(restaurants_df)
  # df.fillna(0, inplace=)
  # li = cosine_similarity_recommendations(restaurants_df, title='Marufuku Ramen SF')
  # return render_template('index.html', li=li)
  restaurant_names = get_all_restaurant_names(restaurants_df)
  return render_template('index.html', restaurant_names=restaurant_names)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    restaurants_df = get_restaurants_df()
    # reviews_condensed_df = get_reviews_cond_df()
    # reviews_df = get_reviews_df()
    df = cosine_similarity_recommendations(restaurants_df, title=text, n=3)
    # reviewli = reviews_recommender(reviews_df, reviews_condensed_df, title=text)
    # descli = description_recommender(restaurants_df, title=text)
    restaurant_names = get_all_restaurant_names(restaurants_df)
    return render_template('index.html', df = df, restaurant_names=restaurant_names)
# def api_root():
#     restaurants_df = get_restaurants_df()
#     li = cosine_similarity_recommendations(restaurants_df, title='Marufuku Ramen SF')
#     return li

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()