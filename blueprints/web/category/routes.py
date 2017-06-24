from flask import Blueprint, render_template
from models import Category


mod = Blueprint('category', __name__, template_folder='templates',
                static_folder='static')


@mod.route('/')
def categories():
    categories = Category.query.all()
    return render_template('categories.html.j2', categories=categories,
                           page='Categories')
