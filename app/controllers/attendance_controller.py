from db.database import Database
from flask import abort
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

    def check_in(self, event_id: str, personal_code: str) -> None:
        '''
        @param: event_id: str, required,
        @param: personal_code: str, required

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
        except (ForeignKeyViolation, UniqueViolation):
            abort(400, 'Invalid parameter value')

        return self.db.get_one(query, param)

    def invite(self, event_id: str, emails: list) -> None:
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
        query = "SELECT * FROM Event WHERE event_id = %s"
        exist = self.db.get(query, [event_id])
        if not exist:
            return abort(400, "The input event_id is invalid..")
        statement = """
                    INSERT INTO Attendance
                    (event_id, user_email, personal_code, is_invited)
                    VALUES (%s, %s, %s, True)
                    """
        failed = []
        for email in emails:
            personal_code = Attendance.generate_personal_code(event_id, email)
            try:
                self.db.set(statement, [event_id, email, personal_code])
            except (ForeignKeyViolation, UniqueViolation):
                failed.append(email)
        print("failed to invite: ", failed)

    def rsvp(self, event_id: str, personal_code: str) -> None:
        '''
        @param: event_id: str, required,
        @param: personal_code: str, required
        Questions: Can a user rsvp without a personal_code? A public link?
                   Do we want to give unrsvp option?
        '''
        if not event_id or not personal_code:
            return abort(400, "Missing event_id or personal_code..")
        query = "SELECT * FROM Attendance \
                 WHERE event_id = %s \
                 AND personal_code = %s"
        param = [event_id, personal_code]
        exist = self.db.get(query, param)
        if not exist:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")
        try:
            statement = "UPDATE Attendance \
                         SET is_rsvped = True \
                         WHERE event_id = %s \
                        AND personal_code = %s"
            self.db.set(statement, param)
        except (ForeignKeyViolation, UniqueViolation):
            abort(400, 'Invalid parameter value')
        return None

    def unrsvp(self, event_id: str, personal_code: str) -> None:
        '''
        @param: event_id: str, required,
        @param: personal_code: str, required
        '''
        if not event_id or not personal_code:
            return abort(400, "Missing event_id or personal_code..")
        query = "SELECT * FROM Attendance \
                 WHERE event_id = %s \
                 AND personal_code = %s"
        param = [event_id, personal_code]
        exist = self.db.get(query, param)
        if not exist:
            return abort(400, "The input event_id-personal_code \
                               combination is invalid..")
        try:
            statement = "UPDATE Attendance \
                         SET is_rsvped = False \
                         WHERE event_id = %s \
                         AND personal_code = %s"
            self.db.set(statement, param)
        except (ForeignKeyViolation, UniqueViolation):
            abort(400, 'Invalid parameter value')
        return None
