from flask import Flask, render_template, request, redirect
import sqlite3

app=Flask(__name__)

DB_NAME = '/app/data/database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close() 
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    note = request.form['content']
    conn = sqlite3.connect(DB_NAME)
    conn.execute('INSERT INTO notes (content) VALUES (?)', (note,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)