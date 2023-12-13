from flask import Blueprint, jsonify

hello = Blueprint("hello", __name__)


@hello.get("/")
def sayHello():
    return jsonify("Hello", 200)
