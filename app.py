from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    author_name = "Sevgitr"  # Replace with your actual name
    return render_template('index.html', author_name=author_name)

if __name__ == '__main__':
    app.run(debug=True)
