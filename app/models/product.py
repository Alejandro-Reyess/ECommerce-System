class Product:
    def __init__(
        self,
        product_id,
        name,
        category,
        price,
        rating=0,
        review="",
    ):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.rating = rating
        self.review = review

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "review": self.review,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
