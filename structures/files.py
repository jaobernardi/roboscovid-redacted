import json


class RelativeJsonFile(object):
	def __init__(self, input):
		with open(f"{input}", encoding="utf-8") as file:
			self._data = json.load(file)

	def __getattribute__(self, name):
		_data = object.__getattribute__(self, "_data")
		if name in _data:
			return _data[name]
		return object.__getattribute__(self, name)


class Config(RelativeJsonFile):
	def __init__(self):
		super().__init__("config.json")


class Messages(RelativeJsonFile):
	def __init__(self):
		c = Config()
		super().__init__(c.messages_file)