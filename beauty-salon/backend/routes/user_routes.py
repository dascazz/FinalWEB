from flask import Blueprint, request, jsonify
from models import mysql

bp = Blueprint('user', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User registered successfully'})

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({'message': 'Login successful', 'role': user[3]})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Get all users
@bp.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify([{"id": user[0], "username": user[1], "role": user[2]} for user in users])

# Create a new user
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User created successfully'})

# Update a user
@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE users
        SET username = %s, password = %s, role = %s
        WHERE id = %s
    """, (username, password, role, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User updated successfully'})

# Delete a user
@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User deleted successfully'})
