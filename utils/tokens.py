from string import ascii_letters
from random import choice, randint


def token(size=5):
	values = [str(randint(0, 9)) for i in range(len(ascii_letters))]
	values.extend(list(ascii_letters))

	return "".join([choice(values) for i in range(size)])