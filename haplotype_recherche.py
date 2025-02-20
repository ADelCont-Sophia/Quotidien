#! Recherche des haplotypes

from Bio import SeqIO

def lire_sequences(fichier):
    """Lire les séquences d'un fichier FASTA."""
    sequences = {}
    with open(fichier, "r") as f:
        for record in SeqIO.parse(f, "fasta"):
            sequences[record.description] = {"description": record.description, "seq": record.seq}
    return sequences

def comparer_sequences(seq1, seq2):
    """Comparer deux séquences et retourner le pourcentage de similarité."""
    nb_identiques = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return (nb_identiques / len(seq1)) * 100

# Lire les séquences du fichier 1
sequences_fichier1 = lire_sequences("fichier1.fasta")

# Lire les séquences du fichier 2
sequences_fichier2 = lire_sequences("fichier2.fasta")

# Vérifier si une séquence du fichier 1 correspond à 100% avec une séquence du fichier 2
found_match = False

for id_seq1, seq1 in sequences_fichier1.items():
    for id_seq2, seq2 in sequences_fichier2.items():
        sim = comparer_sequences(seq1, seq2)
        if sim == 100.0:
            print(f"Une séquence du fichier 1 ({id_seq1}) correspond à 100% avec une séquence du fichier 2 ({id_seq2}).")
            print(f"Séquence du fichier 1: {seq1}")
            print(f"Séquence du fichier 2: {seq2}")
            found_match = True
            break  # Stop searching for this seq2, move to the next seq1
    if found_match:
        break  # Stop searching for more matches

if not found_match:
    print("Aucune correspondance à 100% trouvée entre les séquences des deux fichiers.")
