#!/usr/bin/env python
from blueprints import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def search(cls, query):
        return cls.query.filter_by(name=query).first()
