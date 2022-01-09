from datetime import datetime
from enum import unique
import flask_login
from bookcrud import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    shelves = db.relationship('Shelf', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Book(db.Model):
    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)
    isbn = db.Column(db.String(), unique=True, nullable=False)
    pub_year = db.Column(db.String(), unique=False, nullable=True)
    original_lang = db.Column(db.String(), unique=False, nullable=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', '{self.pub_year}', '{self.original_lang}')"  

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag('{self.id}, {self.name}')"

class Tagging(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), unique=False, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), unique=False, nullable=False)

    def __repr__(self):
        return f"Taggings('{self.book_id}', '{self.tag_id}')"

class Shelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False)

    def __repr__(self):
        return f"Shelf('{self.id}, {self.name}, {self.user_id}')"

class BooksOnShelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), unique=False, nullable=False)
    shelf_id = db.Column(db.Integer, db.ForeignKey("shelf.id"), unique=False, nullable=False)

    def __repr__(self):
        return f"BooksOnShelf('{self.id}, {self.book_id}, {self.shelf_id}')"

