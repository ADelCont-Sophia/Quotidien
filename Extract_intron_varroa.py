import subprocess

# Fonctions utilitaires
def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

# Téléchargements
run_cmd('wget -O Vd_octb2r_mRNA.fasta "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=nuccore&id=XM_022808967.1&report=fasta"')
run_cmd('wget -O genome.fasta.gz "https://ftp.ebi.ac.uk/pub/databases/ena/wgs/public/be/BEIS01.fasta.gz"')

# Décompression
run_cmd('gunzip genome.fasta.gz')

# Préparation BLAST
run_cmd('makeblastdb -in genome.fasta -dbtype nucl')

# Alignement BLAST
run_cmd('blastn -query Vd_octb2r_mRNA.fasta -db genome.fasta -outfmt 6 > Vd_octb2r_mRNA.blast')

# Extraction segment génomique avec seqkit
segment_start, segment_end = 21409138, 21552323
run_cmd(f'seqkit subseq -r {segment_start}:{segment_end} genome.fasta > seg.fasta')

# Alignement exonerate (est2genome)
run_cmd('exonerate --model est2genome --bestn 1 --showtargetgff 1 Vd_octb2r_mRNA.fasta seg.fasta > Vd_octb2r_mRNA.exonerate')

# Extraction fragment intron/exon
fragment_start, fragment_end = 4507, 7581
run_cmd(f'seqkit subseq -r {fragment_start}:{fragment_end} seg.fasta > frag.fasta')


print("Workflow terminé.")
