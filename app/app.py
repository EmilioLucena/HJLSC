from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify
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


app = Flask(__name__)

swagger = Swagger(app, config=swagger_configuration)

@app.route('/status')
def status():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/transcribe', methods = ['POST'])
@swag_from('swagger/transcribe.yml')
def process():

    if(not request.is_json or request.get_json() == None):
        return json.dumps({"Bad Request":"missing or badly formatted data"}), 
        400, {'ContentType':'application/json'}
    
    input_dict = request.get_json()

    app.logger.info(f"JSON object received in /transcribe route: {input_dict}")
    
    app.logger.info(f"mission name: {input_dict['mission_id']}")

    #data = transcriptionController().transcribe_answer_file(input_dict)

    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/check_job', methods = ['POST'])
def check_job():

    if(not request.is_json or request.get_json() == None):
        return json.dumps({"Bad Request":"missing or badly formatted data"}), 
        400, {'ContentType':'application/json'}
    
    input_dict = request.get_json()

    app.logger.info(f"JSON object received in /check_job route: {input_dict}")

    return json.dumps({'status':'running'}), 200, {'ContentType':'application/json'}



app.run(host=os.environ['HOST'],port=os.environ['PORT'])