from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import mysql.connector

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/photos'

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Database configuration
db_config = {
    'user': 'admin',
    'password': 'StrongP@ssw0rd',
    'host': 'localhost',
    'database': 'stin_db'
}

def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS visits (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        place_name VARCHAR(255),
                        visit_date DATE,
                        photo VARCHAR(255))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        visit_id INT,
                        comment TEXT,
                        FOREIGN KEY (visit_id) REFERENCES visits(id))''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visits')
    visits = cursor.fetchall()
    conn.close()
    return render_template('index.html', visits=visits)

@app.route('/add_visit', methods=['GET', 'POST'])
def add_visit():
    if request.method == 'POST':
        place_name = request.form['place_name']
        visit_date = request.form['visit_date']
        photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO visits (place_name, visit_date, photo) VALUES (%s, %s, %s)', 
                       (place_name, visit_date, filename))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_visit.html')

@app.route('/get_visits', methods=['GET'])
def get_visits():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM visits')
    visits = cursor.fetchall()
    conn.close()
    return jsonify([{"id": visit[0], "place_name": visit[1], "visit_date": visit[2], "photo": visit[3]} for visit in visits]), 200

@app.route('/add_comment', methods=['POST'])
def add_comment():
    visit_id = request.json.get('visit_id')
    comment = request.json.get('comment')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO comments (visit_id, comment) VALUES (%s, %s)', (visit_id, comment))
    conn.commit()
    conn.close()
    return jsonify({"message": "Comment added successfully"}), 200

@app.route('/get_comments/<int:visit_id>', methods=['GET'])
def get_comments(visit_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments WHERE visit_id = %s', (visit_id,))
    comments = cursor.fetchall()
    conn.close()
    return jsonify([{"id": comment[0], "visit_id": comment[1], "comment": comment[2]} for comment in comments]), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5014)