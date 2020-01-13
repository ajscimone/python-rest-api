#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Task

app = Flask(__name__)

engine = create_engine('sqlite:///tasks.db', echo = True)
Session = sessionmaker(bind = engine)
session = Session()

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
    session = Session()
    tasks_results = {}
    for task in session.query(Task).all():
        this_task = {}
        this_task["id"] = vars(task)["id"]
        this_task["title"] = vars(task)["title"]
        this_task["description"] = vars(task)["description"]
        this_task["done"] = vars(task)["done"]
        tasks_results[vars(task)["id"]] = this_task
    return jsonify(tasks_results)

# http://127.0.0.1:5000/api/task/1
@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    session = Session()
    row = session.query(Task).filter(Task.id == 1).first()
    print("found", row.title)
    # if len(task) == 0:
    #     abort(404)
    return jsonify({'task': "task"})

# Test String
# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Walk", "description": "Take a walk"}' http://127.0.0.1:5000/api/new
@app.route('/api/new/', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_task = Task(title = request.json['title'], description = request.json.get('description', "No Description"), done = False)
    session.add(new_task)
    session.commit()
    return jsonify({"Success":"True"}), 201

# Test String
# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/api/update/2
@app.route('/api/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    return jsonify({'result': True})

# Test String
# curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/delete/2
@app.route('/api/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)