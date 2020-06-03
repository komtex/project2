import os, requests
from datetime import timedelta
from collections import deque
from flask import Flask, flash, render_template, session, request, redirect, json
from flask_socketio import SocketIO, emit, send, join_room, leave_room, close_room, disconnect
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_ke"

""" app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=5) """

socketio = SocketIO(app)
# Keep track of channels created
Nchannels = []
# Keep track of users logged
users = []
# create an empty ditionary
Messages = dict()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    return render_template("index.html", channels=Nchannels)

@app.route("/signin", methods=['GET','POST'])
def signin():
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="Please fill username!")
        if username in users:
            return render_template("error.html", message="that username already exists!")
        users.append(username)
        session['username'] = username
        # the session cookie will expire after PERMANENT_SESSION_LIFETIME.
        session.permanent = True
        flash("You were successfully logged in", "success")
        return redirect("/")
    else:
        return render_template("signin.html")

@app.route("/logout", methods=['GET'])
def logout():
    try:
        users.remove(session['username'])
    except ValueError:
        pass
    session.clear()
    return redirect("/")

@app.route("/create", methods=['GET','POST'])
def create():
    # Get channel name from index.html
    newChannel = request.form.get("channel")
    if request.method == "POST":
        if newChannel in Nchannels:
            return render_template("error.html", message="that channel already exists!")
        Nchannels.append(newChannel)
        # https://stackoverflow.com/questions/53892422/python-ordered-list-of-dictionaries-with-a-size-limit
        Messages[newChannel] = deque()
        return redirect("/channels/" + newChannel)
    else:
        return render_template("/create", channels = Nchannels)

@app.route("/channels/<channel>", methods=['GET','POST'])
@login_required
def enter_channel(channel):
        # Updates user current channel
    session['current_channel'] = channel
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("channel.html", channels=Nchannels, messages=Messages[channel])

@socketio.on("joined", namespace = '/')
def joined():
    room = session.get('current_channel')
    join_room(room)
    emit('status', {
        'user': session.get('username'),
        'channel': room,
        'msg': session.get('username') + ' has entered the Room: ' + room},
        room=room)

@socketio.on("left", namespace = '/')
def on_leave():
    room = session.get('current_channel')
    leave_room(room)
    emit('status', {
        'user': session.get('username'),
        'channel': room,
        'msg': session.get('username') + ' Has left the Room:'},
        room=room)

@socketio.on('send message')
def send_msg(msg, timestamp):

    room = session.get('current_channel')
    # Save 100 messages and pass them when a user joins a specific channel.
    if len(Messages[room]) > 100:
        # Pop the oldest message
        Messages[room].popleft()
    Messages[room].append([timestamp, session.get('username'), msg])
    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg},
        room=room)

# Reset button for testing purposes
@socketio.on('reset')
def reset():
    users.clear()
    Nchannels.clear()
    Messages.clear()
