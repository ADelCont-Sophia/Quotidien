import gzip
from statistics import median  # Importation de la fonction 'median' pour calculer la médiane

# Fonction pour lire un fichier FASTQ et extraire les séquences
def read_fastq(file_path):
    sequences = []  # Liste pour stocker les séquences
    # On ouvre le fichier, en fonction de son extension (.gz ou non)
    with (gzip.open if file_path.endswith('.gz') else open)(file_path, 'rt') as file:
        lines = file.readlines()  # Lire toutes les lignes du fichier
        for i in range(1, len(lines), 4):  # Les séquences se trouvent sur les lignes 2, 6, 10, ...
            sequence = lines[i].strip()  # Récupérer la séquence en supprimant les espaces inutiles
            sequences.append(sequence)  # Ajouter la séquence à la liste
    return sequences  # Retourner la liste des séquences

# Fonction pour calculer les statistiques principales sur les séquences
def calculate_stats(sequences):
    # Calcul des longueurs des séquences
    lengths = [len(seq) for seq in sequences]
    total_sequences = len(lengths)  # Nombre total de séquences
    total_bases = sum(lengths)  # Total des bases (somme des longueurs des séquences)

    # Tri des longueurs des séquences
    sorted_lengths = sorted(lengths)

    # Initialisation des variables pour le calcul de N50
    n50_value = 0
    n50 = 0

    # Calcul de la valeur N50 en parcourant les séquences triées par taille décroissante
    for i, length in enumerate(sorted_lengths[::-1]):  # Parcours des longueurs triées à l'envers (décroissant)
        n50_value += length
        if n50_value >= total_bases / 2:  # Lorsque la somme dépasse 50% du total des bases
            n50 = length  # La longueur de la séquence est la valeur N50
            break  # On arrête le calcul dès qu'on a trouvé la valeur N50

    # Calcul de la moyenne de la longueur des séquences
    mean = total_bases / total_sequences
    # Calcul de la médiane des longueurs des séquences
    median_value = median(sorted_lengths)

    # Retourner les résultats : N50, moyenne, médiane et le nombre total de séquences
    return n50, mean, median_value, total_sequences

# Programme principal qui va traiter les fichiers et afficher les résultats
if __name__ == "__main__":
    # Liste des fichiers FASTQ à traiter (ajoutez vos fichiers ici)
    input_files = ["projets/SHFrag2/fastq_pass/FAU80345_pass_8b4b00cf_774856e7_0.fastq.gz"]

    # Boucle sur tous les fichiers à traiter
    for file_path in input_files:
        sequences = read_fastq(file_path)  # Lire les séquences du fichier
        # Calculer les statistiques pour ces séquences
        n50, mean, median_value, total_sequences = calculate_stats(sequences)

        # Afficher les résultats
        print(f"File: {file_path}")  # Affiche le nom du fichier traité
        print(f"N50: {n50}")  # Affiche la valeur N50
        print(f"Mean: {mean}")  # Affiche la moyenne des longueurs de séquences
        print(f"Median: {median_value}")  # Affiche la médiane des longueurs de séquences
        print(f"Number of sequences: {total_sequences}")  # Affiche le nombre de séquences
        print("-----------------------")  # Séparation visuelle entre les fichiers

        # Création du graphique
        plt.figure(figsize=(10, 6))
        plt.hist(lengths, bins=50, color='skyblue', edgecolor='black')
        plt.title(f"Distribution des longueurs de séquences\n{file_path}")
        lt.xlabel("Longueur des séquences")
        plt.ylabel("Fréquence")
        plt.grid(True)

       # Nom fichier sortie pour du graphique
        output_image = file_path.split("/")[-1].replace(".fastq.gz", "_length_distribution.png")
        plt.savefig(output_image)
        plt.close()

        print(f" Graphique sauvegardé sous : {output_image}")
