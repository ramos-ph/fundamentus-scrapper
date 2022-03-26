from flask import Flask, jsonify, request
from scrapper import get_stocks_payment_dates
from formatter import format_payments_to_json

app = Flask(__name__)

@app.route('/payments')
def index():
	try:
		symbols = request.args.get("symbols")
		scrapped_payment_dates = get_stocks_payment_dates(symbols.split(','))
		return format_payments_to_json(scrapped_payment_dates)
	except:
		return jsonify([])


if __name__ == "__main__":
	app.run(debug=True)
