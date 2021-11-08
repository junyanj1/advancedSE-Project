import os
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg

from db.database import Database


# Init app
app = Flask(__name__)
CORS(app)


def connect_to_db(attempts=5):
    '''Returns a psycopg.Connection instance.'''
    while attempts:
        try:
            return psycopg.connect('postgresql://postgres@db:5432/aapi')
        except psycopg.errors.OperationalError:
            attempts -= 1
            print(f'DB connection failed, remaining attempts: {attempts}, ' +
                  f'reconnect in {(wait_time := 10 / attempts)} seconds')
            time.sleep(wait_time)
    raise Exception(f'DB Connection failed after {attempts} attempts')


# Connect to DB
db = Database()


@app.route('/health')
def health():
    """Returns server status."""
    commit_id = os.getenv('COMMIT_ID', default='unknown')
    return jsonify(status='UP', commit_id=commit_id)


@app.route('/users', methods=['GET', 'POST', 'PUT'])
def users():
    if request.method == 'POST':
        data = request.json
        try:
            db.set('INSERT INTO Users (user_id, username) VALUES (%s, %s)', (data['user_id'], data['username']))
            return 'OK', 200
        except Exception as ex:
            return str(ex), 400
    elif request.method == 'PUT':
        data = request.json
        try:
            db.set('UPDATE Users SET username = (%s) WHERE user_id = (%s)', (data['username'], data['user_id']))
            return 'OK', 200
        except Exception as ex:
            return str(ex), 400
    elif request.method == 'GET':
        result = db.get('SELECT * FROM Users')
        return jsonify(result)
    else:
        return 'Unknown method', 403


@app.route('/users/<id>')
def user(id):
    result = db.get_one('SELECT * FROM Users WHERE user_id = (%s)', (id,))
    return jsonify(result)


if __name__ == '__main__':
    # Only for dev
    app.run(host='0.0.0.0', port=3000)
