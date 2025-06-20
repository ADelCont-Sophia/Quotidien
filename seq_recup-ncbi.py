database_file = config_opts["database_file"]
accs_exclude_file = config_opts["accs_exclude_file"]
retmax = int(config_opts["retmax"])

accs_to_exclude = []
with open(accs_exclude_file,"r") as accs_exclude_handle:
    for line in accs_exclude_handle:
        acc,info = line.split(' ', 1)
        accs_to_exclude.append(acc)

Entrez.email = "aurelie.delcont@anses.fr" #email obligatoire
handle = Entrez.esearch(db="nucleotide",idtype="acc",term=search_term,retmax=retmax)  # "acc" :identifiants retournés soient des accessions
record = Entrez.read(handle)                                                          # exemple :term="Varooa destructor" [Organism] AND COI[Gene]", retmax=10)
ncbi_accs = record["IdList"]
handle.close()

ids_present = []
if os.path.isfile(database_file):
    database_handle = open(database_file,'r')
    records = SeqIO.parse(database_handle,"fasta")
    for record in records:
        ids_present.append(record.id)
    database_handle.close()

final_accs = []
for acc in ncbi_accs:
    if acc not in accs_to_exclude and acc not in ids_present:
        final_accs.append(acc)
        ids_present.append(acc)

today=str(datetime.date.today())

log_file_name = database_file + ".log"
log_file_handle = open(log_file_name,'a')

if len(final_accs) == 0:

    log_file_handle.write(today + ": Up to date\n")

else:
    handle = Entrez.efetch(db="nucleotide",id=final_accs,rettype="fasta")
    records = SeqIO.parse(handle,"fasta")
    database_handle = open(database_file,'a')

    for record in records:
        database_handle.write(">" + record.id + "\n" + str(record.seq) + "\n")

    database_handle.close()

    if len(final_accs)>1:
        if len(final_accs)>5:
            record_txt = " records.\n"
        else:
            record_txt = " records. " + str(final_accs) + " \n"
    else:
        record_txt = " record. " + str(final_accs) + " \n"

    log_file_handle.write(today + ": Added " + str(len(final_accs)) + record_txt)
    handle.close()

log_file_handle.close()
