import story_database as database
from datetime import datetime
import uuid
import os
from PIL import Image
from moviepy.editor import VideoFileClip
import story_queue
import threading
import configuration
import json

queue_start = False

def get_all_stories():
    data = database.get_all()
    result = [json.loads(d[0]) for d in data]
    return result

def create_story(data, file=None):
    story = None
    if data.get('file_type') == 'image':
        if file is None:
            raise BaseException('need an image file')
        story = create_image_story(data, file)
    elif data.get('file_type') == 'video':
        if file is None:
            raise BaseException('need a video file')
        story = create_video_story(data, file)
    elif data.get('file_type') == 'text':
        story = create_text_story(data)
    else:
        raise BaseException('this file type is not recognized')
    return story

def create_image_story(data, file):
    story_id = uuid.uuid4().__str__()
    original_file_name = file.filename
    extension = os.path.splitext(original_file_name)[1]
    file_name = story_id+extension
    file.save(os.path.join(configuration.current_config['original_files'], file_name))
    story = {
        'story_id' : story_id,
        'user_name' : data.get('user_name'),
        'story_name' : data.get('story_name'),
        'description' : data.get('description'),
        'file_type' : data.get('file_type'),
        'latitude' : data.get('latitude'),
        'longitude' : data.get('longitude'),
        'system_timestamp' : datetime.now(),
        'original_filename' : original_file_name,
        'file_extension' : extension,
        'file_name' : file_name,
        'story_content': data.get('story_content')
    }
    database.insert(story)
    story_queue.put(story_id)
    return story

def create_video_story(data, file):
    story_id = uuid.uuid4().__str__()
    original_file_name = file.filename
    extension = os.path.splitext(original_file_name)[1]
    file_name = story_id+extension
    file.save(os.path.join(configuration.current_config['original_files'], file_name))
    story = {
        'story_id' : story_id,
        'user_name' : data.get('user_name'),
        'story_name' : data.get('story_name'),
        'description' : data.get('description'),
        'duration' : None,
        'file_type' : data.get('file_type'),
        'latitude' : data.get('latitude'),
        'longitude' : data.get('longitude'),
        'system_timestamp' : datetime.now(),
        'original_filename' : original_file_name,
        'file_extension' : extension,
        'file_name' : file_name,
        'story_content': data.get('story_content')
    }
    database.insert(story)
    story_queue.put(story_id)
    return story

def create_text_story(data):
    story_id = uuid.uuid4().__str__()
    story = {
        'story_id' : story_id,
        'user_name' : data.get('user_name'),
        'story_name' : data.get('story_name'),
        'description' : data.get('description'),
        'file_type' : data.get('file_type'),
        'latitude' : data.get('latitude'),
        'longitude' : data.get('longitude'),
        'system_timestamp' : datetime.now(),
        'story_content': data.get('story_content')
    }
    database.insert(story)
    return story

def resize_stories():
    while True:
        if(story_queue.empty()):
            continue
        resize_story(story_queue.get())

def get_resized_story(story_id):
    story = database.get_story_by_id(story_id)
    return os.path.join(configuration.current_config['resized_files'], story.get('file_name'))

def resize_story(story_id):
    story = database.get_story_by_id(story_id)
    if story.get('file_type') not in ['image', 'video']:
        raise BaseException('this story is not a image or a video')
    if story.get('file_type') == 'image':
        resize_image(story)
    elif story.get('file_type') == 'video':
        resize_video(story)
    return 'success'

def resize_image(story):
    im = Image.open(os.path.join(configuration.current_config['original_files'], story.get('file_name'))) 
    im.resize((600,1200))
    im.save(os.path.join(configuration.current_config['resized_files'], story.get('file_name')))
    return 'success'

def resize_video(story):
    video = VideoFileClip(os.path.join(configuration.current_config['original_files'], story.get('file_name')))
    video.resize( (460,720) )
    video.write_videofile(os.path.join(configuration.current_config['resized_files'], story.get('file_name')))
    return 'success'

def init():
    os.makedirs(configuration.current_config['original_files'], exist_ok=True)
    os.makedirs(configuration.current_config['resized_files'], exist_ok=True)
    database.get_db()
    thread = threading.Thread(target=resize_stories)
    thread.start()