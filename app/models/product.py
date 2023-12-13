class Product:
    def __init__(
        self,
        product_id,
        name,
        category,
        price,
        review="",
        rating=0,
    ):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.review = review
        self.rating = rating

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "review": self.review,
            "rating": self.rating,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
