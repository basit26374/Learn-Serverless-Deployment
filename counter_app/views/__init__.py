from flask import Blueprint
from flask import current_app
from flask_restful import Api
from counter_app.views.count import GetCount, PostCount, SendCount


count_bp = Blueprint('count_bp', __name__)
count_api = Api(count_bp)

count_api.add_resource(GetCount, '/count')
count_api.add_resource(PostCount, '/count')
count_api.add_resource(SendCount, '/send/count')