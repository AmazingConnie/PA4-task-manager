from flask import Blueprint, jsonify, request
from services.products import create_product
from services.tags import create_tag
from services.tasks import get_task, create_task, process_order, update_task, get_tasks_by_priority
from services.users import get_user, get_pref, update_pref
from utils.errors import AppError

api = Blueprint("api", __name__)

@api.errorhandler(AppError)
def handle_app_error(e):
    return jsonify({"error": e.message}), e.status_code

@api.route("/tasks/<int:task_id>", methods=["GET"])
def get_task_route(task_id):
    return jsonify(get_task(task_id))

@api.route("/tasks", methods=["GET"])
def list_tasks_by_priority_route():
    return jsonify(get_tasks_by_priority(request.args.get("priority", type=int)))

@api.route("/tasks", methods=["POST"])
def create_task_route():
    data = request.get_json()
    return jsonify(create_task(data["title"], data["user_id"], data.get("priority", 3))), 201

@api.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task_route(task_id):
    data = request.get_json(silent=True) or {}
    return jsonify(update_task(task_id, data.get("priority")))

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    return jsonify(get_user(user_id))

@api.route("/users/<int:user_id>/notifications", methods=["GET"])
def get_pref_route(user_id):
    return jsonify({"notification_pref": get_pref(user_id)})

@api.route("/users/<int:user_id>/notifications", methods=["PATCH"])
def update_pref_route(user_id):
    data = request.get_json(silent=True) or {}
    return jsonify(update_pref(user_id, data.get("notification_pref")))

@api.route("/products", methods=["POST"])
def create_product_route():
    data = request.get_json(silent=True) or {}
    return jsonify(create_product(data.get("name"), data.get("price"))), 201

@api.route("/tags", methods=["POST"])
def create_tag_route():
    data = request.get_json(silent=True) or {}
    return jsonify(create_tag(data.get("name"))), 201
