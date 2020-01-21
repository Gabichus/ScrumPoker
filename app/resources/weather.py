from app import app, api, db
from flask_restful import Api, Resource, reqparse
import requests
import json

class Weather(Resource):
    def get(self):
        weatherJson = requests.get('http://localhost:9090/weather').content
        weatherJson = json.loads(weatherJson)
        return weatherJson
