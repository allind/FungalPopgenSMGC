#! /usr/bin/env python
#Author: Abigail Lind
#usage: script.py namefile gff
import sys
def main(argv):

	name_file = open(sys.argv[1])
	
	names = {}

	for line in name_file:
		line = line.strip('\n')
		names[line.split('\t')[0]] = line.split('\t')[1]

	name_file.close()

	gff = open(sys.argv[2])
	
	old = ""
	new = ""
	for line in gff:
		line = line.strip('\n')
		if "#" in line[0]:
			print line
		else:
			if line.split('\t')[2] == "gene":
				old = line.split('\t')[-1]
				new = names[old]
				line = line.replace(old, new)
				print line

			else:
				line = line.replace(old, new)
				print line

					
if __name__ == "__main__":
	main(sys.argv)
