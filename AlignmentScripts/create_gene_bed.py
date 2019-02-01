#! /usr/bin/env python
#Author: Abigail Lind
#usage: script.py [gff]
import sys
def main(argv):
	gff =open(sys.argv[1])
	for line in gff:
		line = line.strip('\n')
		if "#" in line[0]:
			continue
		if "gene" in line.split('\t')[2]:
			start = line.split('\t')[3]
			end = line.split('\t')[4]
			if int(start) > int(end):
				tmp = start
				start = end
				end = tmp
			if ";" in line.split('\t')[-1]:
				name = line.split('\t')[-1].split(';')[0].split('=')[1] #change this line if gene line of GFF isn't ID=Genename;
			else:
				name = line.split("\t")[-1]
			print line.split('\t')[0] + '\t' + start + '\t' + end + '\t' + name
	gff.close()
if __name__ == "__main__":
	main(sys.argv)
