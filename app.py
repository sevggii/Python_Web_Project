import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "your_secret_key"  # This is used for session data security

# Define the global author_name variable
author_name = "Sevgi"

# Creating SQLite database connection
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

#API KEY: d35bb35538e0d93fa05e44360e06f2b7
@app.route('/')
def indexForm():
    if 'user_id' in session:
        return redirect('/userHomePage')  # Redirect to UserHomePage if user is logged in
    return render_template('index.html', author_name=author_name)

@app.route('/signupPage', methods=['GET', 'POST'])
def signupPage():
    if request.method == 'POST':
        username = request.form.get('username')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        password_repeat = request.form.get('password-repeat')


            # Verify password match
        if password != password_repeat:
            return render_template('signupPage.html', error="Passwords do not match", author_name=author_name)

        conn = create_connection()
        cursor = conn.cursor()

        # Check if username is already taken
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return render_template('signupPage.html', error="Username is already taken", author_name=author_name)
        
        # Check if nickname is already taken
        cursor.execute("SELECT * FROM users WHERE nickname = ?", (nickname,))
        existing_nickname = cursor.fetchone()
        if existing_nickname:
            conn.close()
            return render_template('signupPage.html', error="Nickname is already taken", author_name=author_name)

        try:
            hashed_password = generate_password_hash(password, method='sha256')
        except Exception as e:
            print("Error generating hashed password:", e)
            hashed_password = None


        try:
            cursor.execute("INSERT INTO users (username, nickname, password, score) VALUES (?, ?, ?, ?)",
                           (username, nickname, hashed_password, 0))
            conn.commit()
            conn.close()
            return redirect('/loginPage')
        except sqlite3.Error as e:
            print("Error inserting user:", e)
            conn.rollback()
            conn.close()
            return render_template('signupPage.html', error="Error occurred during registration", author_name=author_name)

    return render_template('signupPage.html', author_name=author_name)


@app.route('/loginPage', methods=['GET', 'POST'])
def loginPage():
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
            return redirect('/userHomePage')  # Redirect to home page

    return render_template('loginPage.html', author_name=author_name)

@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)  # Log out the user
    return redirect('/')

@app.route('/userHomePage')
def userHomePage():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('userHomePage.html', author_name=author_name)


@app.route('/examPythonAI')
def examPythonAI():
    if 'user_id' not in session:
        return redirect('/loginPage')

    user_id = session['user_id']
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_score = user[0] 
    else:
        user_score = 0

    # Retrieve leaderboard data
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM users ORDER BY score DESC")
    leaderboard_data = cursor.fetchall()
    conn.close()

    return render_template('examPythonAI.html', author_name=author_name, user_score=user_score, leaderboard_data=leaderboard_data)

@app.route('/updateScore', methods=['POST'])
def update_score():
    if 'user_id' not in session:
        return 'Unauthorized', 401
    
    user_id = session['user_id']
    new_score = int(request.json.get('score'))

    conn = create_connection()
    cursor = conn.cursor()

    # Get current score from database
    cursor.execute("SELECT score FROM users WHERE id = ?", (user_id,))
    current_score = cursor.fetchone()[0]

    # Update process
    updated_score = current_score + new_score
    cursor.execute("UPDATE users SET score = ? WHERE id = ?", (updated_score, user_id))
    conn.commit()
    conn.close()

    return 'Score updated successfully', 200



if __name__ == '__main__':
    app.run(debug=True)
