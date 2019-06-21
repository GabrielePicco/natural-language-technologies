from nltk import WordNetLemmatizer
from nltk.corpus import wordnet as wn

wnl = WordNetLemmatizer()


def lemmatize_word(word, pos):
    """
    Lemmatize a word
    :param word: the input word
    :param pos: the PeenTreebank POS tag
    :return: the lemmatized word
    """
    pos = get_wordnet_pos(pos)
    if pos is not None:
        return wnl.lemmatize(word, pos)
    else:
        return wnl.lemmatize(word)


def get_wordnet_pos(treebank_tag):
    """
    Convert a POS treebank in a wordnet POS
    :param treebank_tag: The POS
    :return: the wordnet POS
    """
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None
