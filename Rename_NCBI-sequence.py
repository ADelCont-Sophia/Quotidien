#!/usr/bin/env python3

from Bio import SeqIO
import argparse

# Créer l'objet parser
parser = argparse.ArgumentParser(description='Extrait des séquences d’un fichier FASTA ou GenBank selon une liste d’ID')

# Donner les options mutuellement exclusives : soit FASTA, soit GenBank
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-f', '--fasta', action='store_true', help='le fichier d\'input est en format FASTA')
group.add_argument('-g', '--genbank', action='store_true', help='le fichier d\'input est en format GenBank')


# Chemin vers le fichier de séquences
parser.add_argument('fichier', help='Chemin vers le fichier de séquences à parser (.fasta ou .gbk)')             # parser.add_argument ('-i', '--inputfile')  # parser.add_argument ('-o', '--outputfile')

# Chemin vers le fichier contenant les identifiants à extraire
parser.add_argument('-i', '--idfile', required=True, help='Fichier texte avec une liste d’IDs (un par ligne)')

# Chemin vers le fichier de sortie
parser.add_argument('-o', '--outputfile', required=True, help='Fichier de sortie en format FASTA')

# Analyser les arguments
args = parser.parse_args()

##Traitement des fichiers ##

# Détermination du format à utiliser selon l'option choisie
format_type = "fasta" if args.fasta else "genbank"

# Ouvrir le fichier d'entrée avec les IDs

# Lecture de la liste des IDs à extraire depuis le fichier
with open(args.idfile, 'r') as f:
    ids = {line.strip() for line in f}  # Stockés sous forme d’ensemble :recherche rapide

# Ouverture du fichier d’entrée et de sortie
with open(args.fichier, 'r') as inputfile, open(args.outputfile, 'w') as output:
    for record in SeqIO.parse(inputfile, format_type):
        if record.id in ids:
            output.write(">" + record.id + "  (" + str(len(str(record.seq))) + ")" + "\n" + str(record.seq) + "\n")

if args.fasta:
    # Le chemin vers le fichier FASTA a été spécifié
    fichier_sortie = args.fasta
    print('Fichier FASTA à écrire :', fichier_sortie)
elif args.genbank:
    # Le chemin vers le fichier GenBank a été spécifié
    fichier_sortie = args.genbank
    print('Fichier GenBank à écrire :', fichier_sortie)
else:
    print('Aucun fichier FASTA ou GenBank spécifié')
