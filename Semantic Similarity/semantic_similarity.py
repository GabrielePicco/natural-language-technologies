import csv
import itertools
import re
import statistics
import math
import pandas as pd
import requests
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr

BABELNET_KEY = "ffe50bfb-5dbc-4fe5-8120-45dced25d694"


def print_human_correlation(user_1_val, user_2_val):
    """
    Print the mean value of the two manual annotation and the correlation between them
    :param user_1_val: first user annotation values list
    :param user_2_val: second user annotation values list
    :return: -
    """
    print("First user mean: ", statistics.mean(user_1_val))
    print("Second user mean: ", statistics.mean(user_2_val))
    print("Pearson correlation: ", pearsonr(user_1_val, user_2_val))
    print(spearmanr(user_1_val, user_2_val))


def gen_nasari_formatted_rows(stream):
    """
    Generator for reading the nasari file
    :param stream: the file stream
    :return: [BabelSyn,Lemma,Features
    """
    rows = csv.reader(stream)
    for row in rows:
        row = row[0].split("__")
        vect = row[1].split("\t")
        lemma = vect.pop(0)
        yield [row[0], lemma, vect]


def read_nasari(file_path):
    """
    Read the nasari file as a Dataframe
    :param file_path:
    :return: dataframe, each row is (BabelSyn, Lemma, Dict of Features)
    """
    with open(file_path, encoding="utf8") as f:
        nasari_df = pd.DataFrame.from_records(list(gen_nasari_formatted_rows(f)),
                                              columns=['BabelSyn', 'Lemma', 'Features'])
    return nasari_df


def read_semeval(file_path):
    """
    Read the semeval file and store it in a dictionary
    :param file_path: path of the file
    :return: dictionary containing(Word, list of babelsynsetID)
    """
    with open(file_path, encoding="utf8") as file:
        rows = file.read().split("#")
        rows = [(lambda x: (x[0], x[1:]) if len(x) >= 2 else None)(re.compile(r"\n+").split(r.strip())) for r in rows]
        rows = [r for r in rows if r is not None]
        return dict(rows)


def get_nasari(nasari_df, babel_syn_id):
    """
    Return the corresponding Nasari vectors given a BabelSynset Id
    :param nasari_df: nasari vector in dataframe form
    :param babel_syn_id: BabelSynset Id
    :return: list of nasari vector
    """
    index = nasari_df[nasari_df['BabelSyn'] == babel_syn_id].first_valid_index()
    if index is not None:
        return list(nasari_df.iloc[index]['Features'])


def cosine_similarity(nv1, nv2):
    """
    compute the cosine similarity between two nasari vector embedded
    :param nv1: first nasari vector
    :param nv2: second nasari vector
    :return: number representing the cosine similarity
    """
    v1 = [float(i) for i in nv1]
    v2 = [float(i) for i in nv2]
    return (sum([v1[i] * v2[i] for i in range(len(v1))])) / (
            (math.sqrt(sum(math.pow(v1[i], 2) for i in range(len(v1))))) * (
        math.sqrt(sum(math.pow(v2[i], 2) for i in range(len(v2))))))


def max_cosine_similarity(nasari_df, w1_senses, w2_senses):
    """
    compute the maximum cosine similarity for each sense of a term
    :param w1_senses: list of babelsynsetID
    :param w2_senses: list of babelsynsetID
    :return: tuple containing the two senses that maximize the cosine similarity
    """
    max_cs = -1
    current_cs = -1
    max_senses = ()
    if w1_senses is not None and w2_senses is not None:
        for s1 in w1_senses:
            nasari_vect_1 = get_nasari(nasari_df, s1)
            if nasari_vect_1 != [] and nasari_vect_1 is not None:
                for s2 in w2_senses:
                    nasari_vect_2 = get_nasari(nasari_df, s2)
                    if nasari_vect_2 != [] and nasari_vect_2 is not None:
                        current_cs = cosine_similarity(nasari_vect_1, nasari_vect_2)
                        if current_cs > max_cs:
                            max_cs = current_cs
                            max_senses = (s1, s2)
    return max_senses


def get_babelnet_gloss(babel_synset_id):
    """
    Given a babelsynsetID query babelnet to get the gloss
    :param babel_synset_id: id whose gloss is to be found
    :return: a string containing the gloss
    """
    URL = "https://babelnet.io/v5/getSynset?id={}&key={}".format(babel_synset_id, BABELNET_KEY)
    babel_synset = requests.get(url=URL)
    data = babel_synset.json()
    if len(data['glosses']) > 0:
        return data['glosses'][0]['gloss']
    else:
        return ""


def calculate_accuracy(file_path):
    """
    Compute the accuracy of the of the intended meaning between
     human and the senses that maximize the cosine similarity
    :param file_path: path of the file
    :return: number representing the accuracy
    """
    acc_eval = []
    sum = 0
    with open(file_path) as file:
        for line in file:
            acc_eval.append(line[0])
    return acc_eval.count("1") / len(acc_eval)


def get_best_sense_glosses(dataset_df, nasari_df, semeval_dict):
    """
    get the senses that maximize the cosine similarity and stores them into a list
    :param dataset_df: dataframe containing the dataset from where get the terms
    :param nasari_df: dataframe containing all the nasari embedded vectors
    :param semeval_dict: dictionary contaninig (Word, babelsynsetId) from semeval 2017
    :return: number representing the accuracy
    """
    user_1_val, user_2_val, glosses = [], [], []
    for index, row in dataset_df.iterrows():
        user_1_val.append(row['Val1'])
        user_2_val.append(row['Val2'])
        w1 = row['Word1']
        w2 = row['Word2']
        w1_senses = semeval_dict.get(w1)
        w2_senses = semeval_dict.get(w2)
        argmax_senses = max_cosine_similarity(nasari_df, w1_senses, w2_senses)
        if argmax_senses != ():
            glosses.append([w1, get_babelnet_gloss(argmax_senses[0])])
            glosses.append([w2, get_babelnet_gloss(argmax_senses[1])])
    return glosses


def write_glosses_to_file(glosses):
    """
    Write a term and its relative gloss to an output file
    :param glosses: list of tuples cointainig a term and its relative best gloss
    :return: -
    """
    with open("results/Output_EN.txt", "w", encoding="utf8") as text_file:
        for word, gloss in glosses:
            print("Termine: {}; Glossa: {}".format(word, gloss), file=text_file)


nasari_df = read_nasari("data/mini_NASARI.tsv")
semeval_dict = read_semeval("data/SemEval17_IT.txt")
dataset_df = pd.read_csv('data/data_1.txt')
glosses = get_best_sense_glosses(dataset_df, nasari_df, semeval_dict)
write_glosses_to_file(glosses)

print("Accuracy singoli termini utente S {}".format(calculate_accuracy("results/Accuracy_termini_S.txt")))
print("Accuracy coppie utente S {}".format(calculate_accuracy("results/Accuracy_coppie_S.txt")))
print("Accuracy singoli termini utente G {}".format(calculate_accuracy("results/Accuracy_termini_G.txt")))
print("Accuracy coppie utente G {}".format(calculate_accuracy("results/Accuracy_coppie_G.txt")))
