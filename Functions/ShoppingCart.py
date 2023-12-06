class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"

class ShoppingCart:
    def __init__(self):
        self.cart = []

    def add_product(self, product, quantity=1):
        for item in self.cart:
            if item['product'] == product:
                item['quantity'] += quantity
                return
        self.cart.append({'product': product, 'quantity': quantity})

    def remove_product(self, product, quantity=1):
        for item in self.cart:
            if item['product'] == product:
                item['quantity'] = max(0, item['quantity'] - quantity)
                if item['quantity'] == 0:
                    self.cart.remove(item)
                return

    def modify_product_quantity(self, product, new_quantity):
        for item in self.cart:
            if item['product'] == product:
                item['quantity'] = new_quantity
                return

    def view_cart(self):
        total_cost = 0
        for item in self.cart:
            product = item['product']
            quantity = item['quantity']
            total_cost += product.price * quantity
            print(f"{product.name} - Quantity: {quantity}")
        print(f"Total cost: ${total_cost}")
