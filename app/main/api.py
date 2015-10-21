from marshmallow import Schema
from flask import Blueprint
from ..models import Product

blueprint = Blueprint('api', __name__, url_prefix='/api',
						static_folder="../static")

@blueprint.route("/products/<int:farmerId>", methods=["GET"])
def api_products_by_farmer():
	products = Product.query.filter(Product.farmer_id == farmerId).all()
	return Schema(many=True).dump(products).data
