#!/usr/bin/env python

from blueprints import db

db.drop_all()
db.create_all()
