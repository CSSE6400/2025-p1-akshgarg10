from flask import Blueprint, jsonify, request

api = Blueprint('api',__name__, url_prefix='/api/v1')

@api.route('/<username>')
def login(username):
    return f"Hey {username}, This is the login page."

@api.route('/hello')
def hello():
    return jsonify({"status":"Hello Sir JI"})


tasks = [] #Created a list to store TODO Tasks

# get all tasks
@api.route('/getData')
def get_title():
    return jsonify(tasks)

# get by id
@api.route('/getDataByID/<int:id>', methods=['GET'])
def get_title_by_id(id):
    for task in tasks:
        if task["id"]==id:
            return jsonify(task)
    return jsonify({"error":"the ID does not exists"}),400

# post data
@api.route('/addData', methods=['POST'])
def add_data():
    data = request.get_json()
    for task in tasks:
        if task["id"] == data["id"]:
            return jsonify({"error":"Task with same ID exists"}),400
    tasks.append(data)
    return jsonify({"Success":"It's added"})

# update by id
@api.route('updateData/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == id:
            task.update(data)
            return jsonify({"Success":"Task updated", "Task":task}),200
        
        
        
# delete by id
@api.route('deleteByID/<int:id>', methods=['DELETE'])
def delete_data(id):
    for task in tasks:
        if id == task["id"]:
            tasks.remove(task)
            return jsonify({"Success":"Task removed"}),200
    return jsonify({"error":"ID does not exists"}),400