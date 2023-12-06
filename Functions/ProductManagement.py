class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"

class ProductManager:
    def __init__(self):
        self.products = []
        self.admins = []  # Assume admins are identified by their usernames

    def add_product(self, admin_username, product):
        if admin_username in self.admins:
            self.products.append(product)
            print(f"Product '{product.name}' added to the inventory.")
        else:
            print("Unauthorized: You don't have admin privileges.")

    def edit_product(self, admin_username, product_name, new_price):
        if admin_username in self.admins:
            for product in self.products:
                if product.name == product_name:
                    product.price = new_price
                    print(f"Product '{product_name}' edited. New price: ${new_price}")
                    return
            print(f"Product '{product_name}' not found.")
        else:
            print("Unauthorized: You don't have admin privileges.")

    def remove_product(self, admin_username, product_name):
        if admin_username in self.admins:
            for product in self.products:
                if product.name == product_name:
                    self.products.remove(product)
                    print(f"Product '{product_name}' removed from the inventory.")
                    return
            print(f"Product '{product_name}' not found.")
        else:
            print("Unauthorized: You don't have admin privileges.")
