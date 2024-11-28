from flask import Flask
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template
import markdown
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
def todo():
    if request.method == 'GET': #get all todo
        return render_template('todo.html', td_dict=todo_dict)
    else:                       #post for add new todo
        todo_item = {
            'title': request.form.get('title'),
            'description': markdown.markdown(request.form.get('description'))
        }
        uid = str(uuid.uuid1())
        todo_dict[uid] = todo_item
        return redirect(url_for('get_todo', id=uid)) #redirect to list item


@app.route('/todo/<uuid:id>/')
def get_todo(id):
    return render_template('todo-item.html', item=todo_dict[str(id)])


@app.route('/todo/<uuid:id>/del', methods=['POST'])
def delete_todo(id):
    del todo_dict[str(id)]
    return redirect(url_for('todo'))

@app.route('/new-todo/')
def new_todo():
    return render_template('todo-form.html')
    
