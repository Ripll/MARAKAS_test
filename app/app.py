import logging
from flask import request
from . import create_app
from .models import Products, Reviews
from .utils.caching import make_cache_key

logging.basicConfig(level=logging.INFO)
app, cache = create_app()


@app.route('/endpoint', methods=['GET'])
@cache.cached(timeout=30, key_prefix=make_cache_key)
def get_data():
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
    except:
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



