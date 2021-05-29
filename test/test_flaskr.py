import pytest
import json
import io
import configuration
from PIL import Image

from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.testing = True
    configuration.current_config = configuration.configs.get('test')
    return app.test_client()

def test_root(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = 'Welcome to stories-api'
    assert expected == res.get_data(as_text=True)

def test_get_empty_stories(app, client):
    res = client.get('/story')
    assert res.status_code == 200
    expected = '[]'
    assert expected == res.get_data(as_text=True).replace('\n','')

def test_fail_create_story(app, client):
    data = dict(
        file=(open('test/test.jpg', 'rb'), "work_order.123"),
    )
    res = client.post('/story', headers={'enctype':'multipart/form-data', 'content-type':'multipart/form-data'}, data=data, follow_redirects=True)
    assert res.status_code == 400

    data = dict(
        story_content=(open('test/test.jpg', 'rb'), "work_order.123"),
    )
    with pytest.raises(BaseException):
        client.post('/story', headers={'enctype':'multipart/form-data', 'content-type':'multipart/form-data'}, data=data, follow_redirects=True)

    data = dict(
        story_content=(open('test/test.jpg', 'rb'), "work_order.123"),
        file_type = 'jnknkjnkjnk'
    )
    with pytest.raises(BaseException):
        client.post('/story', headers={'enctype':'multipart/form-data', 'content-type':'multipart/form-data'}, data=data, follow_redirects=True)

def test_create_story(app, client):
    file = 'test.jpg'
    data = dict(
        story_content=(open('test/test.jpg', 'rb'), file),
        file_type = 'image'
    )
    res = client.post('/story', headers={'enctype':'multipart/form-data', 'content-type':'multipart/form-data'}, data=data, follow_redirects=True)
    assert res.status_code == 200
    assert file == res.get_json().get('original_filename')

def test_resize_story(app, client):
    file_name="test.jpg"
    data = dict(
        story_content=(open('test/test.jpg', 'rb'), file_name),
        file_type = 'image'
    )
    res = client.post('/story', headers={'enctype':'multipart/form-data', 'content-type':'multipart/form-data'}, data=data, follow_redirects=True)
    assert res.status_code == 200
    story_id = res.get_json().get('story_id')

    res = client.put('/story/resize/{}'.format(story_id))
    assert res.status_code == 200
    assert "success" == res.get_data(as_text=True)


def test_get_story_by_id(app, client):
    file_name="test.jpg"
    data = dict(
        story_content=(open('test/test.jpg', 'rb'), file_name),
        file_type = 'image'
    )
    res = client.post('/story', headers={'enctype':'multipart/form-data', 'content-type':'multipart/form-data'}, data=data, follow_redirects=True)
    assert res.status_code == 200
    story_id = res.get_json().get('story_id')

    res = client.put('/story/resize/{}'.format(story_id))
    assert res.status_code == 200
    assert "success" == res.get_data(as_text=True)

    res = client.get('/story/{}'.format(story_id))
    assert res.status_code == 200