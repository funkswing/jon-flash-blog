# How I Created the Blog You Are Currently Reading 
> "You should make yourself a blog" said everyone ever in software engineering 

### Work in progress post. Jumbled notes below... 

Create Flask Blueprint to create blog as a component Docs: 
http://flask.pocoo.org/docs/0.11/blueprints 

Project structure: 
``` 
/blog/ 
    /templates/blog/
/static/blog/
    __init__.py
    processing.py
/static/
/templates/
app.py
requirements.txt 
```

Import "blog" module: 
```
/blog/__init__.py
from flask import Blueprint, render_template 
``` 

```
blog = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates')```


```sh 
@blog.route('/') 
def blog_index(): 
    """Render the blog page.""" 
    return render_template('blog/blog.html') 
``` 

app.py: 
``` 
from blog import blog 
from flask.ext.pymongo 
import PyMongo 

app = Flask(__name__) 
app.register_blueprint(blog) 
app.config['MONGO_DBNAME'] = 'blog' 
mongo = PyMongo(app) 
``` 

Requirements.txt 
``` 
flask 
requests 
Flask-PyMongo 
markdown 
Pygments 
``` 
____ 
[Loops in templates](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)

[Blog post URL schema](http://blog.benmcmahen.com/post/41122888102/creating-slugs-for-your-blog-using-expressjs-and)
``` 
/blog/2016/09/title-of-blog-post 
```
