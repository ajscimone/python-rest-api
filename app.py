#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from schema import Tasks, Base

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
    session = Session()
    row = session.query(Tasks).filter(Tasks.id == task_id).first()      #Need error checking here if we don't find a task
    print("found", row.title)
    this_task = {}
    this_task["id"] = vars(row)["id"]
    this_task["title"] = vars(row)["title"]
    this_task["description"] = vars(row)["description"]
    this_task["done"] = vars(row)["done"]
    return jsonify({'task': this_task})

@app.route('/api/new', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_task = Tasks(title = request.json['title'], description = request.json.get('description', "No Description"))
    session.add(new_task)
    session.commit()
    return jsonify({"Success":"True"}), 201

@app.route('/api/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    row = session.query(Tasks).filter(Tasks.id == task_id).first()
    if 'title' in request.json:
        row.title = request.json['title']
    if 'description' in request.json:
        row.description = request.json['description']
    if 'done' in request.json:
        row.done = request.json['done']
    if 'date' in request.json:  # Could do better error handling here by checking if it matches datetime type
        try:
            row.date = request.json['date']
        except SQLAlchemyError as e:
            print(e)
    session.commit()
    return jsonify({'result': True})

@app.route('/api/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    session.query(Tasks).filter(Tasks.id == task_id).delete()   # Need some error checking here if we try an id that doesnt exist
    session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)