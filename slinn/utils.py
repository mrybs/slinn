import re


def restartswith(text, reg):
	buf, largest = '', None
	for c in text:
		buf += c
		if re.sub(reg, '', buf) == '':
			largest = buf
	return largest is not None

def rematcheswith(text, reg): 
	return re.match('^'+reg+'$', text) is not None

def Bmin_restartswith_size(text, reg):
	buf, smallest = text, None
	for _ in range(len(text)):
		buf = buf[:-1]
		if re.sub(reg, '', buf) == '':
			smallest = buf
		else:
			break
	return len(smallest) if smallest is not None else 2147483647

def min_restartswith_size(text, reg):
	buf, smallest = text, None
	for _ in range(len(text)):
		buf = buf[:-1]
		if re.sub(reg, '', buf) == '':
			smallest = buf
	return len(smallest) if smallest is not None else 2147483647
