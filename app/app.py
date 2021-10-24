from flask import Flask, jsonify
from flask_cors import CORS
import psycopg


app = Flask(__name__)
CORS(app)
conn = psycopg.connect('postgresql://postgres@db:5432/aapi')  # connect to DB


@app.route('/health')
def health():
    """Returns server status."""
    return jsonify(status='UP')


@app.route('/users')
def users():
    """Returns all Users."""
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM Users')
        return jsonify(cur.fetchall())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
