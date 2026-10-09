import os
import sqlite3
from flask import Flask, request, redirect, render_template_string

DB_PATH = os.environ.get("DB_PATH", "/data/notes.db")
app = Flask(__name__)

PAGE = """
<!doctype html>
<title>Notes App</title>
<body style="font-family:sans-serif;max-width:600px;margin:40px auto">
  <h1>Notes App (SWE40006 Task 4.3)</h1>
  <form method="post" action="/add">
    <input name="text" placeholder="Write a note" required style="width:70%">
    <button type="submit">Add</button>
  </form>
  <ul>
  {% for n in notes %}
    <li>{{ n['text'] }}
      <form method="post" action="/delete/{{ n['id'] }}" style="display:inline">
        <button type="submit">x</button>
      </form>
    </li>
  {% else %}
    <li>No notes yet.</li>
  {% endfor %}
  </ul>
</body>
"""

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL)"
        )

init_db()

@app.route("/")
def index():
    with get_db() as conn:
        notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return render_template_string(PAGE, notes=notes)

@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        with get_db() as conn:
            conn.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    return redirect("/")

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    with get_db() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    return redirect("/")