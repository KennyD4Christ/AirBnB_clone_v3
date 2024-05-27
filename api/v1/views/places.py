#!/usr/bin/python3
"""
Module containing views for Place objects.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity  # noqa 184


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Searches for Place objects based on JSON request"""
    if not request.json:
        abort(400, 'Not a JSON')

    # Get JSON data from request
    json_data = request.json

    # Extract states, cities, and amenities lists from JSON
    states = json_data.get('states', [])
    cities = json_data.get('cities', [])
    amenities = json_data.get('amenities', [])

    # Initialize list to store filtered places
    filtered_places = []

    # If states and cities lists are empty, retrieve all places
    if not states and not cities:
        filtered_places = storage.all(Place).values()
    else:
        # Get places based on states
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city not in filtered_places:
                        filtered_places.extend(city.places)

        # Get places based on cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in filtered_places:
                filtered_places.extend(city.places)

    # Filter places based on amenities
    if amenities:
        filtered_places = [place for place in filtered_places if all(
            amenity_id in place.amenities for amenity_id in amenities
        )]
    # Convert filtered places to dictionary representation
    places_dict = [place.to_dict() for place in filtered_places]

    return jsonify(places_dict)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
