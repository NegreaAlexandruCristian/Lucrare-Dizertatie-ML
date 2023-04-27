from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


@app.route('/predict-bitcoin-price')
def hello_world():  # put application's code here
    # Your code to predict the bitcoin price goes here
    response = jsonify({'price': 1234.56})
    return response


if __name__ == '__main__':
    app.run()
