#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Tasks

app = Flask(__name__)

engine = create_engine('sqlite:///tasks.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()

tasks= []

'''
    Error Handling
'''
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

'''
    Routes
'''
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api')
def task_index():
    return "Task Manager Listening"

@app.route('/api/all')
def get_all_tasks():
    tasks_results = {}
    for task in session.query(Tasks).all():
        this_task = {}
        this_task["id"] = vars(task)["id"]
        this_task["title"] = vars(task)["title"]
        this_task["description"] = vars(task)["description"]
        this_task["done"] = vars(task)["done"]
        tasks_results[vars(task)["id"]] = this_task
    return jsonify(tasks_results)

@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# Test String
# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Walk", "description": "Take a walk"}' http://localhost:5000/api/new
@app.route('/api/new/<int:task_id>', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', "No Description"),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

# Test String
# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/api/update/2
@app.route('/api/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# Test String
# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/delete/2
@app.route('/api/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)