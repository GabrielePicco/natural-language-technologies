"""
Testing the Lesk disambiguation algorithm on the first 50 sentences of the SemCor corpora
"""

import pprint
import re
from nltk.corpus import semcor
from word_disambiguation_utils import lesk

extract_true_syn_regex = "Lemma\('(.+?)'\), .Tree\('NN', .'([a-zA-Z]+?)'\]"

test_sentences = []
for sentence, tagged_sentence in zip(semcor.sents()[:50], semcor.tagged_sents(tag='both')[:50]):
    syn = re.search(extract_true_syn_regex, pprint.pformat(tagged_sentence))
    if syn.group(2) == "per":
        print("error")
    if syn:
        test_sentences.append((sentence, syn.group(2), syn.group(1)[:syn.group(1).rindex('.')]))

correct_disambiguations = 0
print("\nIncorrect disambiguation: \n")
for (sentence, ambiguous_word, syn_corret) in test_sentences:
    syn = lesk(" ".join(sentence), ambiguous_word)
    if str(syn)[8:-2] in syn_corret:
        correct_disambiguations += 1
    else:
        print("{} : {}".format(str(syn)[8:-2], syn_corret))

print("\nDisambiguation accuracy: {}".format(correct_disambiguations / len(test_sentences)))
