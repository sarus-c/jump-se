import os
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from scraper import Scraper

load_dotenv()

app = Flask(__name__)
api = Api(app)
CORS(app)


class Task(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        search_urls = json_data['search_urls']
        rs = 'Error'

        if len(search_urls):
            try:
                data = Scraper(search_urls)
                load = requests.post(os.getenv('API_ITEMS'), json=data.items)
                if load.status_code in {200, 201}:
                    rs = 'Operation done!'
            except ValueError:
                rs = 'Error'

        return {'result': rs}


api.add_resource(Task, '/task', methods=['POST'])


def main():
    port = int(os.getenv('SERVER_PORT'))
    url = os.getenv('SERVER_URL')

    app.run(host=url, port=port, debug=True)


if __name__ == '__main__':
    main()
