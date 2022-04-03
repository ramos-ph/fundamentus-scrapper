import pandas as pd
from datetime import datetime

DATE_PATTERN = '\d{2}/\d{2}/\d{4}'

def format_payments_to_json(df):
	symbols = list(df['symbol'].drop_duplicates())
	payments = []
	for symbol in symbols:
		payments.append(get_pending_earnings_for(symbol, df))
	return payments

def get_pending_earnings_for(symbol, df):
	df = df[(df['symbol'] == symbol) & (df['payment'].str.contains(DATE_PATTERN))]
	df = df.assign(payment_timestamp=pd.to_datetime(df['payment'], format='%d/%m/%Y'))
	df = df[df['payment_timestamp'] >= datetime.now()]

	return {
		'symbol': symbol,
		'earnings': df[['value', 'payment', 'type']].to_dict(orient='records')
	}
