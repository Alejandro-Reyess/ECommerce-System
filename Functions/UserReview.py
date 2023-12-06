class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.reviews = []

    def write_review(self, product, rating, comment):
        review = Review(self, product, rating, comment)
        self.reviews.append(review)
        product.add_review(review)


class Product:
    def __init__(self, product_id, name):
        self.product_id = product_id
        self.name = name
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def get_average_rating(self):
        if not self.reviews:
            return 0
        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews)


class Review:
    def __init__(self, user, product, rating, comment):
        self.user = user
        self.product = product
        self.rating = rating
        self.comment = comment