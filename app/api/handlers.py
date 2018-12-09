from app.api import api
from flask_restplus import Resource
from datetime import datetime


@api.route('/')
@api.route('/index')
class Index(Resource):

    def get(self):
        return {'message': "Welcome to the Simply Poetry API, get daily poems curated by the team",
                'api_endpoints': [
                    {'uri': '/poem/<date>', 'method': "GET", 'description': "Get the poem on the passed date,"
                                                                            " defaults to todays date"},
                ]}


@api.route('/poem', defaults={'release_date': datetime.now().date()})
@api.route('/poem/<date:release_date>')
class Poem(Resource):

    def get(self, release_date):
        return {'author': "James King",
                'poem': "Hello World",
                'date': str(release_date)}
