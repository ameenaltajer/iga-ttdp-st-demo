from flask import request
from flask import Flask
from database import *
app = Flask(__name__)

# Write the API to call the function in the database.py file to add a user and return all users in the database. The API should have two endpoints: one for adding a user and another for getting all users.


# Checkt the health of the database connection
@app.route("/db_health", methods=["GET"])
def db_health():
    try:
        conn = sqlite3.connect("example.db")
        conn.close()
        return {"message": "DB Online"}, 200
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}, 500



# Endpoint to add a user
@app.route("/add_user", methods=["POST"])
def add_user_api():
    data = request.get_json()
    name = data.get("name")
    add_user(name)
    return {"message": f"User {name} added"}, 200


# Endpoint to delete a user
@app.route("/delete_user", methods=["POST"])
def delete_user_api():
    data = request.get_json()
    user_id = data.get("id")
    delete_user(user_id)
    return {"message": f"User with id {user_id} deleted"}, 200

# Endpoint to get all users
@app.route("/get_users", methods=["GET"])
def get_users_api():
    users = get_all_users()
    return {"users": users}, 200





@app.route("/", methods=["GET"])
def hi():
    return {"message": "Ameen!"}, 200

if __name__ == "__main__":
    app.run(debug=True)

