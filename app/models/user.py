from models.order import Order


class User:
    def __init__(
        self, name, email, address, username, password, cart=None, orders=None
    ):
        self.name = name
        self.email = email
        self.address = address
        self.username = username
        self.password = password
        self.cart = cart if cart is not None else {}
        self.orders = orders if orders is not None else []

    def to_dict(self):
        cart_dict = {
            str(product): product.to_dict() if hasattr(product, "to_dict") else product
            for product in self.cart.values()
        }
        orders_list = []
        for order in self.orders:
            if isinstance(order, dict):
                orders_list.append(order)
            elif hasattr(order, "to_dict"):
                orders_list.append(order.to_dict())
            else:
                orders_list.append(order)
        return {
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "username": self.username,
            "password": self.password,
            "cart": cart_dict,
            "orders": orders_list,
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            name=data.get("name"),
            email=data.get("email"),
            address=data.get("address"),
            username=data.get("username"),
            password=data.get("password"),
        )
        user.cart = data.get("cart", {})

        orders_data = data.get("orders", [])
        user.orders = []
        for order_data in orders_data:
            order = Order.from_dict(order_data)
            user.add_order(order)
        return user

    def add_order(self, order):
        self.orders.append(order)

    def load_status(self):
        for order in self.orders:
            if order.order_number == self.order_number:
                self.status = order.status
                break
