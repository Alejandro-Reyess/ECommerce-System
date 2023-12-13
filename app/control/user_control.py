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
        with open(file_path, "r+") as file:
            data = json.load(file)
            file.seek(0)
            for user in self.users:
                existing_user = next(
                    (u for u in data if u["username"] == user.username), None
                )
                if existing_user:
                    existing_user.update(user.to_dict())
                else:
                    data.append(user.to_dict())
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

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

    def finalize_order(self, username, order):
        for user in self.users:
            if user.username == username:
                user.add_order_to_history(order)
                self.save_users()
                return True
        return False

    def load_status(self):
        for order in self.orders:
            if order.order_number == self.order_number:
                self.status = order.status
                break
