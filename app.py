from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    author_name = "Your Name"  # Değiştirin
    return render_template('index.html', author_name=author_name)

if __name__ == '__main__':
    app.run(debug=True)
