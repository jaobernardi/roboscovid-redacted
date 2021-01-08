import dill
import os
from utils import token
from .files import Config
from .enums import ActionType

class EventResponse(object):
	def __init__(self, cancellable, **kwargs):
		self._cancellable = cancellable
		self._cancelled = False
		self.response = None
		self.__dict__.update(kwargs)

	@property
	def cancelled(self):
		return self._cancelled

	@cancelled.setter
	def cancelled(self, new_value):
		if self._cancellable:
			self._cancelled = bool(new_value)
			return
		raise Exception(f"This event cannot be cancelled")

class IO_Wrapper:
	def __init__(self, data):
		self.token = token()
		self.data = data

class Persistance_IO:
	def __init__(self, path):
		self.path = path

	@staticmethod
	def list(path):
		output = []
		for file in os.listdir(path):
			if file.endswith(".iov"):
				output.append("".join(file.split(".iov")[0]))
		return tuple(output)

	@staticmethod
	def load(path):
		try:
			with open(path, "rb") as file:
				output = dill.load(file)
				file.close()
		except:
			output = None
		return output

	@staticmethod
	def write(path, intake):
		with open(path, "wb") as file:
			output = dill.dump(intake, file)
			file.close()

class IO_Var(Persistance_IO):
	def __init__(self, path):
		self.path = path

	def __len__(self):
		return len(os.listdir(self.path))

	@property
	def last(self):
		last = os.listdir(self.path)
		if len(last) == 0: 
			return
		return self.load(self.path+last[0])

	def remove(self, wrapper):
		token = wrapper.token if isinstance(wrapper, IO_Wrapper) else wrapper
		if token+".iov" in os.listdir(self.path):
			os.remove(self.path+token+".iov")

	def add(self, data):
		wrapped = IO_Wrapper(data)
		self.write(self.path+wrapped.token+".iov", wrapped)

class ReferencesIO(Persistance_IO):
	def __init__(self, path=None):
		super().__init__(path or Config().references_path)

	@property
	def itens(self):
		return self.list(self.path)
	

	def get(self, name):
		if name.lower() in self.list(self.path):
			obj = self.load(self.path+name.lower()+".iov")
			return obj
		return 

	def set(self, name, data):
		self.write(self.path+name.lower()+".iov", data)
