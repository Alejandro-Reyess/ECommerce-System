class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.discount = 0  # default discount is 0%

    def apply_discount(self, discount_percent):
        if 0 <= discount_percent <= 100:
            self.discount = discount_percent
            print(f"Discount of {discount_percent}% applied to {self.name}.")
        else:
            print(
                "Invalid discount percentage. Please provide a percentage between 0 and 100."
            )

    def get_discounted_price(self):
        discounted_price = self.price * (1 - self.discount / 100)
        return discounted_price

    def display_info(self):
        print(f"Product: {self.name}")
        print(f"Original Price: ${self.price}")
        print(f"Discount: {self.discount}%")
        print(f"Discounted Price: ${self.get_discounted_price()}")
        print()


class DiscountManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        print(f"Product '{product.name}' added to the discount manager.")

    def create_promotion(self, product, discount_percent):
        product.apply_discount(discount_percent)

    def display_all_products(self):
        print("All Products in Discount Manager:")
        for product in self.products:
            product.display_info()
