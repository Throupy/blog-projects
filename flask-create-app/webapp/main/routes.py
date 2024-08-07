from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return NotImplementedError("Add your implementation logic here")