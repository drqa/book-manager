from flask import render_template, url_for, flash, redirect, abort
from flask.templating import render_template_string
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login.utils import login_required, logout_user
from bookcrud.forms import RegistrationForm,LoginForm, BookForm, ShelfCreateForm, ShelfAddForm
from bookcrud import app, db, bcrypt
from bookcrud.models import Book, User, Shelf, BooksOnShelf
from flask_login import login_user, current_user

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated != True:
        return redirect(url_for('login'))
    current = current_user.id
    shelves = Shelf.query.filter_by(user_id=current)
    return render_template('index.html', isIndex = True, shelves=shelves) 

@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit() 
        flash(f"Your account has been created. You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template('register.html', title='register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Login unsucceful. Please check email/password.")
    return render_template('login.html', title='login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/add book", methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, isbn=form.isbn.data, pub_year=form.pub_year.data, original_lang=form.original_lang.data)
        db.session.add(book)
        db.session.commit()
        flash('Book added to database', 'success')
        return redirect(url_for("add_book"))
    books = Book.query.all()
    return render_template('add_book.html', title='add_book', form=form, books=books)

@app.route("/shelf/create", methods=["GET", "POST"])
@login_required
def create_shelf():
    if current_user.is_authenticated != True:
        return redirect(url_for('login'))
    form = ShelfCreateForm()
    if form.validate_on_submit():
        shelf = Shelf(name=form.title.data, description=form.description.data, user=current_user)
        db.session.add(shelf)
        db.session.commit()
        flash('Shelf Created', 'success')
        return redirect(url_for("create_shelf"))
    shelves = Shelf.query.all()
    return render_template('create_shelf.html', title='create_shelf', form = form, shelves=shelves)

@app.route("/shelf/<int:shelf_id>", methods=["GET", "POST"])
def shelf(shelf_id):
    shelf = Shelf.query.get_or_404(shelf_id)
    if shelf.user_id != current_user.id:
        abort(403)
    form = ShelfAddForm()
    if form.validate_on_submit():
        books = Book.query.all()
        for book in books:
            if form.book.data == book.title:
                to_shelf = BooksOnShelf(book_id = book.id, shelf_id = shelf.id)
                db.session.add(to_shelf)
                db.session.commit()
    return render_template('shelf.html', title=shelf.name, shelf=shelf, form = form)



