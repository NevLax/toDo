from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
import uuid

app = Flask(__name__)
todo_dict = dict()
#url_for('static', filename='style.css')

def todo_simple(title='Title', description=None):
    return {'title': title, 'description': description}

def impostor_list():
    todo_dict[str(uuid.uuid1())] = todo_simple(title='Simple')
    todo_dict[str(uuid.uuid1())] = todo_simple(title='Dimple')
    todo_dict[str(uuid.uuid1())] = todo_simple(title='PopIt')
impostor_list()
print(todo_dict)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/todo/', methods=['GET', 'POST'])
def todo_new():
    if request.method == 'GET': #get all todo
        return render_template('todo.html', td_dict=todo_dict)
    else:                       #post for add new todo
        todo_item = request.json['todo']
        return redirect(url_for('todo')) #redirect to list item

@app.route('/todo/<uuid:id>/')
def get_todo(id):
    return 'sim'
