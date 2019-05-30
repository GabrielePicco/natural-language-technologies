import csv
import itertools
import math
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import wordnet as wn
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import minmax_scale


def depth(sense):
    """
    Compute a synset depth
    :param sense: synset for calculate depth
    :return: integere representing the depth of the synset
    """
    if (sense is not None):
        ancestor = sense.hypernyms()
        if len(ancestor) > 0:
            return 1 + depth(ancestor[0])
    return 0


def lcs_path(sense_1, sense_2, path):
    """
    Compute the least common subsumer of two synset and their shortest path
    :param sense_1: first synset
    :param sense_2: second synset
    :param path: path between the two synset
    :return: (least common subsumer (synset), path between senses (integer))
    """
    s1_depth = depth(sense_1)
    s2_depth = depth(sense_2)
    if (s1_depth == s2_depth):
        return lcs_path_same_depth(sense_1, sense_2, path)
    elif (s1_depth < s2_depth):
        ancestor_2 = sense_2.hypernyms()
        if len(ancestor_2) > 0:
            return lcs_path(sense_1, ancestor_2[0], path + 1)
    else:
        ancestor_1 = sense_1.hypernyms()
        if len(ancestor_1) > 0:
            return lcs_path(ancestor_1[0], sense_2, path + 1)


def lcs_path_same_depth(sense_1, sense_2, path):
    """
    Helper function to compute the least common subsumer
    of two synset at the same depth and their shortest path
    :param sense_1: first synset
    :param sense_2: second synset
    :param path: path between the two synset
    :return: (least common subsumer (synset), path between senses (integer))
    """
    ancestor_1 = sense_1.hypernyms()
    ancestor_2 = sense_2.hypernyms()
    if (len(ancestor_1) > 0 and len(ancestor_2) > 0):
        if (ancestor_1[0] == ancestor_2[0]):
            return ancestor_1[0], path + 2
        else:
            return lcs_path_same_depth(ancestor_1[0], ancestor_2[0], path + 2)


def wu_palmer_similarity(sense_1, sense_2, lcs):
    """
    Compute the Wu Palmer similarity between two synsets
    :param sense_1: first synset
    :param sense_2: second synset
    :param lcs: the least common subsumer of the two synsets
    :return: number representing the similarity
    """
    return ((2 * depth(lcs)) / (depth(sense_1) + depth(sense_2)))


def shortest_path_similarity(sense_1, sense_2, senses_path, depth_max):
    """
    Compute the shortest path similarity between two synsets
    :param sense_1: first synset
    :param sense_2: second synset
    :param senses_path: the shortest path between two synsets
    :param depth_max: the max depth of the taxonomy
    :return: number representing the similarity
    """
    return (((2 * depth_max) - senses_path))


def lc_similarity(sense_1, sense_2, senses_path, depth_max):
    """
    Compute the Leacock Chodorow similarity between two synsets
    :param sense_1: first synset
    :param sense_2: second synset
    :param senses_path: the shortest path between two synsets
    :param depth_max: the max depth of the taxonomy
    :return: number representing the similarity
    """
    return (-(math.log2((((senses_path) + 1) / ((2 * depth_max) + 1)))))


def get_all_synset_list(list):
    """
    Helper function to transform a list of words into a list of synsets
    :param list: the list to transform
    :return: a list of synset
    """
    syns_list = []
    for elem in list:
        syns_list.append(wn.synsets(elem[0]))
        syns_list.append(wn.synsets(elem[1]))
    return itertools.chain.from_iterable(syns_list)


def max_dataset_depth(df):
    """
    Compute the max depth of the dataset taxonomy in Wordnet
    :param df: a dataframe containing the dataset
    :return: number representing the max depth of the taxonomy
    """
    df_to_list = df.reset_index()[['Word 1', 'Word 2']].values.astype(str).tolist()
    all_synset_list = get_all_synset_list(list(itertools.chain.from_iterable(df_to_list)))
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in all_synset_list)


