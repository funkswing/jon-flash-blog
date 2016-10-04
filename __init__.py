from flask import current_app, Blueprint, render_template, jsonify, request
from blog_post import BlogPost, as_blog_post, dummy_posts, dummy_post1
from mongo import Mongo
import json
from bson import json_util


blog = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates')


@blog.record
def record(state):
    db = state.app.config.get('MONGO_CONNECT')

    if not db:
        raise Exception("This blueprint expects you to provide "
                        "database access through Flask-PyMongo")


def get_mongo():
    return Mongo(current_app.mongo.db)


@blog.route('/posts')
def get_blog_post():
    """Render the blog page."""
    mongo = get_mongo()

    if request.args.get('start'):
        try:
            start = int(request.args.get('start'))
        except ValueError:  # If unable to cast arg value to int, set to 0
            start = 0
        docs = mongo.get_blog_previews(start)
    else:
        docs = mongo.get_blog_previews()

    data = json_util.dumps(docs)
    return current_app.response_class(data, mimetype='application/json')


@blog.route('/')
def blog_home():
    """Render a blog post"""

    posts_json = get_blog_post()
    posts = json.loads(posts_json.data)

    for post in posts:
        post['year'] = post['year_month'][:4]
        post['month'] = post['year_month'][4:]

    return render_template(
        'blog/blog.html',
        title="Coding Blog - ",
        logo="logo",
        header="Coding Blog",
        skills="Or How I Did What I Did and What I Learned Along the Way",
        posts=posts
    )


@blog.route('/<int:year>/<int:month>/<string:slug>/')
def blog_post(year, month, slug):
    """Render a blog post"""
    mongo = get_mongo()

    d = mongo.get_blog_post(slug)

    author = d.pop('author')
    title = d.pop('title')
    subtitle = d.pop('subtitle')
    body = d.pop('body')
    timestamp = d.pop('timestamp')
    post = BlogPost(author, title, subtitle, body, timestamp)

    return render_template('blog/post.html', post=post)
