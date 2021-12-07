from base64 import b64encode


class Attendance:
    def __init__(self, event_id, user_email,
                 user_role, personal_code,
                 is_invited, is_rsvped, is_checked_in,
                 created_at, updated_at) -> None:
        self.event_id = event_id
        self.user_email = user_email
        self.user_role = user_role
        self.personal_code = personal_code
        self.is_invited = is_invited
        self.is_rsvped = is_rsvped
        self.is_checked_in = is_checked_in
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def generate_personal_code(event_id, user_email) -> str:
        # Generate personal_code with simple base64 encoding on utf-8
        return bytes(f'{event_id}:{user_email}', 'utf-8').hex()

    def to_dict(self) -> dict:
        return {
            'event_id': self.event_id,
            'user_email': self.user_email,
            'user_role': self.user_role,
            'personal_code': self.personal_code,
            'is_invited': self.is_invited,
            'is_rsvped': self.is_rsvped,
            'is_checked_in': self.is_checked_in,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
