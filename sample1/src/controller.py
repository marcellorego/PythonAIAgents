from flask import Flask, request
from slack import slack_handler

# Initialize the Flask web app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)

@flask_app.route("/hello")
def hello():
    return "<p>Hello World</p>"


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return slack_handler.handle(request)