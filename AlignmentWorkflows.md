# Identifying variants using a reference genome and short read alignments

This workflow is intended to use a reference genome and short read alignments to identify gene cluster loss, gene loss, and smaller variants like SNPs and indels within strains of a fungal species. Everything here is done relative to a reference genome. This approach can't identify novel SMGCs or changes in SMGC genomic location (see AssemblyWorkflow for that). This is **orders of magnitude** more sensitive than assembly for gene cluster loss and gene loss, however, so I strongly recommend you use both approaches.

# Identifying large structural variants like gene cluster, whole gene, and partial gene deletion

**Step 0.** Download a genome, GFF, protein files, and mRNA files for your reference genome. If you haven't already, run antiSMASH on this genome (see AssemblyWorkflow for tips).

**Step 1.** Align your reads against the reference genome.

Choose an appropriate aligner for your data. Our paper used bwa mem. Minimap2 is a newer good option. Bowtie2 is a good option. In my case, I had 101 bp paired-end reads and used bwa mem. Here is an example using bwa mem and picardtools. In addition to aligning, I sort the resulting output by coordinate, compress it to a BAM file, and remove duplicate reads.

```
bwa index [ref_genome.fa]
bwa mem -t [desired_cores] -M -R [read group information] [ref_genome.fa] [fwd_reads.fastq.gz] [rev_reads.fastq.gz] > [alignment.sam]
java -jar picard.jar SortSam INPUT=alignment.sam OUTPUT=alignment.sorted.bam SORT_ORDER=coordinate
java -jar picard.jar MarkDuplicates INPUT=[alignment.sorted.bam] OUTPUT=[alignment.sorted.deduped.bam] METRICS_FILE=[metrics.txt]
java -jar picard.jar BuildBamIndex INPUT=[alignment.sorted.deduped.bam]
````
This is a good time to evaluate your sequencing data. Check out picardtools CollectRawWgsMetrics, for example.

**Step 2.** Determine gene coverage using bedtools.

The purpose of this is to determine which genes are or are present in the isolate you've sequenced. You will need [bedtools](https://bedtools.readthedocs.io/en/latest/) for this.

Create a bed file for all the genes in the reference genome. This just needs to be "scaffold\tstart_coord\tend_coord\tgenename". I have a script that will do this for certain GFFs, but yours might be formatted differently.
```
create_gene_bed.py [ref_genome.gff] > [genes.bed]
bedtools coverage -sorted -a [genes.bed] -b [alignment.sorted.deduped.bam] > [gene_coverage.txt]
```

The output for this will be tab delimited: "Chromosome, start_coord, end_coord genename, reads_mapping_to_region, bases_covered, gene_length, percentage_of_bases_covered"


I also recommend you run bedtools coverage on the entire genome. This helps you determine if any gene losses or cluster losses are part of a larger deletion or not.

Depending on the size of your genome, 10 Kb or 1 Kb window sizes could be appropriate. The "-w" flag controls this in bedtools makewindows. You need a file with the lengths of all contigs in your reference genome as input. If you don't have that, I have a script that generates it.
```
count_contig_length.py [ref_genome.fa] > [ref_genome_contig_lengths.txt]
bedtools makewindows -g ref_genome_contig_lengths.txt -w 10000 > ref_genome_10kb_windows.txt
bedtools coverage -sorted -a [ref_genome_10kb_windows.txt] -b [alignment.sorted.deduped.bam] > [genome_coverage_10kb.txt]
```

**Step 3.** Explore your results.

Look at the coverage of all of the reference genome SMGCs in the gene coverage windows. Any time there is less than 100% coverage of a SMGC gene, it's worth investigating. Visualize the alignments around each non-100% coverage gene in an alignment browser like [IGV](http://software.broadinstitute.org/software/igv/). This is be very helpful for figuring out exactly what's going on for each non-100% coverage case.

# Identifying SNPs and indels

Briefly, use the [GATK pipeline](https://software.broadinstitute.org/gatk/) and genotype all your strains together (the more strains, the better your power). Use [SnpEFF](http://snpeff.sourceforge.net/) for determining what kind of impact the variants you find will have. Details under development.
