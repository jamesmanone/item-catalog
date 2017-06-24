from flask import Blueprint, request, abort
from models import Category, Item
import utilities

mod = Blueprint('api', __name__)


# Kept to one endpoint to follow what seems to be common now for api's with
# a reasonable (or sometimes unreasonable) number of options
@mod.route('/json')
def api():
    method = request.args.get('method')
    query = None
    if request.args.get('q'):
        query = ' '.join(request.args.get('q').split('%20'))

    # retrieve items in category by category name
    if method == 'category.list':
        category = Category.query.filter_by(name=query).first_or_404()
        items = Item.query.filter_by(category=category).all()
        obj = []
        for item in items:
            data = {
                'name': item.name,
                'id': item.id
            }
            obj.append(data)
        return utilities.make_cors_json_response(obj)

    # Search through categories && items
    if method == 'search':
        if not query:
            return utilities.make_cors_json_response({'items': [],
                                                     'categories': []})
        categories = Category.query.filter(Category.name.ilike('%'+query) |
                                           Category.name.ilike('%'+query+'%') |
                                           Category.name.ilike(query+'%') |
                                           Category.name.ilike(query))
        items = Item.query.filter(Item.name.ilike('%'+query) |
                                  Item.name.ilike('%'+query+'%') |
                                  Item.name.ilike(query+'%') |
                                  Item.name.ilike(query))
        obj = {'items': [], 'categories': []}
        for item in items:
            obj['items'].append(item.name)
        for cat in categories:
            obj['categories'].append(cat.name)
        return utilities.make_cors_json_response(obj)

    # Retrieve list of categories
    if method == 'categories':
        categories = Category.query.all()
        obj = []
        for category in categories:
            data = {
                'name': category.name,
                'id': category.id
            }
            obj.append(data)
        return utilities.make_cors_json_response(obj)

    # Retrieve item details by item name
    if method == 'item':
        if not query:
            abort(400)
        item = Item.query.filter(Item.name.ilike(query)).first_or_404()
        obj = {
            'id': item.id,
            'category': item.category.name,
            'name': item.name,
            'description': item.description
        }
        return utilities.make_cors_json_response(obj)
