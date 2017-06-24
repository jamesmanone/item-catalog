#!/usr/bin/env python
from blueprints import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    uuid = db.Column(db.String, nullable=False)
    provider = db.Column(db.String, nullable=False)

    def __init__(self, uuid, email, provider, name):
        self.uuid = uuid
        self.name = name
        self.email = email
        self.provider = provider

    @classmethod
    def by_google_uuid(cls, uuid):
        return cls.query.filter_by(provider='google').filter_by(
                                   uuid=uuid).first()

    @classmethod
    def by_facebook_uuid(cls, uuid):
        return cls.query.filter_by(provider='facebook').filter_by(
                                    uuid=uuid).first()

    @classmethod
    def by_id(cls, query):
        return cls.query.filter_by(id=query).first()
