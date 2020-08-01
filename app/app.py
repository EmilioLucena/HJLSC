from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, Response
from flask_pymongo import PyMongo
import os
import json
import sys

from swagger.swagger_config import swagger_configuration
from flasgger import Swagger, swag_from

from logging.config import dictConfig
import traceback

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

username = os.environ['MONGODB_USERNAME']
password = os.environ['MONGODB_PASSWORD']
db_host = os.environ['MONGODB_HOSTNAME']
database = os.environ['MONGODB_DATABASE']

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{username}:{password}@{db_host}:27017/{database}?authSource=admin"
mongo = PyMongo(app)
db = mongo.db

swagger = Swagger(app, config=swagger_configuration)

API_URL = 'http://localhost:5000'


@app.route('/status')
def status():
    r = Response(response=json.dumps({'success':True}), status=200)
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    #return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return r

@app.route('/journeys', methods = ['get'])
#@swag_from('swagger/etapas.yml')
def get_journeys():

    app.logger.info("request received on route /journeys'")

    journeys_db = db.journey.find()
    journeys = []
    for obj in journeys_db:
        obj_id = obj['id']
        journey = {
            'id':obj_id, 
            'name': obj['name'], 
            'url': API_URL + f'/journey/{obj_id}'
            }
        journeys.append(journey)

    r = Response(response=json.dumps(journeys), status=200)
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    #return json.dumps(journeys), 200, {'ContentType':'application/json'}
    return r

@app.route('/journey/<int:journey_id>', methods = ['get'])
#@swag_from('swagger/etapas.yml')
def get_journey(journey_id):

    app.logger.info("request received on route /journey'")

    journey_db = db.journey.find_one({'id':journey_id})

    if(journey_db == None):
        journey_db = {'status': 404, 'error': 'resource not found'}
        response_code = 404
        
    else:
        del journey_db['_id']
        stages_db = db.stage.find({'journey_id':journey_id})
        stages = []
        for obj in stages_db:
            obj_id = obj['id']
            stage = {
                'id':obj_id, 
                'name': obj['name'], 
                'step': obj['step'], 
                'stage': obj['stage'],
                'journey_id': obj['journey_id'],
                'url': API_URL + f"/stage/{obj_id}"
                }
            stages.append(stage)
        journey_db['stages'] = stages
        response_code = 200

    r = Response(response=json.dumps(journey_db), status=response_code)
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r

@app.route('/stage/<int:stage_id>', methods = ['get'])
@swag_from('swagger/etapa.yml')
def get_stage(stage_id):

    app.logger.info("request received on route /stage'")

    stage_db = db.stage.find_one({'id':stage_id})
    if(stage_db != None):
        del stage_db['_id']
        response_code = 200
    else:
        stage_db = {'status': 404, 'error': 'resource not found'}
        response_code = 404

    r = Response(response=json.dumps(stage_db), status=response_code)
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


app.run(host=os.environ['HOST'],port=os.environ['PORT'])