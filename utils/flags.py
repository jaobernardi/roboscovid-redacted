from structures.files import Messages

def flag_define(inp):
	msg = Messages()
	if "amarel" in inp.lower():
		return msg.flags[0]
	elif "laranj" in inp.lower():
		return msg.flags[1]
	elif "verm" in inp.lower():
		return msg.flags[2]
	elif "pret" in inp.lower():
		return msg.flags[3]
	return "- Indefinida -"

def value_assign(inp, ranges=[25, 50, 75, 100], values=["🟡", "🟠", "🔴", "⚫"]):
	if inp <= ranges[0]:
		return values[0]

	elif inp >= ranges[0] and inp < ranges[1]:
		return values[1]

	elif inp >= ranges[1] and inp < ranges[2]:
		return values[2]

	else:
		return values[3]
