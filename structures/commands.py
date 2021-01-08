from .files import Messages
import difflib


class CommandMap:
	def __init__(self):
		self.commands = {}

	def add(self, name, alias: list, desciption="", permission=None):
		def wrapper(function):
			cmd = Command(function, name, desciption, permission)
			for alia in alias:
				self.commands[alia] = cmd
		return wrapper

	@property
	def list(self):
		commands = []
		for alias in self.commands:
			cmd = self.commands[alias]
			if cmd not in commands:
				commands.append(cmd)
		return commands

	def match(self, user, message):
		alia = message.split(" ")[0]
		for alias in self.commands:
			if difflib.SequenceMatcher(a=alias.lower(), b=alia.lower()).ratio() > 0.85:
				return True, self.commands[alias](user, message)
		msg = Messages()
		return False, msg.errors["commands_not_found"]

class Command:
	def __init__(self, handler, name, desciption="", permission=None):
		self.handler = handler
		self.name = name
		self.desciption = desciption
		self.permission=permission

	def __call__(self, user, message):
		msg = Messages()
		if self.permission and not user.has_permission(self.permission):
			return msg.errors["commands_no_permission"]
		return self.handler(user, message)

	def format(self):
		return f"```{self.name}```" + (f" - _{self.desciption}_" if self.desciption else "")