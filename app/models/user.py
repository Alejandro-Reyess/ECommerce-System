class User:
    def __init__(self, name, email, address, username, password):
        self.name = name
        self.email = email
        self.address = address
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "username": self.username,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
