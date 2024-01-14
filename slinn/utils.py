import re


def restartswith(text, reg):
	buf, largest = '', None
	for c in text:
		buf += c
		if re.sub(reg, '', buf) == '':
			largest = buf
	return largest is not None