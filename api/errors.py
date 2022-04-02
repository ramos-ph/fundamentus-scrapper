class OutOfBoundsError(Exception):
	status_code = 400
	message = 'Only up to 5 symbols can be searched simultaneously.'

class ScrapError(Exception):
	def __init__(self, symbol):
		self.message = f'Failed to get scrap data from symbol {symbol}'
