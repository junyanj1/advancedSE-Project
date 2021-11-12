import uuid
import base64
import re

class User:
    def __init__(self, org_id, username, email, user_id=None):
        if user_id is None:
            self.generate_id()
        else:
            self.user_id = user_id
        self.org_id = org_id
        self.username = username
        self.email = email
    
    def generate_id(self):
        self.user_id = re.sub("[^0-9a-zA-Z]+", "", str(base64.b64encode(uuid.uuid4().bytes)))

    def to_dict(self):
        return {
            'organization_id': self.org_id, 
            'username': self.username,
            'email': self.email,
            'user_id': self.user_id, 
        }