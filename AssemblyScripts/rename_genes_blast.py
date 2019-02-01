#! /usr/bin/env python
#Author: Abigail Lind
#usage: script.py organism_name cds gff rbbh
#output is old'\t'new
#new names are: organismname-scaffold-augustusname[-reciprocal_best_blast_hit]
from Bio import SeqIO
import sys
def main(argv):
	
        org_name = sys.argv[1]
	genes = []
	names = {}

	cds = SeqIO.parse(sys.argv[2], 'fasta')
	genes = [seq.id.split('.')[0] for seq in cds]

	for gene in genes:
		names[gene] = ""

	gff = open(sys.argv[3])
	for line in gff:
		if line[0] == '#' or line.split('\t')[2] != "gene":
			continue
		else:
			line = line.strip('\n')
			gene = line.split('\t')[-1]
			node = "_".join(line.split('\t')[0].split('_')[0:2])
			names[gene] = org_name + '-' + node + '-' + gene
	gff.close()
	
	rbbh = open(sys.argv[4])
	rbbh.readline()
	for line in rbbh:
		gene = line.split('\t')[0].split('.')[0]
		hit = line.split('\t')[1]
		curr = names[gene]
		names[gene] = curr + '-' + hit
	rbbh.close()

	for gene in names:
		print gene + '\t' + names[gene]
		
if __name__ == "__main__":
	main(sys.argv)
