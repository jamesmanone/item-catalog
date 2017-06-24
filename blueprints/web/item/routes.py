#!/usr/bin/env python
from flask import Blueprint, render_template, redirect, flash, url_for, \
    request, session, abort, json
from blueprints import db
from models import Item, Category, User
import utilities

mod = Blueprint('item', __name__, template_folder='templates',
                static_folder='static')


# All routes prefixed with /item

@mod.route('/')
def items():
    list_items = Item.query.order_by(Item.created.desc()).limit(10).all()
    return render_template('items.html.j2', items=list_items, page='Items')


@mod.route('/<int:item_id>/')
def item(item_id):
    state = utilities.get_state()
    session['state'] = state
    list_item = Item.query.get_or_404(item_id)
    return render_template('item.html.j2',
                           item=list_item, state=state,
                           page=list_item.name)


@mod.route('/new/', methods=['GET', 'POST'])
@utilities.login_required
def add_item():
    if request.method == 'GET':

        # Set state for CSRF protection
        state = utilities.get_state()
        session['state'] = state
        categories = Category.query.all()
        return render_template('new-item.html.j2', categories=categories,
                               state=state, page='New Item')
    else:
        form = request.get_json()
        try:
            form_category = form['category']
            description = form['description']
            name = form['title']
        # checking for incomplete forms
        except:
            abort(418)
        if not form_category or not description or not name:
            #  Useful response ommitted: handled in js
            abort(418)
        # CSRF check
        if form['state'] != session['state']:
            abort(401)
        # Check db for category
        try:
            category = Category.search(form_category)
            assert category is not None
        # Make category if not in db
        except:
            category = Category(form_category)
            db.session.add(category)
            db.session.commit()
        user = User.by_id(session['user'])
        it = Item(category, name, description, user)
        db.session.add(it)
        db.session.commit()
        flash('{0} has been added to the catalog'.format(it.name),
              'success')
        return json.jsonify({'href': url_for('item.item', item_id=it.id)})


@mod.route('/<int:item_id>/edit', methods=['GET', 'POST', 'DELETE'])
@utilities.login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    user = User.query.get(session['user'])

    # Prevent edits to non-owned items
    if item.creator != user:
        flash('You can only modify your own items', 'danger')
        return redirect(url_for('user.login'))
    if request.method == 'GET':

        # Send edit form
        categories = Category.query.all()
        category = Category.query.get(item.category_id)
        state = utilities.get_state()
        session['state'] = state
        return render_template('edit.html.j2', item=item, state=state,
                               page='Edit {0}'.format(item.name),
                               category=category, categories=categories)
    elif request.method == 'DELETE':
        data = request.get_json()

        # CSRF protection
        state = data['state']
        if session['state'] != state:
            abort(401)
        db.session.delete(item)
        db.session.commit()
        flash('{0} was successfully deleted'.format(item.name.capitalize()),
              'success')
        return redirect(url_for('item.items'))
    else:
        form = request.get_json()

        # CSRF protection
        if session['state'] != form['state']:
            abort(401)
        try:
            form_category = form['category']
            description = form['description']
            name = form['title']
        except:

            # Form validation is handled in js, so we just kill the request if
            # not all fields are filled out.
            abort(418)

        # Double check those fields? This should be redudndant
        if not form_category or not description or not name:
            #  Useful response ommitted: handled in js
            abort(418)
        try:

            # Find category in DB
            category = Category.search(form_category)
            assert category is not None
        except:

            # If category not in db, make new category
            category = Category(form_category)
            db.session.add(category)
            db.session.commit()
        item.name = name
        item.description = description
        item.category = category
        db.session.commit()
        return redirect(url_for('item.items'))
