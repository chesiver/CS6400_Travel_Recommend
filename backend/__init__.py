from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()


api_base_url = '/api/v1'
es_base_url = {
    'destination': 'http://localhost:9200/travelsearch/destination',
    'countries': 'http://localhost:9200/travelsearch/countries',
    'cities': 'http://localhost:9200/travelsearch/cities'
}

class destinationList(Resource):

    def get(self):
        print("Call for: GET /destination")
        url = es_base_url['destination']+'/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        destinations = []
        for hit in data['hits']['hits']:
            destination = hit['_source']
            destination['id'] = hit['_id']
            destinations.append(destination)
        return destinations


class countryList(Resource):

    def get(self):
        print("Call for: GET /countries")
        url = es_base_url['countries']+'/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        countries = []
        for hit in data['hits']['hits']:
            country = hit['_source']
            country['id'] = hit['_id']
            countries.append(country)
        return countries

class cityList(Resource):

    def get(self):
        print("Call for: GET /cities")
        url = es_base_url['cities']+'/_search'
        query = {
            "query": {
                "match_all": {}
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        cities = []
        for hit in data['hits']['hits']:
            city = hit['_source']
            city['id'] = hit['_id']
            cities.append(city)
        return cities

    # def post(self):
    #     print("Call for: POST /beers")
    #     parser.add_argument('name')
    #     parser.add_argument('producer')
    #     parser.add_argument('abv')
    #     parser.add_argument('description')
    #     parser.add_argument('styles', action='append')
    #     beer = parser.parse_args()
    #     print(beer)
    #     url = config.es_base_url['beers']
    #     resp = requests.post(url, data=json.dumps(beer))
    #     data = resp.json()
    #     return data

class Destination(Resource):

    def get(self, destination_id):
        print("Call for: GET /destination/%s" % destination_id)
        url = es_base_url['destination']+'/'+destination_id
        resp = requests.get(url)
        data = resp.json()
        destination = data['_source']
        return destination

    def put(self, beer_id):
        """TODO: update functionality not implemented yet."""
        pass

    # def delete(self, beer_id):
    #     print("Call for: DELETE /beers/%s" % beer_id)
    #     url = config.es_base_url['beers']+'/'+beer_id
    #     resp = requests.delete(url)
    #     data = resp.json()
    # return data

class Country(Resource):

    def get(self, country_id):
        print("Call for: GET /countries/%s" % country_id)
        url = es_base_url['countries']+'/'+country_id
        resp = requests.get(url)
        data = resp.json()
        country = data['_source']
        return country


class Search(Resource):

    def get(self):
        print("Call for GET /search")
        parser.add_argument('q')
        query_string = parser.parse_args()
        url = es_base_url['destination']+'/_search'
        query = {
            "query": {
                "multi_match": {
                    "fields": ["name", "city", "country", "intro"],
                    "query": query_string['q'],
                    "type": "cross_fields",
                    "use_dis_max": False
                }
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        destinations = []
        for hit in data['hits']['hits']:
            destination = hit['_source']
            destination['id'] = hit['_id']
            destinations.append(destination)
        return destinations

api.add_resource(Destination, api_base_url+'/destination/<destination_id>')
api.add_resource(destinationList, api_base_url+'/destination')
api.add_resource(countryList, api_base_url+'/countries')
api.add_resource(Country, api_base_url+'/countries/<country_id>')
api.add_resource(cityList, api_base_url+'/cities')
api.add_resource(Search, api_base_url+'/search')



