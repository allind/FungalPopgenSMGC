#! /usr/bin/env python
#Author: Abigail Lind
#This script assumes that the GFF is already sorted by scaffold. If not, you can either sort the output, or sort the gff first.
#input: script.py gff
#output: scaffold\tgenename\tstartcoord\tendcoord\tstrand
import sys
def main(argv):

	gff = open(sys.argv[1])
	for line in gff:
		if "#" not in line[0] and line.split('\t')[2] == "gene":
			print line.split('\t')[0] + '\t' + line.split('\t')[-1].strip('\n') + '\t' + line.split('\t')[3] + '\t' + line.split('\t')[4] + '\t' + line.split('\t')[6]
if __name__ == "__main__":
	main(sys.argv)
