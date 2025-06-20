#!/usr/bin/env python3

import subprocess
import os

def run(desc, cmd):
    print(f"\n[Étape] {desc}")
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERREUR] Échec : {desc}")
        exit(1)
    print(f"[OK] {desc}")

# Fichiers d'entrée/sortie
input_fasta = "sequences.fasta"
aligned_msa = "aligned.msa"
trimmed_msa = "trimmed.msa"
model_out = "modeltest_output"
tree_prefix = "T1"

# Étape 1 : Alignement avec MUSCLE v5
run("Alignement avec MUSCLE v5", f"muscle -super5 {input_fasta} -output {aligned_msa}")

# Étape 2 : Trimming avec trimal
run("Nettoyage des alignements avec trimAl", f"trimal -in {aligned_msa} -automated1 -out {trimmed_msa}")

# Étape 3 : Détermination du meilleur modèle avec modeltest-ng
run("Sélection du modèle avec ModelTest-NG", f"modeltest-ng -d nt -i {trimmed_msa} -o {model_out}")

# Étape 4 : Extraction du modèle depuis les résultats
with open(f"{model_out}.model", "r") as f:
    for line in f:
        if line.startswith("Best model"):
            model = line.strip().split()[-1]
            break
    else:
        print("[ERREUR] Modèle non trouvé dans modeltest-ng.")
        exit(1)

print(f"[INFO] Modèle sélectionné : {model}")

# Étape 5 : Reconstruction phylogénétique avec RAxML-ng
run("RAxML-ng (ML + bootstrap)", 
    f"raxml-ng --all --msa {trimmed_msa} --model {model} --prefix {tree_prefix} "
    f"--bs-trees autoMRE --bs-metric tbe,fbp --threads 8")

# Résumé final
print("\n[Résumé]")
print(f"- Alignement MSA : {aligned_msa}")
print(f"- Alignement trimé : {trimmed_msa}")
print(f"- Modèle choisi : {model}")
print(f"- Arbres : {tree_prefix}.raxml.bestTree, {tree_prefix}.raxml.support")
