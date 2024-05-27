#!/usr/bin/python3
"""
Module containing the Flask application for version 1 of the API.
"""
from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)

# Create a CORS instance allowing /* for 0.0.0.0
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown method to close the current SQLAlchemy session.
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a JSON response.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
