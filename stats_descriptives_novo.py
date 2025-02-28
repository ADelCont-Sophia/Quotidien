import gzip
from statistics import median

def read_fastq(file_path):
    sequences = []
    with (gzip.open if file_path.endswith('.gz') else open)(file_path, 'rt') as file:
        lines = file.readlines()
        for i in range(1, len(lines), 4):  # FASTQ files have sequences on every 4th line starting from 2nd line.
            sequence = lines[i].strip()
            sequences.append(sequence)
    return sequences

def calculate_stats(sequences):
    lengths = [len(seq) for seq in sequences]
    total_sequences = len(lengths)
    total_bases = sum(lengths)
    sorted_lengths = sorted(lengths)
    n50_value = 0
    n50 = 0

    for i, length in enumerate(sorted_lengths[::-1]):
        n50_value += length
        if n50_value >= total_bases / 2:
            n50 = length
            break

    mean = total_bases / total_sequences
    median_value = median(sorted_lengths)

    return n50, mean, median_value, total_sequences


input_files = ["/home/maintenance/projets/SHFrag2/fastq_pass/FAU80345_pass_8b4b00cf_774856e7_0.fastq.gz"]  # Add the list of input FASTQ files here

for file_path in input_files:
        sequences = read_fastq(file_path)
        n50, mean, median_value, total_sequences = calculate_stats(sequences)

        print(f"File: {file_path}")
        print(f"N50: {n50}")
        print(f"Mean: {mean}")
        print(f"Median: {median_value}")
        print(f"Number of sequences: {total_sequences}")
        print("-----------------------")
