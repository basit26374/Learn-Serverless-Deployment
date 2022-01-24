from flask import Blueprint
from flask import current_app
from flask_restful import Api


count_bp = Blueprint('count_bp', __name__)
count_api = Api(count_bp)

from counter_app.views.count import GetCount, PostCount, SendCount, SendBulkCount, GenerateRandomCount, Response

count_api.add_resource(GetCount, '/count')
count_api.add_resource(PostCount, '/count')
count_api.add_resource(SendCount, '/send/count')
count_api.add_resource(SendBulkCount, '/send_bulk/count')
count_api.add_resource(GenerateRandomCount, '/generate/count')
count_api.add_resource(Response, '/async-response/<response_id>')