from flask import Blueprint, render_template, request

from models import Category, Item

mod = Blueprint('search', __name__, template_folder='templates',
                static_folder='static')


# Search page
@mod.route('/')
def search():
    if not request.args.get('q'):
        return render_template('search.html.j2', page='search')
    query = request.args.get('q').replace('%20', ' ').replace('+', ' ')
    # There must be a way to use r"/\w*{0}\w*/".format(re.escape(query))
    categories = Category.query.filter(Category.name.ilike('%'+query) |
                                       Category.name.ilike('%'+query+'%') |
                                       Category.name.ilike(query+'%') |
                                       Category.name.ilike(query)).all()
    items = Item.query.filter(Item.name.ilike('%'+query) |
                              Item.name.ilike('%'+query+'%') |
                              Item.name.ilike(query+'%') |
                              Item.name.ilike(query)).all()
    print categories
    print items
    return render_template('results.html.j2', items=items,
                           categories=categories, page=query.capitalize())
