import csv
import flask_sqlalchemy
from app.models import Products, Reviews


def import_test_data(db: flask_sqlalchemy.SQLAlchemy):
    with open('./Products.csv') as products_file:
        reader = csv.reader(products_file)
        next(reader, None)
        for row in reader:
            new_product = Products(
                asin=row[1],
                title=row[0]
            )
            db.session.add(new_product)
    with open('./Reviews.csv') as reviews_file:
        reader = csv.reader(reviews_file)
        next(reader, None)
        for row in reader:
            product = Products.query.filter_by(asin=row[0]).first()
            new_review = Reviews(
                asin=row[0],
                title=row[1],
                text=row[2],
                product_id=product.id if product else None
            )
            db.session.add(new_review)
    db.session.commit()
