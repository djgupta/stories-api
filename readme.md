# stories-api
This is a rest API to create/view stories in the form of text, image and video. \
All the images and video are resized into compressed format. \
Once a story is created, story_id is sent to a queue and queue is being continuously read for image and video **compression** \
Application has unit tests written in **pytest**. \
Application is written in **python** using **flask** framework and uses **sqlite3** as database \
API is deployed on **heroku**: http://story-api-dj.herokuapp.com

## Design
This application has following APIs: \

GET http://story-api-dj.herokuapp.com \
returns a welcome message

GET http://story-api-dj.herokuapp.com/story \
gets all the stories in descending order of creation

POST http://story-api-dj.herokuapp.com/story \
creates a story \
Example: \
"""
curl -X POST \
   http://story-api-dj.herokuapp.com/story \
  -H 'content-type: multipart/form-data' \
  -H 'enctype: multipart/form-data' \
  -F 'story_content=@YOUR_IMAGE' \
  -F user_name=dj \
  -F file_type=image \
  -F 'description=beautiful view' \
  -F 'story_name=first story'
"""

GET http://story-api-dj.herokuapp.com/story/{story_id} \
gets a compressed video/image story by story_id
Example: \
https://story-api-dj.herokuapp.com/story/f204f1ef-86ac-4794-9926-f7a3ce428ee6


PUT http://story-api-dj.herokuapp.com/story/resize/{story_id} \
compresses video/image story by story_id

## How to run locally
pip install -r requirements.txt
export FLASK_APP=app.py or set FLASK_APP=app.py
flask run

## Run tests locally
python -m pytest
