from flask import Flask, session, redirect, render_template, flash, request
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_demo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'abc123')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['WTF_CSRF_ENABLED'] = True
print(app.config['SECRET_KEY'])

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/', methods=["GET"])
def home_page():
    """Display home page, or redirect to /register"""
    flash("Welcome to the home page", "primary")
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Render register user form"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # send data from WTForms to register which is a class function. Would normally make new User instance, but first need to hash pwd with register function, which returns new User instance.
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.commit()

        session['username'] = new_user.username
        flash(f"Welcome to Flask Feedback, {new_user.username}! Your account was created successfully!", "success")
        return redirect(f'/users/{username}')
    
    else:
        return render_template('register.html', form=form)

@app.route('/users/<username>', methods=["GET"])
def display_user_page(username):
    """Take a user to their own page"""

    if 'username' not in session:
        flash("You're not logged in! Please login first.", "danger")
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first()

    return render_template('user.html', user=user)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Render login form or log user in"""
    
    if "username" in session:
        flash("You're already logged in! See below.","info")
        return redirect(f'/users/{session["username"]}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authorize(username, password)
        if user:
            session['username'] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(f'/users/{username}')
        else:
            flash("Your username or password is incorrect!", "danger")
            return redirect('/login')
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'username' in session:
        flash(f"Good-bye {session['username']}, you logged out successfully.", "success")
        session.pop('username', None)    
        return redirect('/login')
    else:
        flash("You can't logout, because you're not logged in! :)", "warning")
        return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback_form(username):
    """Show and handle feedback form for a logged in user."""

    if 'username' not in session:
        flash("You're not logged in! Please login first.", "danger")
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=user.username)

        db.session.add(new_feedback)
        db.session.commit()

        flash("Thanks for adding your feedback!", "success")
        return redirect(f'/users/{username}')

    return render_template('feedback_form.html', form=form, user=user)

@app.route('/users/<username>/delete', methods=["GET"])
def delete_account(username):
    """Delete logged in user and all their feedback."""

    if 'username' not in session:
        flash("You're not logged in! Please login first.", "danger")
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    flash("You deleted your account and all corresponding feedback for that account.", "warning")    

    return redirect('/login')

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show and handle feedback edit form for a logged in user."""

    if 'username' not in session:
        flash("You're not logged in! Please login first.", "danger")
        return redirect('/login')

    curr_username = session["username"]
    curr_user = User.query.filter_by(username=curr_username).first()
    curr_feedback = Feedback.query.get_or_404(feedback_id)

    form = FeedbackForm()

    if form.validate_on_submit():
        curr_feedback.title = form.title.data
        curr_feedback.content = form.content.data
        db.session.commit()

        flash("You've updated this feedback. Thank you.", "success")
        return redirect(f'/users/{curr_user.username}')

    form.title.data = curr_feedback.title
    form.content.data = curr_feedback.content
    
    return render_template('update_feedback.html', form=form, user=curr_user, feedback=curr_feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=["GET"])
def delete_feedback(feedback_id):
    """Delete a logged-in user's feedback."""

    if 'username' not in session:
        flash("You're not logged in! Please login first.", "danger")
        return redirect('/login')

    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash("You successfully deleted that feedback", "success")
    return redirect(f'/users/{feedback.username}')
