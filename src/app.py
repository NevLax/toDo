from flask import Flask
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template
import sqlite3
import markdown
import uuid

app = Flask(__name__)

connection = sqlite3.connect('database.db')
connection.execute('''
CREATE TABLE IF NOT EXISTS Notes (
id INTEGER PRIMARY KEY,
uuid TEXT NOT NULL,
title TEXT NOT NULL,
description TEXT,
done INTEGET NOT NULL
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
        return render_template('todo.html', data=data)
    else:                       #post for add new todo
        title = request.form.get('title')
        description = request.form.get('description')
        uid = str(uuid.uuid1())

        with sqlite3.connect('database.db') as notes:
            cursor = notes.cursor()
            cursor.execute('INSERT INTO Notes (uuid, title, description, done) VALUES (?, ?, ?, 0)',
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
        id, uid, title, description, done = data
        description = markdown.markdown(description)
        item = (id, uid, title, description, done)
        return render_template('todo-item.html', item=item)


@app.route('/todo/<uuid:id>/del')
def delete_todo(id):
    with sqlite3.connect('database.db') as notes:
        cursor = notes.cursor()
        cursor.execute('DELETE FROM Notes WHERE uuid = ?', (str(id),) )

        notes.commit()
        return redirect(url_for('todo'))


@app.route('/todo/<uuid:id>/edit', methods=['GET', 'POST'])
def edit_todo(id):
    if request.method == 'GET':
        with sqlite3.connect('database.db') as notes:
            cursor = notes.cursor()
            cursor.execute('SELECT * FROM Notes WHERE uuid = ?', (str(id),))

            data = cursor.fetchone()
            _, _, title, description, _ = data
            return render_template('todo-edit.html', item=(title, description))
    else:
        with sqlite3.connect('database.db') as notes:
            cursor = notes.cursor()
            
            title = request.form.get('title')
            description = request.form.get('description')

            cursor.execute('UPDATE Notes SET title = ?, description = ? WHERE uuid = ?',
                (title, description, str(id),))

        return redirect(url_for('get_todo', id=id))


@app.route('/todo/<uuid:id>/done')
def done_todo(id):
    with sqlite3.connect('database.db') as notes:
        cursor = notes.cursor()
        cursor.execute('SELECT * FROM Notes WHERE uuid = ?', (str(id),))
    
        _, _, _, _, done = cursor.fetchone()
        if done:
            done = 0
        else:
            done = 1

        cursor.execute('UPDATE Notes SET done = ? WHERE uuid = ?', (done, str(id),))
    return redirect(url_for('get_todo', id=id))

            
if __name__ == '__main__':
    app.run()
