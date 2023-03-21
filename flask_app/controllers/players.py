from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, player, comment

# Create route for the landing page of the website. This will eventually be the login and registration page
@app.route('/view/<int:id>')
def viewplayer(id):
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    onePlayer = player.Player.get_player_by_id(id)
    comments = comment.Comment.get_user_comments(session["user_id"])
    return render_template('viewplayer.html',logged_in_user=logged_in_user, onePlayer=onePlayer, comments=comments)

@app.route("/search")
def searchplayers():
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    players= player.Player.get_all_players()
    return render_template('search.html', logged_in_user=logged_in_user, players=players)

@app.route('/addplayer')
def addplayer():
    if 'user_id' not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    return render_template('addplayer.html', logged_in_user = logged_in_user)

@app.route('/createplayer', methods=["POST"])
def createPlayer():
    if "user_id" not in session:
        return redirect('/')
    if player.Player.validate_player(request.form):
        player.Player.create_player(request.form)
        return redirect('/profile')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    return render_template("addplayer.html", logged_in_user=logged_in_user)

@app.route("/update/player/<int:id>", methods=["POST"])
def updatePlayer(id):
    if "user_id" not in session:
        return redirect('/')
    if player.Player.validate_player(request.form):
        player.Player.update_player(request.form)
        return redirect('/profile')
    return redirect(f"/view/{id}")

@app.route('/delete/<int:id>')
def deletePlayer(id):
    if "user_id" not in session:
        return redirect('/')
    player.Player.delete_player_by_id(id)
    return redirect('/profile')