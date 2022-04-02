from flask import Flask, jsonify, make_response, request
from scrapper import get_payment_dates
from errors import OutOfBoundsError

app = Flask(__name__)

LIMIT_OF_SYMBOLS_PER_REQUEST = 5

@app.route('/payments', methods=['GET'])
def index():
	symbols = request.args.get('symbols', '').split(',')
	symbols = set(symbols)

	try:
		if len(symbols) > LIMIT_OF_SYMBOLS_PER_REQUEST:
			raise OutOfBoundsError

		payments = get_payment_dates(symbols)
		return jsonify({'data': payments})
	except OutOfBoundsError as e:
		return make_response({'error': e.message}, e.status_code)


if __name__ == '__main__':
	app.run(debug=True)
