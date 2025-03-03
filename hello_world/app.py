from flask import Flask, render_template, request, redirect, url_for
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

# Подключение к MongoDB (при необходимости измените URI)
client = MongoClient('mongodb://localhost:27017/')
db = client['tasks_db']         # База данных tasks_db
tasks_collection = db['tasks']  # Коллекция tasks

@app.route('/', methods=['GET'])
def index():
    tasks = list(tasks_collection.find())
    return render_template('index.html', tasks=tasks)

@app.route('/ad', methods=['POST'])
def add_task():
    task_title = request.form.get('task')
    if task_title:
        tasks_collection.insert_one({'title': task_title})
    return redirect(url_for('index'))

@app.route('/delete/<task_id>', methods=['GET'])
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
