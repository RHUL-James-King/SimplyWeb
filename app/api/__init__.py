from flask import Blueprint
from flask_restplus import Api

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)

from app.api import handlers