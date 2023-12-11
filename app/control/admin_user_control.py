import json
import os
from models.admin_user import AdminUser


class AdminUserControl:
    def __init__(self):
        self.admin_users = []
        self.load_admin_users()

    def get_directory(self):
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "db", "admin_users.json")
        )

    def load_admin_users(self):
        try:
            file_path = self.get_directory()
            with open(file_path, "r") as file:
                data = file.read()
                if data:
                    self.admin_users = [
                        AdminUser(**admin_user) for admin_user in json.loads(data)
                    ]
                else:
                    self.users = []
        except FileNotFoundError:
            open(file_path, "w").close()
            self.admin_users = []

    def save_admin_users(self):
        file_path = self.get_directory()
        with open(file_path, "w") as file:
            data = [admin_user.to_dict() for admin_user in self.admin_users]
            json.dump(data, file, indent=4)

    def authenticate_admin(self, username, password):
        for admin_user in self.admin_users:
            if admin_user.username == username and admin_user.password == password:
                return True
        return False

    def create_admin_user(self, username, password):
        new_admin_user = AdminUser(username, password)
        self.admin_users.append(new_admin_user)
        self.save_admin_users()
        return new_admin_user
