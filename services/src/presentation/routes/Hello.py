from flask import Blueprint, jsonify

Hello = Blueprint("hello", __name__)


@Hello.get("/")
def say_hello():
    return jsonify("Welcome", 200)
