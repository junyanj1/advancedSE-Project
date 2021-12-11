from db.database import Database
from flask import abort
import requests
import json
import os
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from models.attendance import Attendance


class AttendanceController():
    def __init__(self, db: Database):
        self.db = db

    def get_attendances(self, event_id: str, invited=None, rsvped=None,
                        checked_in=None) -> list:
        """
        @param: event_id: str, required,
        @param: invited: bool,
        @param: rsvped: bool,
        @param: checked_in: bool
        @return: list of satisfying attendances

        Get list of attendees/rsvp/invited people of an event
        """
        if not event_id:
            return abort(400, "Missing event_id..")
        statement = "SELECT * FROM Attendance WHERE event_id = %s"
        param = [event_id]
        if invited is not None:
            statement += " AND is_invited = %s"
            param.append(invited)
        if rsvped is not None:
            statement += " AND is_rsvped = %s"
            param.append(rsvped)
        if checked_in is not None:
            statement += " AND is_checked_in = %s"
            param.append(checked_in)
        attendances = self.db.get(statement, param)
        resp = []
        for att in attendances:
            resp.append(Attendance(att["event_id"], att["user_email"],
                                   att["user_role"], att["personal_code"],
                                   att["is_invited"], att["is_rsvped"],
                                   att["is_checked_in"], att["created_at"],
                                   att["updated_at"]).to_dict())
        return resp

    def check_in(self, event_id: str, personal_code: str) -> dict:
        '''
        @param: event_id: str, required,
        @param: personal_code: str, required
        @return: updated row in Attendance

        This API is intended to be used by the attendee.
        When the user invokes this link, the server finds the user
        based on the personalized code and check this person in.
        '''
        if not event_id or not personal_code:
            return abort(400, "Missing event_id or personal_code..")
        query = """
                SELECT * FROM Attendance WHERE event_id = %s
                AND personal_code = %s
                """
        param = [event_id, personal_code]
        exist = self.db.get_one(query, param)
        if not exist:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")
        try:
            statement = "UPDATE Attendance \
                         SET is_checked_in = True \
                         WHERE event_id = %s \
                         AND personal_code = %s"
            self.db.set(statement, param)
        except (ForeignKeyViolation, UniqueViolation) as e:
            abort(400, e)

        updated = self.db.get_one(query, param)
        if not updated:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")

        return Attendance(updated["event_id"], updated["user_email"],
                          updated["user_role"], updated["personal_code"],
                          updated["is_invited"], updated["is_rsvped"],
                          updated["is_checked_in"], updated["created_at"],
                          updated["updated_at"]).to_dict()

    def invite(self, event_id: str, emails: list) -> list:
        '''
        @param: event_id: str, required,
        @param: emails: list

        Request event invites
        ** Question here: do we create new users if there are unknown emails?
        ** How to reduce costly queries?
        ** For iteration 1, all emails are linked to existing users.
        '''
        if not event_id:
            return abort(400, "Missing event_id..")
        query = """SELECT *
                   FROM Events
                   JOIN Users ON Users.user_id = Events.user_id
                   WHERE event_id = %s
                """
        exist = self.db.get_one(query, [event_id])
        if not exist:
            return abort(400, "The input event_id is invalid..")

        organizer_name = exist["username"]
        event_name = exist["event_name"]
        event_description = exist["event_description"]
        event_location = exist["event_location"]
        event_start_time = exist["event_start_time"].strftime(
            "%m/%d/%Y, %H:%M:%S")
        event_end_time = exist["event_end_time"].strftime(
            "%m/%d/%Y, %H:%M:%S")

        statement = """
                    INSERT INTO Attendance
                    VALUES (%s, %s, 'attendee',%s)
                    """
        failed = []
        for email in emails:
            personal_code = Attendance.generate_personal_code(event_id, email)
            try:
                self.db.set(statement, [event_id, email, personal_code])
            except (ForeignKeyViolation, UniqueViolation):
                failed.append(email)

            try:
                self.send_email(organizer_name, email, personal_code,
                                event_name, event_description, event_location,
                                event_start_time, event_end_time, event_id)
            except requests.exceptions.RequestException:
                failed.append(email)

        print("failed to invite: ", failed)
        return self.get_attendances(event_id, invited=True)

    def rsvp(self, event_id: str, personal_code: str) -> dict:
        '''
        @param: event_id: str, required,
        @param: personal_code: str, required
        @return: updated row in Attendance
        Questions: Can a user rsvp without a personal_code? A public link?
                   Do we want to give unrsvp option?
        '''
        if not event_id or not personal_code:
            return abort(400, "Missing event_id or personal_code..")
        query = "SELECT * FROM Attendance \
                 WHERE event_id = %s \
                 AND personal_code = %s"
        param = [event_id, personal_code]
        exist = self.db.get_one(query, param)
        if not exist:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")
        try:
            statement = "UPDATE Attendance \
                         SET is_rsvped = True \
                         WHERE event_id = %s \
                        AND personal_code = %s"
            self.db.set(statement, param)
        except (ForeignKeyViolation, UniqueViolation) as e:
            abort(400, e)

        updated = self.db.get_one(query, param)
        if not updated:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")

        return Attendance(updated["event_id"], updated["user_email"],
                          updated["user_role"], updated["personal_code"],
                          updated["is_invited"], updated["is_rsvped"],
                          updated["is_checked_in"], updated["created_at"],
                          updated["updated_at"]).to_dict()

    def unrsvp(self, event_id: str, personal_code: str) -> dict:
        '''
        @param: event_id: str, required,
        @param: personal_code: str, required
        @return: updated row in Attendance
        '''
        if not event_id or not personal_code:
            return abort(400, "Missing event_id or personal_code..")
        query = "SELECT * FROM Attendance \
                 WHERE event_id = %s \
                 AND personal_code = %s"
        param = [event_id, personal_code]
        exist = self.db.get_one(query, param)
        if not exist:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")
        try:
            statement = "UPDATE Attendance \
                         SET is_rsvped = False \
                         WHERE event_id = %s \
                         AND personal_code = %s"
            self.db.set(statement, param)
        except (ForeignKeyViolation, UniqueViolation) as e:
            abort(400, e)

        updated = self.db.get_one(query, param)
        if not updated:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")

        return Attendance(updated["event_id"], updated["user_email"],
                          updated["user_role"], updated["personal_code"],
                          updated["is_invited"], updated["is_rsvped"],
                          updated["is_checked_in"], updated["created_at"],
                          updated["updated_at"]).to_dict()

    @staticmethod
    def send_email(organizer_name: str, invitee_email: str,
                   personal_code: str, event_name: str,
                   event_description: str, event_location: str,
                   event_start_time: str, event_end_time: str,
                   event_id: str):
        apikey = os.getenv("MAILGUN_API", default="")
        maps_key = os.getenv("MAPS_API", default="")
        domain = "team-aapi.me"
        url = f"https://api.mailgun.net/v3/mg.{domain}/messages"
        location = str(event_location)[1:-1].split(',')[-1]
        location_query_string = location.replace(" ", "+")
        invite_link = (f"http://{domain}/static/attendee.html?"
                       f"event_id={event_id}&"
                       f"personal_code={personal_code}")

        return requests.post(
            url,
            auth=("api", apikey),
            data={"from": f"{organizer_name} <mailgun@mg.team-aapi.me>",
                  "to": f"{organizer_name} <mailgun@mg.team-aapi.me>",
                  "bcc": [invitee_email],
                  "subject": "You're invited!",
                  "template": "invite",
                  "h:X-Mailgun-Variables":
                      json.dumps(
                          {"invite_msg_body": "invite message body",
                           "organizer_name": organizer_name,
                           "invite_link": invite_link,
                           "event_name": event_name,
                           "event_description": event_description,
                           "event_location": location,
                           "event_start_time": event_start_time,
                           "event_end_time": event_end_time,
                           "embed_link": "https://maps.googleapis.com/" +
                           "maps/api/staticmap?" +
                           "zoom=13&size=600x300&maptype=roadmap&" +
                           "markers=color:blue%7C" +
                           f"label:Event%7C{location_query_string}" +
                           f"&key={maps_key}"
                           })}
        )
