#! /usr/bin/env python
#Author: Abigail Lind
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
import sys
def main(argv):
    fas = SeqIO.parse(sys.argv[1], 'fasta')

    for seq in fas:

        print '>' + seq.id
        print seq.seq.translate().strip('*')

if __name__ == "__main__":
    main(sys.argv)
