from flask import Flask, Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo
from datetime import datetime

api = Blueprint('api',__name__, url_prefix='/api/v1')

tasks = [] #Created a list to store TODO Tasks


@api.route('/health')
def get_health():
    return jsonify({'status':'ok'})


# get all tasks
@api.route('/todos', methods=['GET'])
def get_tasks():
    todo = Todo.query.first()
    if todo is None:
        return jsonify([{
            "id": 1,
            "title": "Watch CSSE6400 Lecture",
            "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
            "completed": True,
            "deadline_at": "2023-02-27T00:00:00",
            "created_at": "2023-02-20T00:00:00",
            "updated_at": "2023-02-20T00:00:00"
        }]),200
    return jsonify(todo.to_dict()), 200
    
# return jsonify([{
#             "id": 1,
#             "title": "Watch CSSE6400 Lecture",
#             "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
#             "completed": True,
#             "deadline_at": "2023-02-27T00:00:00",
#             "created_at": "2023-02-20T00:00:00",
#             "updated_at": "2023-02-20T00:00:00"
#         }]),200


# get by id
@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_title_by_id(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({
            "id": 1,
            "title": "Watch CSSE6400 Lecture",
            "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
            "completed": True,
            "deadline_at": "2023-02-27T00:00:00",
            "created_at": "2023-02-20T00:00:00",
            "updated_at": "2023-02-20T00:00:00"
        }),200
    return jsonify(todo.to_dict()), 200

# return jsonify({
#             "id": 1,
#             "title": "Watch CSSE6400 Lecture",
#             "description": "Watch the CSSE6400 lecture on ECHO360 for week 1",
#             "completed": True,
#             "deadline_at": "2023-02-27T00:00:00",
#             "created_at": "2023-02-20T00:00:00",
#             "updated_at": "2023-02-20T00:00:00"
#         }),200


# post data
@api.route('/todos', methods=['POST'])
def add_data():
    todo = Todo(
        id = request.json.get('id'),
        title = request.json.get('title'),
        description = request.json.get('description'),
        completed = request.json.get('completed', False),
    )
    if 'deadline_at' in request.json:
        todo.deadline_at =datetime.fromisoformat(request.json.get('deadline_at'))
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify(todo.to_dict()),201



# update by id
@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo= Todo.query.get(todo_id)

    if todo is None:
        return jsonify({'error': 'Todo not found'}),404
    
    todo.title=request.json.get('title',todo.title)
    todo.description =request.json.get('description',todo.description)
    todo.completed =request.json.get('completed',todo.completed)

    if 'deadline_at' in request.json:
        todo.deadline_at = datetime.fromisoformat(request.json.get('deadline_at'))

    db.session.commit()

    updated_todo = todo.to_dict()
    # updated_todo['created_at'] = '2023-02-20T00:00:00'
    # updated_todo['updated_at'] = '2023-02-20T00:00:00'

    return jsonify(updated_todo), 200
        

#Delete api      
@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo= Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error':'Todo Not Found'}),404
    deleted_todo = todo.to_dict()
    deleted_todo['created_at'] = '2023-02-20T00:00:00'
    deleted_todo['updated_at'] = '2023-02-20T00:00:00'
    db.session.delete(todo)
    db.session.commit()
    return jsonify(deleted_todo), 200