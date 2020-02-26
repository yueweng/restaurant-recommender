from flask import Flask, url_for, render_template
from recommendations import get_restaurants_df, cosine_similarity_recommendations

app = Flask(__name__,  template_folder='templates')

@app.route('/')
def index():
  restaurants_df = get_restaurants_df()
  li = cosine_similarity_recommendations(restaurants_df, title='Marufuku Ramen SF')
  return render_template('index.html', li=li.items())


def api_root():
    restaurants_df = get_restaurants_df()
    li = cosine_similarity_recommendations(restaurants_df, title='Marufuku Ramen SF')
    return li

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()