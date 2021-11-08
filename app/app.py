import os
import time

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg


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
conn = connect_to_db()


@app.route('/health')
def health():
    """Returns server status."""
    commit_id = os.getenv('COMMIT_ID', default='unknown')
    return jsonify(status='UP', commit_id=commit_id)


@app.route('/users', methods=['GET', 'POST', 'PUT'])
def users():
    """Returns all Users."""
    if request.method == 'POST':
        with conn.cursor() as cur:
            data = request.json
            try:
                cur.execute('''
                    INSERT INTO Users (user_id, username) VALUES (%s, %s)
                    ''', (data['user_id'], data['username']))
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
                    UPDATE Users SET username = (%s) WHERE user_id = (%s)
                    ''', (data['username'], data['user_id']))
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
    # Only for dev
    app.run(host='0.0.0.0', port=3000)