def print_correlations(human_similarity, wup_term_sim, shp_term_sim, lch_term_sim):
    """
    Compute a print Pearson and Spearman correlation between human annotation and
    Wu Palmer, Shortest Path and Leacock Chodorow similarity metrics
    :param human_similarity: list of human annotated similarity measures
    :param wup_term_sim: list of Wu Palmer computed metrics
    :param shp_term_sim: list of Shortest Path computed metrics
    :param lch_term_sim: list of Leacock Chodorow computed metrics
    :return:
    """
    print("Wup-Pearson-Correlation is {}".format(pearsonr(human_similarity, wup_term_sim)))
    print("Shp-Pearson-Correlation is {}".format(pearsonr(human_similarity, shp_term_sim)))
    print("Lch-Pearson-Correlation is {}".format(pearsonr(human_similarity, lch_term_sim)))
    print("Wup-Spearman-Correlation is {}".format(spearmanr(human_similarity, wup_term_sim)))
    print("Shp-Spearman-Correlation is {}".format(spearmanr(human_similarity, shp_term_sim)))
    print("Lch-Spearman-Correlation is {}".format(spearmanr(human_similarity, lch_term_sim)))


def write_similarity(df, wup_term_sim, shp_term_sim, lch_term_sim):
    """
    Write metrics results on a file
    :param df: dataframe containing the dataset
    :param wup_term_sim: list of Wu Palmer computed metrics between terms
    :param shp_term_sim: list of Shortest Path computed metrics between terms
    :param lch_term_sim: list of Leacock Chodorow computed metrics between terms
    :return:
    """
    df['Wu-Palmer-Similarity'] = wup_term_sim
    df['Shortest-Path-Similarity'] = shp_term_sim
    df['Leakock-Chodorow-Similarity'] = lch_term_sim
    df.to_csv("WordSim353.csv")


def compute_max_term_similarity(df):
    """
    Compute the similarity between all synset of two term and return
    the max one for each similarity
    :param df: dataframe containing the dataset
    :return: three lists containing the max similarity and the human similarity list
    """
    human_similarity, wup_term_sim, shp_term_sim, lch_term_sim = [], [], [], []
    # depth_max = 20  # Wordnet 3.0 depth
    depth_max = max_dataset_depth(df)  # dataset taxonomy depth
    for index, row in df.iterrows():
        s_1 = wn.synsets(row['Word 1'])
        s_2 = wn.synsets(row['Word 2'])
        human_similarity.append(float(row['Human']))
        max_wup_similarity = -1
        max_shp_similarity = -1
        max_lch_similarity = -1
        for synset_1 in s_1:
            for synset_2 in s_2:
                lcs_tuple = lcs_path(synset_1, synset_2, 0)
                if lcs_tuple is not None:
                    least_common_subsumer = lcs_tuple[0]
                    synsets_shortest_path = lcs_tuple[1]
                    wu_sim = wu_palmer_similarity(synset_1, synset_2, least_common_subsumer)
                    shp_sim = shortest_path_similarity(synset_1, synset_2, synsets_shortest_path, depth_max)
                    lch_sim = lc_similarity(synset_1, synset_2, synsets_shortest_path, depth_max)
                    if wu_sim is not None:
                        if wu_sim > max_wup_similarity:
                            max_wup_similarity = wu_sim
                    if shp_sim is not None:
                        if shp_sim > max_shp_similarity:
                            max_shp_similarity = shp_sim
                    if lch_sim is not None:
                        if lch_sim > max_lch_similarity:
                            max_lch_similarity = lch_sim
        wup_term_sim.append(max_wup_similarity)
        shp_term_sim.append(max_shp_similarity)
        lch_term_sim.append(max_lch_similarity)
    return human_similarity, wup_term_sim, shp_term_sim, lch_term_sim


def read_csv(file_path):
    """
    Read dataset and return a dataframe
    :param file_path: path of the file to read
    :return: dataframe containing the dataset
    """
    return pd.read_csv(file_path)


df = read_csv('WordSim353.csv')
human_similarity, wup_term_sim, shp_term_sim, lch_term_sim = compute_max_term_similarity(df)
# write_similarity(df,wup_term_sim,shp_term_sim,lch_term_sim)
print_correlations(human_similarity, wup_term_sim, shp_term_sim, lch_term_sim)
