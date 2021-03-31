#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import create_engine
from flask import g
from json import dumps
from datetime import datetime

app = Flask(__name__)
api = Api(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100000 per minute"]
)

DATABASE = 'dnstracker.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = create_engine('sqlite:///'+DATABASE)
    return db


class DNSQuery(Resource):
    def get(self):
        conn = get_db()
        query = conn.execute("select * from dns_query") # This line performs query and returns json result
        return {'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]} # Fetches first column that is query ID
    
    def post(self):
        try:
            conn = get_db()
            print(request.json)
            conn.execute("INSERT INTO dns_query VALUES(null, '{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(
                request.json['version_id'],
                request.json['domain'],
                request.json['query_type'],
                request.json['query_name'],
                request.json['ipv4_address'],
                request.json['ipv6_address'],
                request.json['as_number'],
                request.json['as_name'],
                request.json['bgp_prefix'],
                request.json['worker_id'],
                request.json['created_at'],
                request.json['updated_at']
            ))
            return {'status':'success'}
        except:
            return {'status':'error'}

class DNSQuery_Data(Resource):
    def get(self, query_id):
        conn = get_db()
        query = conn.execute("select * from dns_query where id =%d "  %int(query_id))
        result = {'data': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        return jsonify(result)

class RunVersion(Resource):
    def get(self):
        conn = get_db()
        query = conn.execute("select * from run_version") # This line performs query and returns json result
        return {'runnings': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]} # Fetches first column that is query ID
    
    def post(self):
        try:
            conn = get_db()
            print(request.json)
            conn.execute("INSERT INTO run_version VALUES(null, '{0}','{1}','{2}','{3}')".format(
                request.json['start_at'],
                request.json['end_at'],
                request.json['created_at'],
                request.json['updated_at']
            ))
            return {'status':'success'}
        except:
            return {'status':'error'}

class Alive(Resource):
    def get(self):
        return {'alive': True}




api.add_resource(DNSQuery, '/dns_query') # Route_1
api.add_resource(DNSQuery_Data, '/dns_query/<query_id>') # Route_2
api.add_resource(RunVersion, '/run_version') # Route_3
api.add_resource(Alive, '/alive') # Route_4


if __name__ == '__main__':
     app.run()
