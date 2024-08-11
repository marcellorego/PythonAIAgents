import os
from dotenv import find_dotenv, load_dotenv
from waitress import serve
from controller import flask_app

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Load Server Port
SERVER_PORT = os.environ["SERVER_PORT"]

# Run the app
if __name__ == "__main__":
    print(f"Flask server running at port: {SERVER_PORT}")
    serve(flask_app, host="0.0.0.0", port=SERVER_PORT)