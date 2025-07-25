#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

# Use a proper server name with a dot to avoid cookie domain warnings
app.config['SERVER_NAME'] = 'localhost.localdomain:5555'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()  # Clear the entire session, not just page_views
    return jsonify({'message': '200: Successfully cleared session data.'}), 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(jsonify(articles))

@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0
    session['page_views'] += 1

    if session['page_views'] <= 3:
        article = Article.query.get(id)
        if article:
            return jsonify(ArticleSchema().dump(article)), 200
        else:
            return jsonify({'message': 'Article not found.'}), 404
    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401


if __name__ == '__main__':
    app.run(port=5555)
