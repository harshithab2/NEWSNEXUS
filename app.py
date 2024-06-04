from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)
db_name = 'news_database.db'

def create_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, image_url TEXT, description TEXT)''')
    conn.commit()
    conn.close()

def insert_article(title, image_url, description):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, image_url, description) VALUES (?, ?, ?)", (title, image_url, description))
    conn.commit()
    conn.close()

def get_articles_from_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    articles = c.fetchall()
    conn.close()
    return articles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_news', methods=['POST'])
def get_news():
    api_key = "a8ab6d9bd5684d27bab671e76c15eb91"
    country = request.form.get('country')[:2]
    category = request.form.get('category')
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
    news = requests.get(url).json()
    articles = news["articles"]
    create_table()
    for article in articles:
        insert_article(article['title'], article['urlToImage'] if 'urlToImage' in article else '', article['description'])
    return render_template('news.html', articles=articles)

@app.route('/view_saved_articles')
def view_saved_articles():
    articles = get_articles_from_db()
    return render_template('saved_articles.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
