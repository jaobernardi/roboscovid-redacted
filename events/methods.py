from structures import EventResponse

events = {}

def create_event(event_name):
	events[event_name] = {}

def add_handle(event_name, priority = 0):
	def wrapper(function):
		if event_name not in events:
			create_event(event_name)

		if priority not in events[event_name]:
			events[event_name][priority] = []

		events[event_name][priority].append(function)
	return wrapper

def call_event(event_name, cancellable=False, **kwargs):
	if not event_name in events:
		return EventResponse(cancellable=cancellable, **kwargs)

	order = list(events[event_name])
	order.sort()
	order.reverse()

	event = EventResponse(cancellable=cancellable, **kwargs)
	for priority in order:
		for handle in events[event_name][priority]:
			if event.cancelled:
				return event
			event.response = handle(event)
	return event