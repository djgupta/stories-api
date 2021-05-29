from queue import Queue
 
q = Queue()

def put(story_id):
    return q.put(story_id)

def get():
    return q.get()

def empty():
    return q.empty()