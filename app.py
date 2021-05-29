from flask import Flask, config, request, jsonify, send_file
import threading
import service
import configuration

app = Flask(__name__)
configuration.current_config = configuration.configs.get('prod')

@app.before_first_request
def init():
    service.init()

@app.route('/')
def welcome():
    return 'Welcome to stories-api'

@app.route('/story', methods=['GET'])
def get_all_stories():
    return jsonify(service.get_all_stories())

@app.route('/story', methods=['POST'])
def create_story():
    data = request.form
    print(data)
    file=None
    if request.files.__len__() > 0:
        file = request.files['story_content']  
    return service.create_story(data, file=file)

@app.route('/story/<story_id>', methods=['GET'])
def get_resized_story(story_id):
    filename = service.get_resized_story(story_id)
    return send_file(filename)

@app.route('/story/resize/<story_id>', methods=['PUT'])
def resize_story(story_id):
    return service.resize_story(story_id)