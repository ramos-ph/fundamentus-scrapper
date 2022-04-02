from formatter import format_payments_to_json
from stocks_scrapper import get_stocks_payment_dates

def get_payment_dates(symbols):
	payments_df = get_stocks_payment_dates(symbols)
	return format_payments_to_json(payments_df)
