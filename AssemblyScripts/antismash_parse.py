#! /usr/bin/env python
#Author: Abigail Lind
#usage: script.py [geneclusters.txt]
#output: clusternum\tchrom\gene
import sys
def main(argv):

	antismash = open(sys.argv[1])
	clusts = 0
	curr_clust = ""
	
	for line in antismash:
		line = line.strip('\n')
		clusts += 1
		scaff = line.split('\t')[0]
		genes = line.split('\t')[3].split(';')
		curr_clust = "clust_" + str(clusts)
		for gene in genes:
			print curr_clust + '\t' + scaff + '\t' + gene
	antismash.close()
if __name__ == "__main__":
	main(sys.argv)
