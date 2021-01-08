from .data import Persistance_IO
from .files import Config
from datetime import datetime, timedelta
import os


class CacheWrapper:
	def __init__(self, data, expires=True, expire_time: datetime=None):
		self.expire_time = expire_time or datetime.now() + timedelta(seconds=Config().cache["expire"])
		self.expires = expires
		self.data = data


class CacheIO(Persistance_IO):
	def __init__(self):
		super().__init__(Config().cache["path"])

	@property
	def itens(self):
		return self.list(self.path)
	

	def get(self, name):
		if name.lower() in self.list(self.path):
			obj = self.load(self.path+name.lower()+".iov")
			if not (obj.expires and datetime.now() > obj.expire_time):
				return obj.data
			else:
				os.remove(self.path+name.lower()+".iov")
		return

	def set(self, name, data, expires=True, expire_time: datetime=None):
		obj = CacheWrapper(data, expires, expire_time)
		self.write(self.path+name.lower()+".iov", obj)

	def clear(self, all=False):
		for file in os.listdir(self.path):
			if file.endswith(".iov"):
				if all:
					os.remove(self.path+file)
					continue
				self.get(file.split(".iov")[0])