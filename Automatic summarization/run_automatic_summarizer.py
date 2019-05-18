import os
from automatic_summarizer import Summarizer, Granularity

NASARI_PATH = "./data/nasari_small.txt"
OUTPUT_FOLDER = "./data/summary"
DOCUMENTS = ["./data/sample/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt",
             "./data/sample/People-Arent-Upgrading-Smartphones-as-Quickly-and-That-Is-Bad-for-Apple.txt",
             "./data/sample/The-Last-Man-on-the-Moon--Eugene-Cernan-gives-a-compelling-account.txt"]

summarizer = Summarizer(nasari_file_path=NASARI_PATH)
for document in DOCUMENTS:
    sm = summarizer.summarize_document(document, percentage=0.7)
    print(sm, file=open(os.path.join(OUTPUT_FOLDER, os.path.basename(document)), 'w'))

for document in DOCUMENTS:
    sm = summarizer.summarize_document(document, percentage=0.7, granularity=Granularity.SENTENCE)
    print(sm, file=open(os.path.join(OUTPUT_FOLDER, "sentence", os.path.basename(document)), 'w'))

