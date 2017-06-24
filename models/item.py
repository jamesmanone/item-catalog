#!/usr/bin/env python
from blueprints import db
import datetime


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('items',
                                                              lazy='dynamic'))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.ForeignKey('users.id'))
    creator = db.relationship('User', backref=db.backref('items',
                                                         lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, category, name, description, creator):
        self.category = category
        self.name = name
        self.description = description
        self.creator = creator
