from datetime import *
from events import call_event

schedule_list = {}

def add_schedule(name, function, execute_time, *args, **kwargs):
	event = call_event("scheduleadd", name=name, function=function, execute_time=execute_time, args=args, kwargs=kwargs)

	if event.cancelled:
		raise Exception('Schedule couldn\'t be added due to event cancellation')
	if execute_time not in schedule_list:
		schedule_list[execute_time] = []
	schedule_list[execute_time].append([name, function, args, kwargs])
	print(schedule_list)


def remove_schedule(name):
	for time in schedule_list:
		for scheduled_events in list(schedule_list[time]):
			if scheduled_events[0] == name:
				schedule_list[time].remove(scheduled_events)
