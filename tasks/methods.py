import logging
import multiprocessing
import threading

def add_process(name, function, *args):
	logging.info(f"Starting new process - {name}")
	process = multiprocessing.Process(target=function, args=args)
	process.start()
	return process

def add_thread(name, function, *args):
	logging.info(f"Starting new thread - {name}")
	thread = threading.Thread(target=function, args=args)
	thread.start()
	return thread

class thread_function:
	def __init__(self, function):
		self.function = function

	def __call__(self, *args):
		return add_thread("Unnamed", self.function, *args)