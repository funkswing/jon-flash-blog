from flask import Blueprint, render_template


blog = Blueprint('blog', __name__, url_prefix='/blog', template_folder='templates')


@blog.route('/')
def blog_index():
    """Render the blog page."""
    return render_template('blog/blog.html')
