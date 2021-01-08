from structures.user import User
import os


def getUsers(place=None):
	for user in os.listdir("users\\"):
		user = User(user.split(".")[0])
		if place and place not in user.places:
			continue
		yield user 

def getPlaces():
	places = []
	for user in getUsers():
		for place in user.places:
			if place not in places:
				places.append(place)
	return places