#!/usr/bin/env python3
#! Pour ananlyse : assemblage ONT ou PAcBio ( ! taille genome)
    


import os
import re
import shutil
import subprocess
from Bio import SeqIO
from docopt import docopt
from depot.AladinFun import *
from extraction import extract_reads
from fragmenter import fragment_fasta


def run_pipeline(data_format, mode, reference, reads, genome_size, length, fraction, threads):
    # Structure repertoire
    get_outdir("map")
    get_outdir("mini")

    # Noms fichiers
    FERR = open("assemblage.err", 'w')
    sam_file = "map/aln.sam"
    extract_reads_file = "map/read_ids.txt.fasta"
    extract_reads_frag_file = "map/read_ids.txt.fasta.frag.fasta"
    extract_reads_frag_file_150x = "map/read_ids.txt.fasta.frag.150x.fasta"

    overlap_file = "mini/overlaps.paf"
    unpolished_file = "mini/assembly.gfa"
    polished_file = "mini/polished.gfa"
    assembly_file = "mini/polished.fasta"
    aragorn_file = "mini/aragorn.txt"

    #formats des données
    if data_format == "N":
        format_mini = "map-ont"
        format_asm = "ava-ont"
    elif data_format == "P":
        format_mini = "map-pb"
        format_asm = "ava-pb"

    # Map des reads
    print(status_d['0'])
    sam_out = open(sam_file, 'w')
    subprocess.call(["minimap2", "--sam-hit-only", "-t", threads, "--secondary=no", "-ax",
                     format_mini, reference, reads],
                     stdout=sam_out, stderr=FERR)
    sam_out.close()
    fichier_vide(sam_file)

    # Extraction , fragmentation reads
    print(status_d['1'])
    read_ids = []
    sam_input = open_files(sam_file)
    for line in sam_input:
        elems = line.split("\t")
        if not line.startswith("@") and str(elems[4]) == "60":
            read_ids.append(elems[0])

    read_ids = list(set(read_ids))
    extract_reads(reads, read_ids, extract_reads_file)
    fragment_fasta(extract_reads_file, length, fraction)

    # Selection  ~150x de reads
    num_frags = len([1 for line in open(extract_reads_frag_file) if line.startswith(">")])
    num_150x = (genome_size*1000*200)/length
    fraction_select = min(num_150x/num_frags,1)
    seqtk_out = open(extract_reads_frag_file_150x,'w')
    subprocess.call(["seqtk", "seq", "-f", str(fraction_select), extract_reads_frag_file],
                     stdout=seqtk_out,stderr=FERR)
    seqtk_out.close()

    # Run mini pipeline
    print(status_d['2'])
    overlap_out = open(overlap_file, 'w')
    subprocess.call(["minimap2", "-t", threads, "-x", format_asm, extract_reads_frag_file_150x,
                     extract_reads_frag_file_150x], stdout=overlap_out, stderr=FERR)
    overlap_out.close()
    fichier_vide(overlap_file)

    unpolished_out = open(unpolished_file, 'w')
    subprocess.call(["miniasm", "-f", extract_reads_frag_file_150x, overlap_file],
                    stdout=unpolished_out, stderr=FERR)
    unpolished_out.close()
    fichier_vide(unpolished_file)

    polished_out = open(polished_file, 'w')
    subprocess.call(["minipolish", "-t", threads, extract_reads_frag_file_150x, unpolished_file],
                    stdout=polished_out, stderr=FERR)
    polished_out.close()
    fichier_vide(polished_file)

    # Convertir GFA to FASTA
    cmd = """awk '/^S/{{print ">"$2"\\n"$3}}' {} | fold > {}""".format(polished_file, assembly_file)
    os.system(cmd)

    # Run aragorn pour selectionner contig
    print(status_d['3'])
    aragorn_out = open(aragorn_file, 'w')
    if mode == "M":
        subprocess.call(["aragorn", "-l", "-gc5", "-mt", "-w", assembly_file],
                        stdout=aragorn_out, stderr=FERR)
    else:
        subprocess.call(["aragorn", "-l", "-gc1", "-m", "-t", "-w", assembly_file],
                        stdout=aragorn_out, stderr=FERR)
    aragorn_input = open_files(aragorn_file)
    trna_contigs = []
    trna_genes = []
    for line in aragorn_input:
        if line.startswith(">") and not line.startswith(">end"):
            elem = line.split(" ")
            header = elem[0].replace(">","")
            trna_contigs.append(header)
        elif "genes found" in line:
            elem = line.split(" ")
            num_trnas = int(elem[0])
            trna_genes.append(num_trnas)
    aragorn_contig = str(trna_contigs[trna_genes.index(max(trna_genes))]).rstrip()

    print("[!] Found contig " + aragorn_contig + " with " +  str(max(trna_genes)) + " mtRNAs")

    assembly = {}

    # Load assemblage fasta
    for record in SeqIO.parse(assembly_file, "fasta"):
        elem = str(record.id).split(" ")
        assembly[elem[0]] = str(record.seq)

    mito_contig = aragorn_contig

    circ_file = open("Mitochondion.fasta", 'w')
    circ_file.write(">" + mito_contig + "\n")
    circ_file.write(assembly[mito_contig] + "\n")
    circ_file.close()

    FERR.close()


############### Main ###############

def main():
    args = docopt(__doc__, version='1.1')
    reference = os.path.abspath(str(args['--reference']))
    reads = os.path.abspath(str(args['--reads']))
    dir_output = get_outdir(args['--dir_output'])
    length = int(args['--length'])
    fraction = float(args['--fraction'])
    threads = str(args['--threads'])
    cleanup = args['--cleanup']
    data_format = str(args['--data_format'])
    mode = str(args['--mode'])
    genome_size = int(args['--genome_size'])

    os.chdir(dir_output)

    check_programs("minimap2", "miniasm", "minipolish", "racon", "aragorn", "seqtk")

    run_pipeline(data_format, mode, reference, reads, genome_size, length, fraction, threads)

    if cleanup:
        shutil.rmtree("mini")
        shutil.rmtree("map")

    print(status_d['4'])
    resultats_dir = os.getcwd()
    print("Results be in "+resultats_dir+"/Mitochondion.fasta")

if __name__ == "__main__":
    main()
