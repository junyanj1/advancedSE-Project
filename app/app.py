import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from controllers.attendance_controller import AttendanceController
from controllers.event_controller import EventController
from controllers.sample_controller import SampleController
from controllers.user_controller import UserController
from uwsgidecorators import postfork

from db.database import Database
from services.auth import AuthService


# Init app
app = Flask(__name__)
CORS(app)


# Error handling
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    try:
        json_data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
    except Exception:
        json_data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": str(e.description),
        })
    response.data = json_data
    response.content_type = "application/json"
    return response


class Context:
    def __init__(self):
        pool = Database.get_connection('postgresql://postgres@db:5432/aapi')
        self.db = Database(pool)
        self.auth = AuthService()
        self.attendance = AttendanceController(self.db)
        self.event = EventController(self.db)
        self.user = UserController(self.db, self.auth)
        self.sample = SampleController(self.db)


@postfork
def init():
    app.ctx = Context()


@app.route('/health')
def health():
    """Returns server status."""
    commit_id = os.getenv('COMMIT_ID', default='unknown')
    return jsonify(status='UP', commit_id=commit_id)


@app.route('/signin', methods=['POST'])
def signin():
    """POST /signin"""
    token = request.headers.get('aapi-token')
    return jsonify(app.ctx.user.get_user_by_token(token))


@app.route('/users', methods=['POST'])
def create_user():
    """POST /users"""
    data = request.json
    return jsonify(app.ctx.user.create_user(
        data.get("user_id"),
        data.get("org_name"),
        data.get("username"),
    ))


@app.route('/users/<user_id>')
def get_user(user_id):
    """GET /users/<user_id>"""
    app.ctx.auth.verify_request(request.headers, user_id)
    return jsonify(app.ctx.user.get_user(user_id))


@app.route('/users/<user_id>/events')
def get_user_events(user_id):
    """GET /users/<user_id>/events"""
    app.ctx.auth.verify_request(request.headers, user_id)
    return jsonify(app.ctx.user.get_user_events(user_id))


@app.route('/events', methods=['POST'])
def create_event():
    """POST /events"""
    data = request.json
    app.ctx.auth.verify_request(request.headers, data.get("user_id"))
    try:
        return jsonify(app.ctx.event.create_event(
            data.get("event_name"),  # "Winter Career Fair"
            data.get("user_id"),  # "asdasdas@asdasd.com"
            data.get("description"),  # "This is a winter career fair"
            data.get("location_name"),  # "Columbia University"
            data.get("address"),  # "2960 Broadway..."
            data.get("lat", None),  # 12.34  !NULLABLE
            data.get("long", None),  # 12.34  !NULLABLE
            data.get("start_time"),  # "2021-03-22 18:34"
            data.get("end_time"),  # "2021-03-22 20:34"
            data.get("attendee_limit"),  # 500
        ))
    except AttributeError as e:
        print(e)


@app.route('/events/<event_id>')
def get_event(event_id):
    """GET /events/<event_id>"""
    app.ctx.auth.verify_request(request.headers,
                                app.ctx.event.get_organizer_id(event_id))
    print('  get_eventapi')
    return jsonify(app.ctx.event.get_event(
        event_id,  # "abcdefghijklmn"
    ))


@app.route('/events/<event_id>/attendances')
def get_attendances(event_id):
    """GET /events/<event_id>/attendances"""
    app.ctx.auth.verify_request(request.headers,
                                app.ctx.event.get_organizer_id(event_id))
    return jsonify(app.ctx.attendance.get_attendances(
        event_id,  # "abcdefghijklmn"
        request.args.get('is_invited'),
        request.args.get('is_rsvped'),
        request.args.get('is_checked_in'),
    ))


@app.route('/events/<event_id>/invite', methods=['POST'])
def invite(event_id):
    """POST /events/<event_id>/invite"""
    app.ctx.auth.verify_request(request.headers,
                                app.ctx.event.get_organizer_id(event_id))
    emails = request.json.get('emails')
    return jsonify(app.ctx.attendance.invite(
        event_id,  # "abcdefghijklmn"
        emails,  # ["abc@abc.com", "def@def.com"]
    ))


@app.route('/events/<event_id>/rsvp/<personal_code>')
def rsvp(event_id, personal_code):
    """GET /events/<event_id>/rsvp/<personal_code>"""
    return jsonify(app.ctx.attendance.rsvp(
        event_id,  # "abcdefghijklmn"
        personal_code,  # "abcdefghijklmn"
    ))


@app.route('/events/<event_id>/unrsvp/<personal_code>')
def unrsvp(event_id, personal_code):
    """GET /events/<event_id>/unrsvp/<personal_code>"""
    return jsonify(app.ctx.attendance.unrsvp(
        event_id,  # "abcdefghijklmn"
        personal_code,  # "abcdefghijklmn"
    ))


@app.route('/events/<event_id>/check_in/<personal_code>')
def check_in(event_id, personal_code):
    """GET /events/<event_id>/check_in/<personal_code>"""
    return jsonify(app.ctx.attendance.check_in(
        event_id,  # "abcdefghijklmn"
        personal_code,  # "abcdefghijklmn"
    ))


@app.route('/sample/users')
def get_sample_users():
    return jsonify(app.ctx.sample.get_sample_users())


@app.route('/sample/users', methods=['POST'])
def create_sample_user():
    data = request.json
    return jsonify(app.ctx.sample.create_sample_user(
        data.get('email'),  # "abc@abc.com"
        data.get('username'),  # "Pikachu"
    ))


if __name__ == '__main__':
    # Only for dev
    app.run(host='0.0.0.0', port=3000)
