python
rule all:
    input:
        "T1.raxml.support"

rule align:
    input:
        "sequences.fasta"
    output:
        "aligned.aln"
    shell:
        "muscle -align {input} -output {output}"

rule trim:
    input:
        "aligned.aln"
    output:
        "trimmed.msa"
    shell:
        "trimal -in {input} -automated1 -out {output}"

rule modeltest:
    input:
        "trimmed.msa"
    output:
        "modeltest.out"
    shell:
        "modeltest-ng -d nt -i {input} -o {output}"

rule parse_modeltest:
    input:
        "modeltest.out"
    output:
        "best_model.txt"
    run:
        import re
        with open(input[0], 'r') as f:
            content = f.read()
        match = re.search(r'Best model according to BIC\n(.+)', content)
        if match:
            best_model = match.group(1).split()[0]
            with open(output[0], 'w') as f:
                f.write(best_model)

rule raxml_ng:
    input:
        msa="trimmed.msa",
        model="best_model.txt"
    output:
        "T1.raxml.support"
    shell:
        "raxml-ng --all --msa {input.msa} --model $(cat {input.model}) --prefix T1 --bs-trees autoMRE --bs-metric tbe,fbp"
