from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    author_name = "Your Name"
    return render_template('index.html', author_name=author_name)

@app.route('/register')
def register():
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

