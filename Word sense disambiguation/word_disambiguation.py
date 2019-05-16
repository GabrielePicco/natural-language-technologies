import re

from word_disambiguation_utils import lesk, generate_alternative_sentence


def read_file_lines(file_path):
    """
    Simple function for reading lines from files
    :type file_path: the file path
    :return: list of lines in the file
    """
    with open(file_path) as f:
        lines = f.readlines()
    return lines


def find_ambigous_word(sentence):
    """
    Find the ambiguous word with the pattern **word**
    :param sentence: the sentence
    :return: tuple (sentence, ambiguous word)
    """
    ambiguous_match = "\*\*(.+?)\*\*"
    ambiguous = re.search(ambiguous_match, sentence)
    if ambiguous:
        sentence = sentence.replace(ambiguous.group(0), ambiguous.group(1))
        return sentence, ambiguous.group(1)
    else:
        return sentence, None


sentences = read_file_lines("./data/sentences.txt")
for s in sentences:
    s = s.replace("\n", "")
    s, word_amb = find_ambigous_word(s)
    syn = lesk(s, word_amb)
    s_alternatives = generate_alternative_sentence(s, word_amb, syn)
    print("\nSentence: {}\nSyn: {}\nSyn Definition: {}\nAlternatives sentences:\n{}".
          format(s, syn, syn.definition(), "".join(s_alternatives)))
