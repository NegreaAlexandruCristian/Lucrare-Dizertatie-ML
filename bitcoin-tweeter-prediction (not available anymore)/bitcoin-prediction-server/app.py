from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


@app.route('/predict-bitcoin-price', methods=['POST'])
def predict_bitcoin_price():
    if request.method == 'POST':
        data = request.get_json()
        number = data['bitcoinPrice']

        # Your code to predict the bitcoin price goes here
        predicted_price = number  # predict_price(number)

        response = jsonify({'bitcoinPrice': predicted_price})
        return response
    else:
        response = jsonify({'error': 'Method not allowed'})
        response.status_code = 405
        response.headers.add('allow', 'POST')
        return response


if __name__ == '__main__':
    app.run()
