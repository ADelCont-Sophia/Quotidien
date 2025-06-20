import gzip
from statistics import median
#lecture FASTQ et extraction seq
def read_fastq(file_path):
    sequences = []
    #ouverture fichier compresse ou pas
    with (gzip.open if file_path.endswith('.gz') else open)(file_path, 'rt') as file:
        lines = file.readlines()
        for i in range(1, len(lines), 4):  # FASTQ contient les séquences sur  ligne 4e, en commençant à partir de la ligne 2"
            sequence = lines[i].strip()
            sequences.append(sequence)
    return sequences
#calcul stats principales sur seq :(N50, moyenen, mediane)
def calculate_stats(sequences):
    lengths = [len(seq) for seq in sequences]
    total_sequences = len(lengths)
    total_bases = sum(lengths)
    sorted_lengths = sorted(lengths)
    n50_value = 0
    n50 = 0
#calcule de N50
    for i, length in enumerate(sorted_lengths[::-1]):
        n50_value += length
        if n50_value >= total_bases / 2:
            n50 = length
            break
#calcul moy de longeur des seq
    mean = total_bases / total_sequences
#calcul mediane
    median_value = median(sorted_lengths)

    return n50, mean, median_value, total_sequences

if __name__ == "__main__":
input_files = ["/home/adelcont/projets/SHFrag2/fastq_pass/FAU80345_pass_8b4b00cf_774856e7_0.fastq.gz"]  # Ajout de la liste input FASTQ
#boucle sur fichiers
for file_path in input_files:
        sequences = read_fastq(file_path)
        n50, mean, median_value, total_sequences = calculate_stats(sequences)
#Resultast
        print(f"File: {file_path}")
        print(f"N50: {n50}")
        print(f"Mean: {mean}")
        print(f"Median: {median_value}")
        print(f"Number of sequences: {total_sequences}")
        print("-----------------------")
