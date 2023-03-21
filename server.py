# Import Flask class from flask
from flask_app import app
from flask_app.controllers import users, players, comments

# We have to make sure that the file is being run directly and not from a different module
if __name__ == '__main__':
# If you were going to run it on a mac, you would need to specify the port number, but you do not have to on windows.
#   app.run(port =8000, debug = True)
    app.run(debug = True)