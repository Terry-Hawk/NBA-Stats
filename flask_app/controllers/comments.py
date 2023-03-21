from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, comment, player

# Create route for the landing page of the website. This will eventually be the login and registration page
@app.route('/createcomment', methods=["POST"])
def createComment():
    if "user_id" not in session:
        return redirect('/')
    comment.Comment.create_comment(request.form)
    return redirect("/activity")

@app.route('/deleteComment/<int:id>')
def deleteComment(id):
    if "user_id" not in session:
        return redirect('/')
    comment.Comment.delete_comment_by_id(id)
    return redirect('/activity')

@app.route("/editComment/<int:id>")
def viewComment(id):
    if "user_id" not in session:
        return redirect('/')
    logged_in_user = user.User.get_user_by_id(session["user_id"])
    comments = comment.Comment.get_comment_by_id(id)
    return render_template('editcomment.html',logged_in_user=logged_in_user,comments=comments)

@app.route("/comment/update/<int:id>", methods=["POST"])
def updateComment(id):
    if "user_id" not in session:
        return redirect("/")
    comment.Comment.update_comment(request.form)
    return redirect('/activity')
