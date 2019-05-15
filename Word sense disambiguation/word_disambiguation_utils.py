from nltk.corpus import wordnet
import inflect
import string
inflect = inflect.engine()


def remove_punctuation(sentence):
    return sentence.translate(str.maketrans('', '', string.punctuation))


def lesk(sentence, ambiguous_word):
    """
    Given a sentence (the context) and an ambiguous word, the most probable sense,
    computed with the simple version of the Lesk algorithm is returned
    :param sentence: the context sentence
    :param ambiguous_word: word
    :return: Most probable synset for the ambiguos word
    """
    if ambiguous_word is None:
        print(sentence)
        return None
    target_synsets = wordnet.synsets(ambiguous_word)
    if target_synsets is None:
        return None
    sentence = remove_punctuation(sentence).lower()
    context = set(sentence.split())
    intersection_c, sense = max([(len(context.intersection(remove_punctuation(syn.definition()).split())), syn)
                                 for syn in target_synsets])
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
