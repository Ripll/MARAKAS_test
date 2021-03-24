import logging
from flask import request
from . import create_app
from .models import db, Products, Reviews
from .utils.caching import make_cache_key

logging.basicConfig(level=logging.INFO)
app, cache = create_app()


@app.route('/endpoint', methods=['GET'])
@cache.cached(timeout=30, key_prefix=make_cache_key)
def get_data():
    """
    Returns the product and its reviews by ID or ASIN in the database
    ---
    tags:
      - Get product
    parameters:
      - name: id
        in: query
        type: integer
        description: Product ID from database
      - name: asin
        in: query
        type: string
        description: Product ASIN from database
      - name: page
        in: query
        type: integer
        description: Pagination for reviews
        schema:
            type: integer
            format: int64
            minimum: 1
            example: 1
      - name: count
        in: query
        type: integer
        description: Maximum number of reviews per page
        schema:
            type: integer
            format: int64
            minimum: 1
            example: 10
    responses:
      200:
        description: Product and its reviews
    """
    logging.info(f"GET request with params: {request.args}")

    filters = {}
    if prod_id := request.args.get('id'):
        filters['id'] = prod_id
    elif prod_asin := request.args.get('asin'):
        filters['asin'] = prod_asin
    else:
        logging.info("Product ID or ASIN must be specified")
        return {"error": "Product ID or ASIN must be specified",
                "result": False}

    product = Products.query.filter_by(**filters).first()

    try:
        page = int(request.args.get('page', 1))
        count = int(request.args.get('count', 10))
        if page <= 0 or count <= 1:
            raise
    except Exception as e:
        logging.error(e, exc_info=True)
        logging.info("Page and count should be positive integer")
        return {"error": "Page and count should be positive integer",
                "result": False}

    reviews = product.reviews.limit(count).offset((page-1)*count).all()

    result = {
        "id": product.id,
        "asin": product.asin,
        "title": product.title,
        "reviews": {
            "page": page,
            "count": count,
            "data": [{"id": review.id,
                      "title": review.title,
                      "text": review.text} for review in reviews]
        },
        "result": True
    }

    return result


@app.route('/endpoint', methods=['PUT'])
def new_review():
    """
    Adds a new review to the product and returns the review ID in the database
    ---
    tags:
      - New review
    parameters:
      - name: product_id
        in: query
        type: integer
        required: true
        description: Product ID
      - name: title
        in: query
        type: string
        required: true
        description: Review title
      - name: text
        in: query
        type: string
        required: true
        description: Review text
    responses:
      200:
        description: New review id
    """

    product = Products.query.get(request.args.get('product_id'))
    if not product:
        return {"error": "Incorrect product ID",
                "result": False}
    if request.args.get('title') and request.args.get('text'):
        new_rev = Reviews(asin=product.asin,
                          title=request.args.get('title'),
                          text=request.args.get('text'),
                          product_id=product.id)
        db.session.add(new_rev)
        db.session.commit()
        return {"review_id": new_rev.id,
                "result": True}
    else:
        return {"error": "Text or title are unspecified",
                "result": False}
