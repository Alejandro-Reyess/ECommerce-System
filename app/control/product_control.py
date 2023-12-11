import json
import os
from models.product import Product


class ProductControl:
    def __init__(self, products):
        self.products = products

    def get_directory(self):
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "db", "products.json")
        )

    def load_products(self):
        try:
            file_path = self.get_directory()
            with open(file_path, "r") as file:
                data = file.read()
                if data:
                    self.products = [Product(**product) for product in json.loads(data)]
                else:
                    self.products = []
        except FileNotFoundError:
            open(file_path, "w").close()
            self.products = []

    def save_products(self):
        file_path = self.get_directory()
        with open(file_path, "w") as file:
            data = [product.to_dict() for product in self.products]
            json.dump(data, file, indent=4)

    def create_product(self, product_id, name, category, price):
        for product in self.products:
            if product.product_id == product_id or product.name == name:
                return False

        new_product = Product(product_id, name, category, price)
        self.products.append(new_product)
        self.save_products()
        return True

    def edit_product(self, product_id, name, category, price):
        for product in self.products:
            if product.product_id == product_id:
                product.name = name
                product.category = category
                product.price = price
                self.save_products()
                return True
        return False

    def delete_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                self.save_products()
                return True
        return False
