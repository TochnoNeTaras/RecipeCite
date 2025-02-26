from flask import Flask, render_template, request
from db_scripts import DBManager
from dotenv import load_dotenv
load_dotenv()
import os

IMG_PATH = os.path.dirname(__file__) + os.sep + 'static' + os.sep + 'img'

app = Flask(__name__)  # Створюємо веб–додаток Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = DBManager("blog.db")


@app.route("/")  # Вказуємо url-адресу дл   я виклику функції
def index():
    categories = db.get_categories()
    articles = db.get_articles()
    return render_template("index.html", categories=categories, articles=articles)  # html-сторінка, що повертається у браузер


@app.route("/category/<int:category_id>")  # Вказуємо url-адресу для виклику функції
def category_page(category_id):
    categories = db.get_categories()
    articles = db.get_articles_by_category(category_id)
    return render_template("category.html", categories=categories, articles=articles, 
                           category_name=categories[category_id][1])  # html-сторінка, що повертається у браузер


@app.route("/articles/<int:article_id>")  # Вказуємо url-адресу для виклику функції
def article_page(article_id):
    categories = db.get_categories()
    article = db.get_article_by_id(article_id)
    articles = db.get_articles_by_category(article[6])
    return render_template("article.html", categories=categories, article=article, articles=articles)  # html-сторінка, що повертається у браузер

@app.route("/articles/new", methods=["GET", "POST"])
def new_article():
    categories = db.get_categories()
    if request.method == 'POST':
        image = request.files['image']
        image.save(IMG_PATH + os.sep + image.filename)
        db.create_article(request.form['title'], request.form['description'], request.form['text'],
                          image.filename, 1, request.form['category'])

    return render_template("new_article.html",  categories=categories)


@app.route("/search")  # Вказуємо url-адресу для виклику функції
def search_page():
    categories = db.get_categories()
    query = request.args.get("query", '')
    articles = db.search_articles(query)
    return render_template("search_page.html", categories=categories, articles=articles, 
                           category_name=query)  # html-сторінка, що повертається у браузер




if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # автоматичне оновлення шаблонів
    app.run(debug=True)  # Запускаємо веб-сервер з цього файлу в режимі налагодження
