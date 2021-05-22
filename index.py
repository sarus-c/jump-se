import os
from flask import Flask, request, json
from werkzeug.exceptions import HTTPException
from flask_restful import Api, Resource
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from scraper import Scraper

load_dotenv()

app = Flask(__name__)
api = Api(app)
CORS(app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


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
            except HTTPException as e:
                rs = handle_exception(e)

        return {'result': rs}


api.add_resource(Task, '/task', methods=['POST'])


def main():
    port = int(os.getenv('SERVER_PORT'))
    url = os.getenv('SERVER_URL')

    app.run(host=url, port=port, debug=True)


if __name__ == '__main__':
    main()
