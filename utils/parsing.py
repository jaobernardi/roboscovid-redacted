def parse_string(input, vars={}):
	for var in vars:
		input = input.replace(f"${var}$", vars[var])
	return input
