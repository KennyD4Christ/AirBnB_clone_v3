#!/usr/bin/python3
"""
Module defining the routes for version 1 of the API.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Route to return the status of the API.
    Returns:
        JSON: A JSON object with the status.
    """
    return jsonify({"status": "OK"})
