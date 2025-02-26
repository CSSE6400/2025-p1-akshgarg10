from flask import Blueprint, jsonify, request
from datetime import datetime

api = Blueprint('api',__name__, url_prefix='/api/v1')

tasks = [] #Created a list to store TODO Tasks

#Health API
@api.route('/health')
def heal():
    return jsonify({"status":"ok"}), 200



# get all tasks
@api.route('/todos', methods=['GET'])
def get_tasks():
    return jsonify(tasks),200



# get by id
@api.route('/todos/<int:id>', methods=['GET'])
def get_title_by_id(id):
    for task in tasks:
        if task["id"]==id:
            return jsonify(task)
    return jsonify({"error":"the ID does not exists"}),400



# post data
@api.route('/todos', methods=['POST'])
def add_data():
    data = request.get_json()
    for task in tasks:
        if task["id"] == data["id"]:
            return jsonify({"error":"Task with same ID exists"}),400
    tasks.append(data)
    return jsonify({"Success":"It's added"}),201



# update by id
@api.route('/todos/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == id:
            task.update(data)
            return jsonify(task),200
    else:
        return jsonify({"error":"the id dosen't matches"}),400    
        

        
# delete by id
@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_data(id):
    for task in tasks:
        if id == task["id"]:
            tasks.remove(task)
            return jsonify(task),200
    return jsonify({"error":"ID does not exists"}),400