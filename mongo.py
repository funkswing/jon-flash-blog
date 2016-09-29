

class Mongo(object):
    def __init__(self, db):
        self.db = db
        self.COLL = "posts"

    def get_blog_titles(self, start=0):
        return self.db[self.COLL].find({}, {"title": 1}).sort("_id", -1).skip(start).limit(10)

    def get_blog_post(self, title):
        return self.db[self.COLL].find({"title": title})

    def insert_blog(self, blog_post):
        return self.db[self.COLL].insert(blog_post)


if __name__ == "__main__":
    from blog_post import BlogPost
    from pymongo import MongoClient
    client = MongoClient()
    db = client.blog
    mongo = Mongo(db)
    for x in range(10):
        blog_post = BlogPost("Blog #%s" % (x+1), "My best post evah!")
        mongo.insert_blog(blog_post.as_dict())
