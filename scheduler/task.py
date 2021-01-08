from datetime import datetime
from .methods import schedule_list
from events import call_event


def ScheduleTask():
	while True:
		now = datetime.now()
		for time in list(schedule_list):
			if time < now:
				for item in list(schedule_list[time]): # [[name, function, args, kwargs]]
					event = call_event("schedulecall", name=item[0], function=item[1], args=item[2], kwargs=item[3])
					if not event.cancelled:
						schedule_list[time].remove(item)
					item[1](*item[2], **item[3])
				schedule_list.pop(time)
