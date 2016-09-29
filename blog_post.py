from datetime import datetime
from slugify import slugify


class BlogPost(object):
    """
    title
    subtitle
    url_slug
    author
    timestamp
    """
    def __init__(self, author, title, subtitle, body, post_id=None):
        self.author = author
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.timestamp = datetime.utcnow()
        self.url_slug = slugify(self.title)  # Mongo query on this field
        self.post_id = post_id

    def as_dict(self):
        return dict(
            author=self.author,
            title=self.title,
            subtitle=self.subtitle,
            body=self.body,
            timestamp=self.timestamp.strftime("%A %x"),
            month=self.timestamp.strftime("%m"),
            year=self.timestamp.strftime("%Y"),
            url_slug=self.url_slug
        )


post1 = BlogPost(
        'Bob',
        'Cow jumps over the moon!',
        'Seriously! It happened...',
        'Hey, diddle diddle.'
    )
post2 = BlogPost(
        'Joe',
        'Itsie Bitsie Spider Climbed Up The Water Spout',
        'Forecast: Rain',
        'The itsie bitsie spider climbed up the water spout. Down came the rain and washed the spider out.'
    )
post3 = BlogPost(
        'Tom',
        'Jake and Jill went up the hill',
        "Help! I've fallen and I can't get up!",
        'Jake and Jill went up the hill to fetch a pail of water. Jake feel down and broke his crown.'
    )
post4 = BlogPost(
        'Jon',
        'Twinkle, Twinkle Little Star',
        'Little did he know how little he was and how massive the star was',
        'Twinkle, twinkle little star. How I wonder what you are. Up above the sky so bright.'
    )


def dummy_posts():
    return [
        post1.as_dict(),
        post2.as_dict(),
        post3.as_dict(),
        post4.as_dict()
    ]
