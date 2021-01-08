class ObjectWrapper(object):

	store = {}

	def __setattr__(self, name, value):
		store = object.__getattribute__(self, "store")
		if name not in store:
			store[name] = None
		store[name] = value
		object.__setattr__(self, "store", store)


	def __getattribute__(self, name):
		store = object.__getattribute__(self, "store")
		if name in store:
			return store[name]
		return None