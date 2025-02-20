#!/usr/bin/env python
#Renomme seq NCBI recuperees

from Bio import SeqIO
import sys
import argparse

# Créer l'objet parser
parser = argparse.ArgumentParser(description='Ce script récupère un fichier fasta de séquences pour en faire un fichier texte sous format fasta')


# Ajouter un argument pour le fichier FASTA à écrire
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--fasta', action='store_true', help='le fichier d\'input est en format FASTA')
group.add_argument('-g', '--genbank', action='store_true', help='le fichier d\'input est en format GenBank')

parser.add_argument('-i', '--inputfile', help='Chemin vers le fichier d\'entrée')
parser.add_argument('-d', '--idfile', help='Chemin vers le fichier d\'entrée')
parser.add_argument('-o', '--outputfile', help='Chemin vers le fichier de sortie')

# Analyser les arguments passés au script en utilisant la méthode parse_args() :
args = parser.parse_args()

# Ouvrir le fichier d'entrée avec les IDs
with open(args.idfile, 'r') as l:
    ids = [line.strip() for line in l]

# Ouvrir le fichier de sortie pour écrire les séquences correspondantes
with open(args.outputfile, 'w') as outputfile:
    # Ouvrir le fichier fasta d'entrée
    with open(args.inputfile, 'r') as inputfile:
        #ICI if fasta or gbk
        if args.fasta:
            type = "fasta"
        elif args.genbank:
            type = "genbank"
        else:
            sys.exit()
        for record in SeqIO.parse(inputfile, type):
            if record.id in ids:
                outputfile.write(">" + record.id + "  (" + str(len(str(record.seq))) + ")" + "\n" + str(record.seq) + "\n")
