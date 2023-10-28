
from flask_login import current_user

class UsersPolicy:
    def __init__(self, record):
        self.record = record

    def create(self):
        return current_user.is_admin

    def delete(self):
        return current_user.is_admin

    def show(self):
        return True
    
    def update(self):
        return current_user.is_moder
    
    def show_collections(self):
        if not current_user.is_moder and not current_user.is_admin:
            # if current_user.id == self.record.id:
            return True