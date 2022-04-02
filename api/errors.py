class OutOfBoundsError(Exception):
	status_code = 400
	message = 'Only up to 5 symbols can be searched simultaneously.'
