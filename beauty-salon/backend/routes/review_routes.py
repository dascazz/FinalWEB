from flask import Blueprint, request, jsonify
from models import mysql

bp = Blueprint('review', __name__)

@bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    username = data.get('username')
    review_text = data.get('review')

    if not all([username, review_text]):
        return jsonify({'message': 'Missing required parameters'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO review (username, review) VALUES (%s, %s)", (username, review_text))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Review created successfully'})

@bp.route('/reviews', methods=['GET'])
def get_all_reviews():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM review")
    review_records = cur.fetchall()
    cur.close()

    review_list = []
    for record in review_records:
        review_list.append({
            'id': record[0],
            'username': record[1],
            'review': record[2]
        })

    return jsonify(review_list)

@bp.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM review WHERE id = %s", (id,))
    review = cur.fetchone()
    cur.close()

    if review:
        return jsonify({'id': review[0], 'username': review[1], 'review': review[2]})
    else:
        return jsonify({'message': 'Review not found'}), 404

@bp.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM review WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Review deleted successfully'})
