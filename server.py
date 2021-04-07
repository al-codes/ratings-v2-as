"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud 
from jinja2 import StrictUndefined


app = Flask(__name__)

# Required to use Flask sessions and debug toolbar
app.secret_key = "MAM"

# Undefined variable in Jinja2 fails *silently* so adding
# this to raise an error instead for debugging
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage"""

    # Flask session set up for ratings & login
    session['show_form'] = True
    session['show_login'] = True

    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    """Display all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details for a particular movie."""

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/movies/<movie_id>', methods=['POST'])
def make_movie_rating(movie_id):
	"""Create a new rating."""

	movie = crud.get_movie_by_id(movie_id)
	user_s = session['user']
	score = request.form['score']

	new_rating = crud.create_rating(user_s, movie, score)
	print(new_rating)
	session['rating'] = new_rating

	return redirect('movie_details.html')

	return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    """Display all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)


@app.route('/users/<user_id>')
def user_details(user_id):
    """View all users."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/register', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    session['user'] =[]


    if user:
        flash('This email may already be registered. Try again.')
        
    else:
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/')



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

# if __name__ == '__main__':
#     from server import app
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.