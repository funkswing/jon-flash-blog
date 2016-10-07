from flask import Markup
from datetime import datetime
from slugify import slugify
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from inflection import ordinalize


class BlogPost(object):

    def __init__(self, author, title, subtitle, body, timestamp=None, year=None, month=None):
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.timestamp = self._ensure_dt(timestamp)
        self.time_str = self._format_ts(self.timestamp)
        if year:
            self.year = year
        if month:
            self.month = month
        self.url_slug = slugify(self.title)  # Mongo query on this field

    @property
    def body_html(self):
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.body, extensions=[hilite, extras])

        return Markup(markdown_content)  # http://flask.pocoo.org/snippets/19/

    @staticmethod
    def _ensure_dt(timestamp):
        """
        Ensure self.timestamp is a Python datetime.datetime object. BlogPost() receives 'timestamp'
        attribute as either as a "time since Epoch (ms)" timestamp (from Mongo via JSON), as a
        datetime.datetime object (direct Mongo query/PyMongo), or as None type, in which case a
        new timestamp is created (for a newly published blog post)

        :param timestamp:
        :return: datetime.datetime
        """
        if type(timestamp) is dict and "$date" in timestamp.keys() and type(timestamp.get("$date")) is long:
            return datetime.fromtimestamp(timestamp['$date'] / 1000)
        if type(timestamp) is datetime:
            return timestamp
        else:
            return datetime.utcnow()

    @staticmethod
    def _format_ts(timestamp):
        """
        Format a datatime.datetime object to a string, e.g. "Monday, October 7th 2016",
         where the day of the month is an ordinal number without zero padding.
        :param timestamp:
        :return: string
        """
        if type(timestamp) is datetime:
            # Convert datetime object to string, but remove zero-padding and "ordinalize" the day of month value
            return timestamp.strftime("%A, %B {} %Y").format(
                ordinalize(timestamp.strftime(" %d").replace(" 0", ""))
            )

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
    timestamp = d.pop('timestamp')
    return BlogPost(author, title, subtitle, body, timestamp)


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
