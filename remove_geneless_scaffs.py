#! /usr/bin/env python
#Author: Abigail Lind
from Bio import SeqIO
import sys
def main(argv):
	
	for seq in SeqIO.parse(open(sys.argv[1]), 'genbank'):
		if len(seq.features) > 1:
			print seq.format("genbank")
if __name__ == "__main__":
	main(sys.argv)
