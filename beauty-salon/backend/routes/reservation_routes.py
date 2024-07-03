# backend/routes/reservation_routes.py

from flask import Blueprint, request, jsonify
from models import mysql
from datetime import timedelta

bp = Blueprint('reservation', __name__)

@bp.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    full_name = data.get('fullName')
    phone_number = data.get('phoneNumber')
    guests = data.get('guests')
    date = data.get('date')
    time = data.get('time')
    service = data.get('service')

    if not all([full_name, phone_number, guests, date, time, service]):
        return jsonify({'message': 'Missing required parameters'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO reservations (full_name, phone_number, guests, date, time, service) VALUES (%s, %s, %s, %s, %s, %s)", 
                (full_name, phone_number, guests, date, time, service))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Reservation created successfully'})

@bp.route('/reservations', methods=['GET'])
def get_all_reservations():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reservations")
    reservation_records = cur.fetchall()
    cur.close()

    reservation_list = []
    for record in reservation_records:
        reservation_list.append({
            'id': record[0],
            'full_name': record[1],
            'phone_number': record[2],
            'guests': record[3],
            'date': record[4].strftime('%Y-%m-%d'),  # format date as string
            'time': str(record[5]),  # convert timedelta to string
            'service': record[6]
        })

    return jsonify(reservation_list)

@bp.route('/reservations/<int:id>', methods=['GET'])
def get_reservation(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reservations WHERE id = %s", (id,))
    reservation = cur.fetchone()
    cur.close()

    if reservation:
        return jsonify({'id': reservation[0], 'full_name': reservation[1], 'phone_number': reservation[2], 'guests': reservation[3], 'date': reservation[4].strftime('%Y-%m-%d'), 'time': str(reservation[5]), 'service': reservation[6]})
    else:
        return jsonify({'message': 'Reservation not found'}), 404

@bp.route('/reservations/<int:id>', methods=['DELETE'])
def delete_reservation(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM reservations WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Reservation deleted successfully'})
