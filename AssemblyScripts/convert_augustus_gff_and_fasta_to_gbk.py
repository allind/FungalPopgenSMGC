#! /usr/bin/env python
#Author: Abigail Lind
#usage: script.py [scaffolds fasta] [gff] [amino acid fasta]
#assumptions: GFF is sorted such that it goes gene -> mRNA -> CDS - not gene -> othergene -> mRNA -> whatever
#
#If this script does not work for you, look through the code at the comments. There are several places where you can make changes to accomodate small differences in file formats
from Bio import SeqIO
from Bio.Seq import Seq
import sys
import os

def main(argv):
	genome = {}
	#parse fasta
	for seq in SeqIO.parse(sys.argv[1], 'fasta'):
		genome[seq.id] = [str(seq.seq), []]
	#parse gff
	genes = {}
	gff = open(sys.argv[2])
	
	currgene = ""
	for line in gff:
		line = line.strip('\n')
		if '#' not in line[0]:#skip comment lines
			#parse gff line
			chrom = line.split('\t')[0]
			feature = line.split('\t')[2]
			start = line.split('\t')[3]
			end = line.split('\t')[4]
			strand = line.split('\t')[6]

			
			if feature == "gene":
			
				#name = line.split('\t')[-1].split(';')[1].split('=')[1]#get locus tag
				name= line.split('\t')[-1] #This has to be changed if you are not using Augustus gff

				if name not in genes:#initialize genes dict
					genes[name] = []
					
				genome[chrom][1].append(name)
				genes[name].append(strand)
				genes[name].append([start, end])
				currgene = name

			elif feature == "CDS":
				if len(genes[currgene]) < 3:
					genes[currgene].append([])
				genes[currgene][2].append([start, end])
				
	#structure of genes dict
	#genes[gene] = [strand, gene coords, [CDS coords], seq]
	#add sequences to genes hash
	for seq in SeqIO.parse(sys.argv[3], 'fasta'):
		name = seq.id.split('.')[0] #this is where you modify the gene name if gff and aa names dont match
		if name in genes:
			genes[name].append(str(seq.seq)) #this is what you change depending on aa vs nucl fasta
	

	#print gbk
	for chrom in genome:
		chrom_name = "_".join(chrom.split('_')[0:2])
		print 'LOCUS       ' + chrom_name + (28-len(chrom_name) - len(str(len(genome[chrom][0]))))* " " + str(len(genome[chrom][0])) + ' bp    DNA     linear   CON 17-AUG-2016'
		print 'FEATURES             Location/Qualifiers'
		print "     source          1.." + str(len(genome[chrom][0]))
		for gene in genome[chrom][1]:
			strand = genes[gene][0]
			if strand == '-':

				print "     gene            complement(<" + str(genes[gene][1][0]) + '..>' + str(genes[gene][1][1]) + ")"
				print "                     " + "/locus=" + gene

				if len(genes[gene][2]) > 1:
					cds_location = "complement(join("
					
					for i in range(len(genes[gene][2])-1, -1, -1):
						cds_location += str(genes[gene][2][i][0]) + '..' + str(genes[gene][2][i][1]) + ','
						
					cds_location = cds_location.strip(',')
					cds_location += "))"
				else:

					cds_location = "complement(" + str(genes[gene][2][0][0]) + '..' + str(genes[gene][2][0][1]) + ")"
				print "     CDS             " + cds_location
				print "                     /product=" + gene
				print "                     /translation=" + '"' + genes[gene][3].strip('*') + '"'
				print "                     /locus_tag=" + gene
			
			else:
				print "     gene            <" + str(genes[gene][1][0]) + '..>' + str(genes[gene][1][1])
				print "                     " + "/locus=" + gene
				if len(genes[gene][2]) > 1:
					cds_location = "join("
					for cds in genes[gene][2]:
						cds_location += str(cds[0]) + '..' + str(cds[1]) + ','
					cds_location = cds_location.strip(',')
					cds_location += ")"
				else:
					cds_location = str(genes[gene][2][0][0]) + '..' + str(genes[gene][2][0][1])
				
				print "     CDS             " + cds_location
				print "                     /product=" + gene
				print "                     /translation=" + '"' + genes[gene][3].strip('*') + '"'
				print "                     /locus_tag=" + gene
		print "ORIGIN"
		#print seq
		seq = genome[chrom][0]
		seqlen = len(seq)
		num_lines = seqlen / 60
		if (seqlen % 60) != 0:
			num_lines += 1

		counter = 1
		printstr = ""
		for i in range(0, num_lines):
			numspaces = 9 - len(str(counter))
			printstr += numspaces * " " + str(counter)

			j =0
			while j < 6:
				printstr += " " +seq[counter-1:counter+9]
				counter += 10
				j += 1

			print printstr
			printstr = ""
		print "//"

if __name__ == "__main__":
	main(sys.argv)
