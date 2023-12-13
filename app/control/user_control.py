import json
import os
from models.user import User


class UserControl:
    def __init__(self):
        self.users = []
        self.load_users()

    def get_directory(self):
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "db", "users.json")
        )

    def load_users(self):
        try:
            file_path = self.get_directory()
            with open(file_path, "r") as file:
                data = file.read()
                if data:
                    self.users = [User(**user) for user in json.loads(data)]
                else:
                    self.users = []
        except FileNotFoundError:
            open(file_path, "w").close()
            self.users = []

    def get_user_info(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def save_users(self):
        file_path = self.get_directory()
        with open(file_path, "w") as file:
            data = [user.to_dict() for user in self.users]
            json.dump(data, file, indent=4)

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def create_user(self, name, email, address, username, password):
        new_user = User(name, email, address, username, password)
        self.users.append(new_user)
        self.save_users()
        return new_user

    def edit_user(self, username, new_data):
        for user in self.users:
            if user.username == username:
                for key, value in new_data.items():
                    setattr(user, key, value)
                self.save_users()
                return True
        return False

    def add_to_cart(self, product):
        if product in self.cart:
            self.cart[product] += 1
        else:
            self.cart[product] = 1

    def remove_from_cart(self, product):
        if product in self.cart:
            if self.cart[product] > 1:
                self.cart[product] -= 1
            else:
                del self.cart[product]

    def clear_cart(self):
        self.cart = {}
