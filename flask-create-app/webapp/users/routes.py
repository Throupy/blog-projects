from flask import Blueprint

users = Blueprint("users", __name__)

@users.route("/users/login")
def login():
    return NotImplementedError("Add your implementation logic here")