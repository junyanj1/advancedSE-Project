class User:
    def __init__(self, user_id, org_name, username):
        self.user_id = user_id
        self.org_name = org_name
        self.username = username

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'org_name': self.org_name,
            'username': self.username
        }
