from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def hello():
    data = [
        {'name': 'John Doe', 'age': 28, 'city': 'New York'},
        {'name': 'Jane Smith', 'age': 34, 'city': 'San Francisco'},
        {'name': 'Mike Johnson', 'age': 45, 'city': 'Chicago'}
    ]
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
