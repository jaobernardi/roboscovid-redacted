# main file
import logging
import argparse
import addons
import tasks
import events
import twitter

import whatsapp
import datasets
parser = argparse.ArgumentParser()



def main():
	parser.add_argument("-wao", "--whatsapp_only", help="initializes only the WhatsApp process", action="store_true")
	parser.add_argument("-tto", "--twitter_only", help="initializes only the TwitterIO process", action="store_true")
	parser.add_argument("-tfo", help="initializes only the required process for Twitter flow", action="store_true")
	parser.add_argument("-da", "--disable_addons", help="disable addon loading", action="store_true")

	args = parser.parse_args()



	if not args.disable_addons:
		import addons


	event = events.call_event("prestartup", True, arg_parse=args)
	import scheduler
	if event.cancelled:
		print("Startup denied by event call")
		exit(-1)
	if args.whatsapp_only:
		print(1)
		tasks.add_process("WhatsApp", whatsapp.WhatsApp)
	elif args.twitter_only:
		print(2)
		tasks.add_process("Twitter", twitter.TwitterLoop)
	elif args.tfo:
		print(3)
		tasks.add_process("Twitter", twitter.TwitterLoop)
		tasks.add_process("DatasetCollect", datasets.DatasetCollect)
	else:
		print(4)
		tasks.add_process("WhatsApp", whatsapp.WhatsApp)
		tasks.add_process("Twitter", twitter.TwitterLoop)
		tasks.add_process("DatasetCollect", datasets.DatasetCollect)
		tasks.add_thread("Scheduler", scheduler.ScheduleTask)

	events.call_event("poststartup")
	
	try:
		while True:
			pass
	except KeyboardInterrupt:
		exit()
if __name__ == '__main__':
	main()