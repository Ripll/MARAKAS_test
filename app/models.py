import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(20))
    title = db.Column(db.Text())
    reviews = db.relationship('Reviews', backref='product', lazy="dynamic")

    def __repr__(self):
        return f"<Product ('{self.id}')>"


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(100))
    title = db.Column(db.String(250))
    text = db.Column(db.Text())
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)

    def __repr__(self):
        return f"<Review ('{self.id}')>"
