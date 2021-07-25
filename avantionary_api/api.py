# MANUAL:
# Run the main file "avantionary.py to run the api. Do not run api.py
# The url to the API is http://127.0.0.1:5000/
# as at this point it only has the get method.

from flask import Flask
from flask_restful import Api, Resource, reqparse
from avantionary_database import DataBase as db
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
CORS(app)

# using flask_restful's inbuild request parser to parse data taken from client based on the following arguments
# MEANING of word
# SYNONYMS of the word
# ANTONYMS of the word
word_put_args = reqparse.RequestParser()
word_put_args.add_argument("MEANINGS", type=str, help="A string of all meanings of the word. MEANINGS in caps.")
word_put_args.add_argument("SYNONYMS", type=str, help="A string of the synonyms of the word. Separate by comma if more than one. SYNONYMS in caps.")
word_put_args.add_argument("ANTONYMS", type=str, help="A string of the antonyms of the word. Separate by comma if more than one. ANTONYMS in caps.")
# creating a resouce class
class WordInformation(Resource):
    # the get method of this resource class that returns infomation about word to client
    def get(self, word):
        return {"data": db.definitions(word)}

    # the post method of this resource class takes in data from client
    def post(self, word):
        args = word_put_args.parse_args()
        return {word: args}

# adding the WordInformation resource to the api
api.add_resource(WordInformation, "/WordInformation/<string:word>")

# for staring the api application
def start_api():
    app.run(debug=True)

