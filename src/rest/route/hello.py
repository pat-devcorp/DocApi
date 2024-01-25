from flask import Blueprint, jsonify

hello = Blueprint("hello", __name__)


@hello.get("/")
def say_hello():
    return jsonify("Hello", 200)
