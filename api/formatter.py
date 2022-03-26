import pandas as pd
import numpy as np
import json
from datetime import datetime

COLUMNS = ['symbol', 'value', 'type', 'date']
DATE_PATTERN = '\d{2}/\d{2}/\d{4}'

def format_payments_to_json(scrapped_payment_dates):
	arr = np.vstack(np.array(scrapped_payment_dates, dtype=object))
	df = build_dataframe(arr)
	return format_dataframe_to_json(df)


def build_dataframe(arr):
	df = pd.DataFrame(columns=COLUMNS, data=arr)

	df = df[df['date'].str.contains(DATE_PATTERN)]
	df['Payment timestamp'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
	df = df[df['Payment timestamp'] >= datetime.today()]

	return df


def format_dataframe_to_json(df):
	symbols = list(df['symbol'].drop_duplicates())
	payments = []

	for symbol in symbols:
		pending_earnings = df[df['symbol'] == symbol]
		pending_earnings = pending_earnings[['value', 'date', 'type']]
		payments.append({
			'symbol': symbol,
			'pending_earnings': pending_earnings.to_dict(orient='records')
		})

	return json.dumps(payments)
