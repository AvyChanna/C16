import re, sys, time

def main(file):
	lines = []
	with open(file, "r") as f:
		for line in f:
			line = line.split(";", 1)[0]
			line.upper()
			print(line.split())

			pass



main("a.ass")