Web Programming with Python and JavaScript
Requirements
In this project, you’ll build an online messaging service using Flask, similar in spirit to Slack. Users will be able to sign into your site with a display name, create channels (i.e. chatrooms) to communicate in, as well as see and join existing channels. Once a channel is selected, users will be able to send and receive messages with one another in real time. Finally, you’ll add a personal touch to your chat application of your choosing!
Here are the requirements:

    Display Name: When a user visits your web application for the first time, they should be prompted to type in a display name that will eventually be associated with every message the user sends. If a user closes the page and returns to your app later, the display name should still be remembered.
    Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel.
    Channel List: Users should be able to see a list of all current channels, and selecting one should allow the user to view the channel. We leave it to you to decide how to display such a list.
    Messages View: Once a channel is selected, the user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. Your app should only store the 100 most recent messages per channel in server-side memory.
    Sending Messages: Once in a channel, users should be able to send text messages to others the channel. When a user sends a message, their display name and the timestamp of the message should be associated with the message. All users in the channel should then see the new message (with display name and timestamp) appear on their channel page. Sending and receiving messages should NOT require reloading the page.
    Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes back to your web application, your application should remember what channel the user was on previously and take the user back to that channel.
    Personal Touch: Add at least one additional feature to your chat application of your choosing! Feel free to be creative, but if you’re looking for ideas, possibilities include: supporting deleting one’s own messages, supporting use attachments (file uploads) as messages, or supporting private messaging between two users.
    In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project. Also, include a description of your personal touch and what you chose to add to the project.
    If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!
Beyond these requirements, the design, look, and feel of the website are up to you! You’re also welcome to add additional features to your website, so long as you meet the requirements laid out in the above specification!
# Project 2
My project represents a  simple webchat application. Its server-side(application.py) is stick with the typical flask approach of rendering templates using jinja2 with Flask-SocketIO and client-side(channel.js), that is written with javascript socketIO which enables real-time bidirectional communication with back-end(server).
Some features include:
    signing in with a username
    Multiple users can join a chat room by each entering a unique username on website load.    
    A notification is sent to all users when a user joins or leaves the chatroom.
    ability to create channels(rooms)
    sending messages within channels(rooms)
    messages and channel additions appear in realtime for all users viewing the page
    username and timestamp displayed with every message
    remembering the channel which the user was last on if the page is closed and reopened
When a user specifies a username, it is then stored in localStorage. Similarly, current channel name that user joined last time is also stored in localStorage.
flask_socketio is a library that allows for websockets inside a Flask application. This library allows for the web server and client to be emitting events to all other users, while also listening for and receiving events being broadcasted by others.
Personal touch

- Use a function ValidInput which prevent empty inputs being existing.
- A flash messege is displayed for successfully log in.
- CSS animation with two move effects and javascript to modify properties: animationPlayState.
