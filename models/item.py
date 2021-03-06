import sqlite3
from db import db


class ItemModel(db.Model):
    __tablename__="items"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) #to connect items and store
    store = db.relationship('StoreModel') # relation

    @classmethod
    def find_by_name(cls,name):
        return ItemModel.query.filter_by(name=name).first() #select * from items where name=name limit 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_all(cls):
        return cls.query.all()