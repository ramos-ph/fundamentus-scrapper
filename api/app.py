from flask import Flask, jsonify, make_response, request
from scrapper import get_stocks_payment_dates
from formatter import format_payments_to_json
from errors import OutOfBoundsError

app = Flask(__name__)

@app.route('/payments', methods=['GET'])
def index():
	symbols = request.args.get('symbols', '').split(',')

	try:
		if len(symbols) > 5:
			raise OutOfBoundsError

		scrapped_payment_dates = get_stocks_payment_dates(symbols)
		return format_payments_to_json(scrapped_payment_dates)
	except OutOfBoundsError as e:
		return make_response({'error': e.message}, e.status_code)
	except:
		return make_response({'error': 'An unknown error had occurred.'}, 500)


if __name__ == '__main__':
	app.run(debug=True)
