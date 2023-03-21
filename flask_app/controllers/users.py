from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, player, comment

# Create route for the landing page of the website. This will eventually be the login and registration page
@app.route('/')
def index():
    if "user_id" not in session:
        return render_template('index.html')
    return redirect("/profile")

@app.route("/register", methods=["POST"])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    user_id = user.User.register(request.form)
    session["user_id"] = user_id
    return redirect("/profile")

@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    players = player.Player.get_user_players(session["user_id"])
    return render_template('profile.html', logged_in_user=logged_in_user, players=players)

@app.route('/activity')
def activity():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    comments=comment.Comment.get_user_comments(session["user_id"])
    return render_template('useractivity.html',logged_in_user=logged_in_user, comments=comments)

@app.route('/social')
def social():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    comments=comment.Comment.get_all_comments()
    return render_template('social.html',logged_in_user=logged_in_user, comments=comments)

@app.route("/login", methods=["POST"])
def login():
    logged_in_user = user.User.validate_login(request.form)
    if not logged_in_user:
        return redirect ("/")
    session["user_id"] = logged_in_user.id
    return redirect('/profile')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


