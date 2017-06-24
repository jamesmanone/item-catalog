from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0], static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = \
                                'postgresql://weblink:12345@localhost/catalog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Start ORM
db = SQLAlchemy(app)

# Imports that can't be at the top due to circular imports
from models import User  # NOQA: E401, E402
from models import Category  # NOQA: E401, E402
from models import Item  # NOQA: E401, E402
from web.item.routes import mod as item_routes  # NOQA: E401, E402
from web.user.routes import mod as user_routes  # NOQA: E401, E402
from web.category.routes import mod as category_routes  # NOQA: E401, E402
from web.search.routes import mod as search_routes  # NOQA: E401, E402
from api.routes import mod as api_routes  # NOQA: E401, E402

app.register_blueprint(item_routes, url_prefix='/item')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(category_routes, url_prefix='/category')
app.register_blueprint(search_routes, url_prefix='/search')
app.register_blueprint(api_routes, url_prefix='/api')


@app.route('/')
def home():
    return render_template('home.html.j2', page='Home')
