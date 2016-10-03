from flask import Markup
from datetime import datetime
from slugify import slugify
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension


class BlogPost(object):

    def __init__(self, author, title, subtitle, body):
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.timestamp = datetime.utcnow()
        self.url_slug = slugify(self.title)  # Mongo query on this field

    @property
    def body_html(self):
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.body, extensions=[hilite, extras])

        return Markup(markdown_content)  # http://flask.pocoo.org/snippets/19/

    def as_dict(self):
        return dict(
            author=self.author,
            title=self.title,
            subtitle=self.subtitle,
            body=self.body_html,
            timestamp=self.timestamp.strftime("%A %x"),
            year_month=self.timestamp.strftime("%Y%m"),
            url_slug=self.url_slug
        )


def as_blog_post(d):
    # "object_hook=as_blog_post" for json.loads()
    author = d.pop('author')
    title = d.pop('title')
    subtitle = d.pop('subtitle')
    body = d.pop('body')
    return BlogPost(author, title, subtitle, body)


dummy_post1 = BlogPost(
        'Bob',
        'Cow jumps over the moon!',
        'Seriously! It happened...',
        'Hey, diddle diddle.'
    )
dummy_post2 = BlogPost(
        'Joe',
        'Itsie Bitsie Spider Climbed Up The Water Spout',
        'Forecast: Rain',
        'The itsie bitsie spider climbed up the water spout. Down came the rain and washed the spider out.'
    )
dummy_post3 = BlogPost(
        'Tom',
        'Jake and Jill went up the hill',
        "Help! I've fallen and I can't get up!",
        'Jake and Jill went up the hill to fetch a pail of water. Jake feel down and broke his crown.'
    )
dummy_post4 = BlogPost(
        'Jon',
        'Twinkle, Twinkle Little Star',
        'Little did he know how little he was and how massive the star was',
        'Twinkle, twinkle little star. How I wonder what you are. Up above the sky so bright.'
    )


def dummy_posts():
    return [
        dummy_post1.as_dict(),
        dummy_post2.as_dict(),
        dummy_post3.as_dict(),
        dummy_post4.as_dict()
    ]


if __name__ == '__main__':
    # Run module to insert "dummy posts" into MongoDB
    from pymongo import MongoClient
    client = MongoClient()
    db = client.blog
    db.posts.insert_many(
        dummy_posts()
    )
