#! /usr/bin/env python
#Author: Abigail Lind
#usage: script.py [names] [fasta]
from Bio import SeqIO
import sys
def main(argv):

	name_file = open(sys.argv[1])
	names = {}
	for line in name_file:
		line = line.strip('\n')
		names[line.split('\t')[0]] = line.split('\t')[1]

	name_file.close()

	fasta = SeqIO.parse(sys.argv[2], 'fasta')
	for seq in fasta:
		name = seq.id.split('.')[0]
		new_name = names[name]
		print '>' + new_name
		print str(seq.seq)
if __name__ == "__main__":
	main(sys.argv)
