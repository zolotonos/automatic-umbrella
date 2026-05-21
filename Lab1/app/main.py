import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def root():
    if 'text/html' not in request.headers.get('Accept', ''):
        return "HTML ONLY", 406
    return "<html><body><ul><li>GET /tasks</li><li>POST /tasks</li><li>POST /tasks/&lt;id&gt;/done</li></ul></body></html>"

@app.route('/health/alive')
def alive():
    return "OK", 200

@app.route('/health/ready')
def ready():
    try:
        conn = get_db_connection()
        conn.close()
        return "OK", 200
    except Exception as e:
        return str(e), 500

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        if request.is_json:
            title = request.json.get('title')
        else:
            title = request.form.get('title')
            
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"id": new_id, "title": title, "status": "pending"}), 201
        
    else:
        cursor.execute("SELECT id, title, status, created_at FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        
        accept = request.headers.get('Accept', '')
        if 'text/html' in accept:
            html = "<html><body><table border='1'><tr><th>ID</th><th>Title</th><th>Status</th><th>Created At</th></tr>"
            for t in tasks:
                html += f"<tr><td>{t['id']}</td><td>{t['title']}</td><td>{t['status']}</td><td>{t['created_at']}</td></tr>"
            html += "</table></body></html>"
            return html
            
        return jsonify(tasks)

@app.route('/tasks/<int:task_id>/done', methods=['POST'])
def task_done(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200