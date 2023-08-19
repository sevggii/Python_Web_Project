from flask import Flask, render_template, request, redirect
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Creating SQLite database connection
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/')
def index():
    author_name = "Your Name"
    return render_template('index.html', author_name=author_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        nickname = request.form.get('nickname')
        password = request.form.get('psw')

        hashed_password = generate_password_hash(password, method='sha256')

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, nickname, password, puan) VALUES (?, ?, ?, ?)", (username, nickname, hashed_password, 0))
        conn.commit()
        conn.close()

        return redirect('/')  # Redirect to home page after registration is complete
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/exam')
def exam():
    return render_template('exam.html')

if __name__ == '__main__':
    app.run(debug=True)
