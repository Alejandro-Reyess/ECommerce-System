from models.product import Product


class Order:
    order_counter = 0

    def __init__(
        self, products, total_price, address, card_number, exp_date, cvv, card_name
    ):
        Order.order_counter += 1
        self.order_number = Order.order_counter
        self.products = products
        self.total_price = total_price
        self.address = address
        self.card_number = card_number
        self.exp_date = exp_date
        self.cvv = cvv
        self.card_name = card_name
        self.status = "Payment Approved - Product Shipped - Awaiting Receipt"

    def to_dict(self):
        products_data = [
            product.to_dict() if hasattr(product, "to_dict") else product
            for product in self.products
        ]
        return {
            "order_number": self.order_number,
            "products": products_data,
            "total_price": self.total_price,
            "address": self.address,
            "card_number": self.card_number,
            "exp_date": self.exp_date,
            "cvv": self.cvv,
            "card_name": self.card_name,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        order_number = data.get("order_number")
        products = [
            Product.from_dict(product_data) for product_data in data.get("products", [])
        ]
        total_price = data.get("total_price")
        address = data.get("address")
        card_number = data.get("card_number")
        exp_date = data.get("exp_date")
        cvv = data.get("cvv")
        card_name = data.get("card_name")
        status = data.get(
            "status", "Payment Approved - Product Shipped - Awaiting Receipt"
        )

        return cls(
            products,
            total_price,
            address,
            card_number,
            exp_date,
            cvv,
            card_name,
            status=status,
            order_number=order_number,
        )

    def add_order(self, order):
        self.orders.append(order)

    def get_status(self):
        return self.status

    def confirm_receipt(self):
        self.status = "Payment Approved - Product Shipped - Product Received"

    def load_status(self):
        for order in self.orders:
            if order.order_number == self.order_number:
                self.status = order.status
                break
