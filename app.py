from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "your_secret_key"  # This is used for session data security

# Define the global author_name variable
author_name = "AuthorNamee"

# Creating SQLite database connection
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/user_index')  # Redirect to user_index page if user is logged in
    return render_template('index.html', author_name=author_name)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        try:
            hashed_password = generate_password_hash(password, method='sha256') # Generate hashed password
        except Exception as e:
            print("Error generating hashed password:", e)
            hashed_password = None  # Handle the error appropriately


        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, nickname, password, score) VALUES (?, ?, ?, ?)", (username, nickname, hashed_password, 0))
        conn.commit()
        conn.close()

        return redirect('/')  # Redirect to home page after registration is complete
    return render_template('signup.html', author_name=author_name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):   # Check user's password
            session['user_id'] = user[0]  # Initialize the user's session
            return redirect('/user_index')  # Redirect to home page

    return render_template('login.html', author_name=author_name)

@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Log out the user
    return redirect('/')

    #return render_template('logout.html')

@app.route('/user_index')
def user_index():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('user_index.html', author_name=author_name)

if __name__ == '__main__':
    app.run(debug=True)
