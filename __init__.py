from flask import current_app, Blueprint, render_template, jsonify, request
from blog_post import BlogPost, dummy_posts, post1
from mongo import Mongo

from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension


blog = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates')


@blog.record
def record(state):
    db = state.app.config.get('MONGO_CONNECT')

    if not db:
        raise Exception("This blueprint expects you to provide "
                        "database access through Flask-PyMongo")


@blog.route('/posts')
def get_blog_post():
    """Render the blog page."""
    mongo = Mongo(current_app.mongo.db)

    if request.args.get('start'):
        try:
            start = int(request.args.get('start'))
        except ValueError:  # If unable to cast arg value to int, set to 0
            start = 0
        titles_cursor = mongo.get_blog_titles(start)
    else:
        titles_cursor = mongo.get_blog_titles()

    titles = [title['title'] for title in titles_cursor]
    data = dict(
        titles=titles
    )
    return jsonify(data)


@blog.route('/')
def blog_home():
    """Render a blog post"""
    return render_template(
        'blog/blog.html',
        title="Coding Blog - ",
        logo="logo",
        header="Coding Blog",
        skills="Or How I Did What I Did",
        posts=dummy_posts()
    )


@blog.route('/<int:year>/<int:month>/<string:slug>/')
def blog_post(year, month, slug):
    """Render a blog post"""

    post = post1.as_dict()

    return render_template('blog/post.html', post=post)
