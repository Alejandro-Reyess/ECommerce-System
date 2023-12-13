class User:
    def __init__(self, name, email, address, username, password):
        self.name = name
        self.email = email
        self.address = address
        self.username = username
        self.password = password
        self.cart = {}

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "username": self.username,
            "password": self.password,
            "cart": self.cart,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(**data)
        user.cart = data.get("cart", {})
        return user

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
