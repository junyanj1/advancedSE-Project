from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg


app = Flask(__name__)
CORS(app)
conn = psycopg.connect('postgresql://postgres@db:5432/aapi')  # connect to DB


@app.route('/health')
def health():
    """Returns server status."""
    return jsonify(status='UP')


@app.route('/users', methods=['GET', 'POST', 'PUT'])
def users():
    """Returns all Users."""
    if request.method == 'POST':
        with conn.cursor() as cur:
            data = request.json
            try:
                cur.execute('''
                    INSERT INTO Users (userID, username) VALUES (%s, %s)
                    ''', (data['userID'], data['username']))
            except BaseException as ex:
                conn.rollback()
                return str(ex), 400
            else:
                conn.commit()
                return 'OK', 200
    elif request.method == 'PUT':
        with conn.cursor() as cur:
            data = request.json
            try:
                cur.execute('''
                    UPDATE Users SET username = (%s) WHERE userID = (%s)
                    ''', (data['username'], data['userID']))
            except BaseException as ex:
                conn.rollback()
                return str(ex), 400
            else:
                conn.commit()
            return 'OK', 200
    elif request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM Users')
            return jsonify(cur.fetchall())
    else:
        return 'Unknown method', 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
