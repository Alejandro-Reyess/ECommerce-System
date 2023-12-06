class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ProductCatalog:
    def __init__(self, products):
        self.products = products

    def browse(self, sort_by=None, price_range=None):
        filtered_products = self.products

        # Filtering by price range
        if price_range:
            filtered_products = [product for product in filtered_products if price_range[0] <= product.price <= price_range[1]]

        # Sorting products
        if sort_by == 'low_to_high':
            filtered_products = sorted(filtered_products, key=lambda x: x.price)
        elif sort_by == 'high_to_low':
            filtered_products = sorted(filtered_products, key=lambda x: x.price, reverse=True)

        return filtered_products


