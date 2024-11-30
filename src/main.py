from flask import Flask
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template
import sqlite3
import markdown
import uuid


app = Flask(__name__)
todo_dict = dict()


connection = sqlite3.connect('database.db')
connection.execute('''
CREATE TABLE IF NOT EXISTS Notes (
id INTEGER PRIMARY KEY,
uuid TEXT NOT NULL,
title TEXT NOT NULL,
description TEXT
)
''')
connection.commit()
connection.close()


@app.route('/')
def hello():
    return 'Hello'


@app.route('/todo/', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET': #get all todo
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM Notes')

        data = cursor.fetchall()
        print(data)
        return render_template('todo.html', data=data)
    else:                       #post for add new todo
        title = request.form.get('title')
        description = markdown.markdown(request.form.get('description'))
        uid = str(uuid.uuid1())

        with sqlite3.connect('database.db') as notes:
            cursor = notes.cursor()
            cursor.execute('INSERT INTO Notes (uuid, title, description) VALUES (?, ?, ?)',
                (uid, title, description)
            )
            notes.commit()
            
        return redirect(url_for('get_todo', id=uid))


@app.route('/todo/<uuid:id>/')
def get_todo(id):
    with sqlite3.connect('database.db') as notes:
        cursor = notes.cursor()
        cursor.execute('SELECT * FROM Notes WHERE uuid = ?', (str(id),))
        
        data = cursor.fetchone() 
        return render_template('todo-item.html', item=data)


@app.route('/todo/<uuid:id>/del', methods=['POST'])
def delete_todo(id):
    with sqlite3.connect('database.db') as notes:
        cursor = notes.cursor()
        cursor.execute('DELETE FROM Notes WHERE uuid = ?', (str(id),) )

        notes.commit()
        return redirect(url_for('todo'))


@app.route('/new-todo/')
def new_todo():
    return render_template('todo-form.html')
