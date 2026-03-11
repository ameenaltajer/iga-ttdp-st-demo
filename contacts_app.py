import re
import sqlite3
from flask import Flask, jsonify, request
 
from contacts_db import (
    init_db,
    get_all_contacts,
    add_contact,
    get_contact_by_id,
    update_contact,
    delete_contact,
    search_contacts,
)
 
app = Flask(__name__)
 
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
 
 
def is_valid_email(email):
    return bool(EMAIL_RE.match(email))
 
 
@app.route("/contacts", methods=["GET"])
def list_contacts():
    return jsonify(get_all_contacts()), 200
 
 
@app.route("/contacts", methods=["POST"])
def create_contact():
    data = request.get_json(silent=True) or {}
 
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
 
    if not name or not email or not phone:
        return jsonify({"error": "name, email, and phone are required"}), 400
 
    if not is_valid_email(email):
        return jsonify({"error": "invalid email"}), 400
 
    try:
        contact_id = add_contact(name, email, phone)
    except sqlite3.IntegrityError:
        return jsonify({"error": "email already exists"}), 409
 
    contact = get_contact_by_id(contact_id)
    return jsonify(contact), 201
 
 
@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    #contact = get_contact_by_id(contact_id)
    if not contact:
        return jsonify({"error": "contact not found"}), 404
    return jsonify(contact), 200
 
 
@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact_route(contact_id):
    existing = get_contact_by_id(contact_id)
    if not existing:
        return jsonify({"error": "contact not found"}), 404
 
    data = request.get_json(silent=True) or {}
 
    name = data.get("name", existing["name"])
    email = data.get("email", existing["email"])
    phone = data.get("phone", existing["phone"])
 
    if not name or not email or not phone:
        return jsonify({"error": "name, email, and phone are required"}), 400
 
    if not is_valid_email(email):
        return jsonify({"error": "invalid email"}), 400
 
    try:
        update_contact(contact_id, name, email, phone)
    except sqlite3.IntegrityError:
        return jsonify({"error": "email already exists"}), 409
 
    return jsonify(get_contact_by_id(contact_id)), 200
 
 
@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact_route(contact_id):
    deleted = delete_contact(contact_id)
    if not deleted:
        return jsonify({"error": "contact not found"}), 404
    return jsonify({"message": "contact deleted"}), 200
 
 
@app.route("/contacts/search", methods=["GET"])
def search_contacts_route():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "query parameter q is required"}), 400
    return jsonify(search_contacts(query)), 200
 
 
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
