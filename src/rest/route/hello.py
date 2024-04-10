from flask import Blueprint, jsonify

hello_route = Blueprint("hello_route", __name__)


@hello_route.get("/")
def say_hello():
    return jsonify("Hello", 200)
