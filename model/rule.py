from database.db import db


class Rules(db.Model):
    id_rule = db.Column(db.Integer, primary_key=True)
    id_detector = db.Column(db.Integer)
    id_organiztion = db.Column(db.Integer)
    is_blacklist = db.Column(db.Boolean)
