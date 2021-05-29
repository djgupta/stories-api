from datetime import datetime
import sqlite3
import json
from bson import json_util
import configuration

conn = None

def get_db():
    db_name = configuration.current_config['database_name']
    global conn
    if conn is None:
        conn = sqlite3.connect(db_name, check_same_thread=False)
        create_table()
    return conn

def insert(story):
    c = get_db().cursor()
    return c.execute("insert into stories values (?, ?, ?)", [story['story_id'], json.dumps(story, default=json_util.default), datetime.now()])

def get_all():
    c = get_db().cursor()
    return c.execute("select data from stories order by system_timestamp desc").fetchall()

def create_table():
    c = get_db().cursor()
    c.execute("CREATE TABLE IF NOT EXISTS stories (story_id varchar(20), data json, system_timestamp timestamp)")

def get_story_by_id(story_id):
    c = get_db().cursor()
    story = c.execute("select data from stories where story_id='{}'".format(story_id)).fetchone()
    return json.loads(story[0])

