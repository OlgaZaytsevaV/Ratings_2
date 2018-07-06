"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")
                         


@app.route('/users')
def user_list():
    
    users = User.query.order_by('user_id').all()
    return render_template("user_list.html", users=users)

@app.route('/movies')
def movies_list():

    movies = Movie.query.order_by('title').all()
    return render_template('movies_list.html', movies=movies)

@app.route('/movie/<str:title>')
def movie_info(title):
    movie_title =  Movie.query.filter_by(Movie.title=
    i


@app.route('/register', methods=["GET"])
def register_form():

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():

    email = request.form.get('email')
    password = request.form.get('password')


    if User.query.filter_by(email='email').first():
        flash("User with this email already exists.")
        return redirect('/')
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("User added to database. Please log in.")
        return redirect('/login')


@app.route('/login', methods=["POST"])
def process_login_form():
    email = request.form.get('email')
    password = request.form.get('password')


    user = User.query.filter_by(email=email, password=password).first()
    if user:
        flash("Login successful.")
        session['user_id'] = user.user_id
        return redirect('/users/{}'.format(user.user_id))
    else:
        flash("Login unsuccesseful.")
        return redirect('/login')






@app.route('/login')
def show_login_form():
    return render_template("login_form.html")


@app.route('/users/<int:uid>')
def show_user_info(uid):

    print("User UID is: {}".format(uid))

    user = User.query.get(uid)

    return render_template('user_info.html',user=user, age=user.age, zipcode=user.zipcode, ratings=user.ratings)
    
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash('You are now logged out')
        return redirect('/')
    else:
        flash('You are not logged in')
        return redirect('/login')







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
