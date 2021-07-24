# MANUAL:
# Run the main file "avantionary.py to run the api. Do not run api.py
# The url to the API is http://127.0.0.1:5000/
# as at this point it only has the get method.

from flask import Flask, request
from flask_restful import Api, Resource
from avantionary_database import DataBase as db
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

# creating a resouce class
class WordInformation(Resource):
    # the get method of this resource class that returns infomation about word to client
    def get(self, word):
        return {"data": db.definitions(word)}

# adding the WordInformation resource to the api
api.add_resource(WordInformation, "/WordInformation/<string:word>")

# for staring the api application
def start_api():
    app.run(debug=True)
    # PORT INSIDE ABOVE.

