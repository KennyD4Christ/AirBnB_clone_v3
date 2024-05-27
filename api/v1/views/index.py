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


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Route to return the number of each object type.
    Returns:
        JSON: A JSON object with the counts of each object type.
    """
    counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(counts)
