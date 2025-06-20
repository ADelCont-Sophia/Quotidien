
import feedparser
import xml.etree.ElementTree as ET

# URL du flux RSS
rss_url = "https://bmcbioinformatics.biomedcentral.com/rss.xml"

# Mots-clés à rechercher
keywords = ["illumina", "annotation", "genome", "deep learning"]

# Analyse du flux
feed = feedparser.parse(rss_url)

# Création d'un arbre XML filtré
root = ET.Element("FilteredArticles")

for entry in feed.entries:
    content = (entry.title + " " + entry.get("summary", "")).lower()
    if any(kw in content for kw in keywords):
        article = ET.SubElement(root, "Article")
        ET.SubElement(article, "Title").text = entry.title
        ET.SubElement(article, "Link").text = entry.link
        ET.SubElement(article, "Published").text = entry.get("published", "N/A")
        ET.SubElement(article, "Summary").text = entry.get("summary", "N/A")

# Sauvegarde du fichier XML
tree = ET.ElementTree(root)
tree.write("filtered_bmc_bioinformatics.xml", encoding="utf-8", xml_declaration=True)

print("Fichier XML généré : filtered_bmc_bioinformatics.xml")
