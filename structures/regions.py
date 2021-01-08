class Regional_Methods:
	def __init__(self):
		self.regions = {"default": lambda x: None}

	def add(self, state, city=None):
		if not state in self.regions:
			self.regions[state.lower()] = {}		
		def wrapper(function):
			if not city:
				self.regions[state.lower()]["default"] = function
			else:
				self.regions[state.lower()][city.lower()] = function	
		return wrapper

	def default(self, function):
		self.regions["default"] = function

	def call(self, state, city=None, **kwargs):
		if not state.lower() in self.regions:
			return self.regions["default"](state, city, **kwargs)

		if city:
			if city.lower() in self.regions[state.lower()]:
				return self.regions[state.lower()][city.lower()](city, **kwargs)
		if "default" in self.regions[state.lower()]:
			return self.regions[state.lower()]["default"](city, **kwargs)
		return self.regions["default"](state, city, **kwargs)
