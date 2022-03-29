from flask import Flask, jsonify, make_response, request
from scrapper import get_stocks_payment_dates
from formatter import format_payments_to_json
from errors import OutOfBoundsError

app = Flask(__name__)

LIMIT_OF_SYMBOLS_PER_REQUEST = 5

@app.route('/payments', methods=['GET'])
def index():
	symbols = request.args.get('symbols', '').split(',')
	unique_symbols = set(symbols)

	try:
		if len(unique_symbols) > LIMIT_OF_SYMBOLS_PER_REQUEST:
			raise OutOfBoundsError

		scrapped_payment_dates, errors = get_stocks_payment_dates(unique_symbols)
		payments = format_payments_to_json(scrapped_payment_dates)

		return jsonify({'data': payments, 'errors': errors})
	except OutOfBoundsError as e:
		return make_response({'error': e.message}, e.status_code)
	except:
		return make_response({'error': 'An unknown error had occurred.'}, 500)


if __name__ == '__main__':
	app.run(debug=True)
