from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
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


@app.route('/status')
def status():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/etapas', methods = ['get'])
@swag_from('swagger/etapas.yml')
def get_etapas():

    app.logger.info("request received on route /etapas'")

    etapas_db = db.etapa.find()
    etapas = []
    for obj in etapas_db:
        etapa = {'course':obj['course'], 'name': obj['name'], 'id':obj['id'], 'step': obj['step'], 'stage': obj['stage']}
        #app.logger.info(etapa)
        etapas.append(etapa)

    return json.dumps(etapas), 200, {'ContentType':'application/json'}

@app.route('/etapa/<int:etapa_id>', methods = ['get'])
@swag_from('swagger/etapa.yml')
def get_etapa(etapa_id):

    app.logger.info("request received on route /etapa'")

    etapa_db = db.etapa.find_one({'id':etapa_id})
    if(etapa_db != None):
        del etapa_db['_id']
        response_code = 200
    else:
        etapa_db = {'status': 404, 'error': 'resource not found'}
        response_code = 404
    
    #app.logger.info(etapa_db)
    return json.dumps(etapa_db), response_code, {'ContentType':'application/json'}


app.run(host=os.environ['HOST'],port=os.environ['PORT'])