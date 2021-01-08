import json
import os
from .files import Config
from .wrapper import ObjectWrapper

user_persistent_data = {}


class User(object):
	def __init__(self, name):
		if name not in user_persistent_data:
			user_persistent_data[name] = ObjectWrapper()
		self.name = name
		self.permissions = []
		self.places = []
		self.blocks = []
		self.context = user_persistent_data[name]
		self.cancelled = False
		self.new = False
		self._load()

	@property
	def _dict(self):
		return {"cancelled": self.cancelled, "permissions": self.permissions, "places": self.places, "blocks": self.blocks, "name": self.name}

	def _load(self):
		config = Config()
		if self.name+".json" not in os.listdir(config.user_path):
			self.new = True
			with open(config.user_path+self.name+".json", "w", encoding="utf-8") as f:
				f.write(json.dumps(self._dict))
				f.close()

		else:
			with open(config.user_path+self.name+".json", "rb") as f:
				dict = json.load(f)
				f.close()
			self.__dict__.update(dict)

	def flush(self):
		config = Config()
		with open(config.user_path+self.name+".json", "w", encoding="utf-8") as f:
			f.write(json.dumps(self._dict))
			f.close()

	def has_permission(self, permission):
		possible = list(self.permissions)
		match_tokens = permission.split(".")

		while len(possible) > 0:
			for perm in possible:
				test_tokens = perm.split(".")
				index = 0
				for token in test_tokens:
					if match_tokens[index] == "*":
						return True
					if token == "*":
						return True
					if token != match_tokens[index]:
						possible.remove(perm)
						break
					if index+1 == len(test_tokens) and index+1 == len(match_tokens):
						return True
					if index+1 >= len(match_tokens):
						possible.remove(perm)
						break
					index += 1
		return False
	