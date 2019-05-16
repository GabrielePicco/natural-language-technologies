import string
import inflect
from nltk.corpus import wordnet

inflect = inflect.engine()


def normalize_sentence(sentence):
    """
    Normalize a sentence, removing punctuation and uppercase letters
    :param sentence: the input sentence
    :return: the normalized sentence
    """
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    sentence = sentence.lower()
    return sentence.split()


def get_synset_context(syn):
    """
    Givene a synset generate a context, extracting the definition, the examples and the gloss
    :param syn: the synset
    :return: set, the context
    """
    sentence_context = normalize_sentence(syn.definition() + " ".join(syn.examples()))
    return set(sentence_context) | set(syn.lemma_names())


def lesk(sentence, ambiguous_word):
    """
    Given a sentence (the context) and an ambiguous word, the most probable sense,
    computed with the simple version of the Lesk algorithm is returned
    :param sentence: the context sentence
    :param ambiguous_word: word
    :return: Most probable synset for the ambiguos word
    """
    target_synsets = wordnet.synsets(ambiguous_word)
    sentence = normalize_sentence(sentence)
    context = set(sentence)
    intersection_c, sense = max([(len(context.intersection(get_synset_context(syn))), syn) for syn in target_synsets])
    return sense


def generate_alternative_sentence(sentence, ambiguous_word, syn):
    """
    Generate alternative sentences given an ambiguous word and the relative synset id
    (set the plural accordingly to the ambiguous word)
    :param sentence: the input sentence
    :param ambiguous_word: the ambiguous word
    :param syn: the synset
    :return: a list of alternatives
    """
    is_word_capitalized = ambiguous_word == ambiguous_word.capitalize()
    ambiguous_word_n = ambiguous_word.lower()
    is_word_plural = inflect.singular_noun(ambiguous_word_n) is not False
    if is_word_plural:
        ambiguous_word_n = inflect.singular_noun(ambiguous_word_n)
    word_version = [ambiguous_word_n, ambiguous_word_n.capitalize(), inflect.plural(ambiguous_word_n),
                    inflect.plural(ambiguous_word_n).capitalize()]
    synonyms = set(syn.lemma_names()) - set(word_version)
    return [sentence.replace(ambiguous_word, inflect_word(lm, is_word_capitalized, is_word_plural)) for lm in synonyms]


def inflect_word(word, capitalize, plural):
    """
    Capitalize and set the word to plural
    :param word: the word
    :param capitalize: boolean
    :param plural: boolean
    :return: the word string
    """
    if capitalize:
        word = word.capitalize()
    if plural:
        word = inflect.plural(word)
    return word
