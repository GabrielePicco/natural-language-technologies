import csv
from enum import Enum

import pandas as pd
import re
import string
import functools
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from itertools import product
from utility import timeit


class Granularity(Enum):
    PARAGRAPH = 0,
    SENTENCE = 1


class Summarizer:

    def __init__(self, nasari_file_path):
        self.nasari = self.__read_nasari(nasari_file_path)
        self.cached_cohesion = {}

    @staticmethod
    def __gen_nasari_formatted_rows(stream):
        """
        Generator for reading the nasari file
        :param stream: the file stream
        :return: [BalbelSyn,Lemma,Features
        """
        rows = csv.reader(stream)
        for row in rows:
            row = row[0].split(";")
            yield [row[0], row[1].lower(),
                   dict((lambda fs: (fs[0], float(fs[1]) if len(fs) > 1 else 0))(lx.split("_")) for lx in row[2:])]

    def __read_nasari(self, file_path):
        """
        Read the nasari file as a Dataframe
        :param file_path:
        :return: dataframe, each row is (BalbelSyn, Lemma, Dict of Features)
        """
        with open(file_path) as f:
            nasari_df = pd.DataFrame.from_records(list(self.__gen_nasari_formatted_rows(f)),
                                                  columns=['BalbelSyn', 'Lemma', 'Features'], index='BalbelSyn')
        return nasari_df

    @timeit
    def summarize_document(self, file_path, percentage=0.7, granularity=Granularity.PARAGRAPH):
        """
        Summarized a given document, the paragraph or sentences are ranked based on the cohesion metrics.
        Cohesion is calculated using the nasari vectors similarity of the words.
        :param file_path: the path of the file to be summarized
        :param percentage: the percentage of relevant information to keep
        :param granularity: the granularity of the analysis (paragraph or sentence)
        :return: a string containing the summary of the document
        """
        self.cached_cohesion = {}
        df_document = self.__preprocess_text(file_path, granularity)
        df_document = self.__compute_cohesion(df_document)
        df_document = df_document.sort_values(by="Cohesion", ascending=False)
        summarized_document = df_document[0:int(len(df_document) * percentage)].sort_values(by="Paragraph")
        if granularity == Granularity.PARAGRAPH:
            return "\n\n".join(list(summarized_document['Sentence']))
        else:
            sum_sentences = list(summarized_document['Sentence'])
            return "{}\n\n".format(sum_sentences[0]) + "\n".join(sum_sentences[1:])

    def __preprocess_text(self, file_path, granularity):
        """
        Transform the document in a dataframe
        :type granularity: the text granularity level (Paragraph or sentence)
        :param file_path: the document filepath
        :return: a dataframe, with row ('Sentence', 'Paragraph', 'Token', 'Cohesion')
        """
        with open(file_path) as f:
            text = f.read()
        text = re.sub("#(.*)\n", "", text).strip()  # remove comments
        if granularity == Granularity.SENTENCE:
            text_sentences = sent_tokenize(text)
            text_sentences = [item for r in text_sentences for item in r.split('\n\n')]
            text_records = [[p_text, p, self.__tokenize(p_text), 0] for (p, p_text) in enumerate(text_sentences)]
        else:
            text_records = [[p_text, p, self.__tokenize(p_text), 0] for (p, p_text) in enumerate(text.split("\n\n"))]
        return pd.DataFrame.from_records(text_records, columns=['Sentence', 'Paragraph', 'Token', 'Cohesion'],
                                         index='Paragraph')

    def __tokenize(self, p_text):
        """
        Trasform a paragraph in a dictionary of word, freq.
        Punctuation and stopwords are removed, and the words are lemmatized
        :param p_text: text of the paragraph
        :return: dict{word: freq}
        """
        p_text = p_text.translate(str.maketrans('', '', string.punctuation))
        lemmatizer = WordNetLemmatizer()
        splitted_text = map(lemmatizer.lemmatize, p_text.lower().split())
        splitted_text = [word for word in splitted_text if word not in stopwords.words("english")]
        return {i: splitted_text.count(i) for i in set(splitted_text)}

    def __compute_cohesion(self, df_document):
        """
        Compute the cohesion between all paragraph
        :param df_document: the document dataframe
        :return: the document dataframe with the cohesion column attribute computed
        """
        for p, row in df_document.iterrows():
            cohesion = 0
            for p_i, row_i in df_document[df_document.index != p].iterrows():
                chs = self.__compute_paragraph_cohesion((p, row['Token']), (p_i, row_i['Token']))
                cohesion += chs if p_i != 0 else p_i * 1.5  # weight more cohesion with the title
            df_document.at[p, 'Cohesion'] = cohesion if p != 0 else cohesion * 1.5
        return df_document

    def __compute_paragraph_cohesion(self, paragraph1, paragraph2):
        """
        Compute the cohesion of two paragraph as the similarity between all words combinations
        :param paragraph1: tuple (paragraph number, dict{word: freq})
        :param paragraph2: tuple (paragraph number, dict{word: freq})
        :return: the paragraph cohesion
        """
        p1, par1 = paragraph1
        p2, par2 = paragraph2
        key = "{};{}".format(p1, p2) if p1 < p2 else "{};{}".format(p2, p1)
        if key in self.cached_cohesion.keys():
            return self.cached_cohesion[key]
        cohesion = 0
        for w1 in par1.keys():
            for w2 in par2.keys():
                cohesion += self.__similarity(w1, w2) * par1[w1] * par2[w2]
        self.cached_cohesion[key] = cohesion
        return cohesion

    @functools.lru_cache(maxsize=1024)
    def __similarity(self, w1, w2):
        """
        Compute the similarity given two word as the max word overlapse of all nasari vectors corresponding to the
        words
        :param w1: word1
        :param w2: word2
        :return: the similarity score
        """
        ns1 = self.__get_nasari(w1)
        ns2 = self.__get_nasari(w2)
        if ns1 == [] or ns2 == []:
            return 0
        return max([self.__word_overlapse(*ns) for ns in product(ns1, ns2)])

    def __get_nasari(self, w):
        """
        Return the corresponding Nasari vectors given a word
        :param w: word
        :return: list of nasari vector
        """
        return list(self.nasari[self.nasari['Lemma'] == w]['Features'])

    @staticmethod
    def __word_overlapse(v1, v2):
        """
        Compute the overlapse between two nasari vector
        :param v1:
        :param v2:
        :return:
        """
        if v1 is None or v2 is None:
            return 0
        common_words = set(v1.keys()).intersection(set(v2.keys()))
        wo = 0
        for word in common_words:
            wo += float(v1[word]) + float(v2[word])
        return wo
