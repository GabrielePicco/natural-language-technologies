import csv
import pandas as pd
import re
import string
import functools
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from itertools import product
from utility import timeit


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
    def summarize_document(self, file_path):
        self.cached_cohesion = {}
        df_document = self.__preprocess_text(file_path)
        df_document = self.__compute_cohesion(df_document)
        return df_document.sort_values(by="Cohesion", ascending=False)

    def __preprocess_text(self, file_path):
        with open(file_path) as f:
            text = f.read()
        text = re.sub("#(.*)\n", "", text).strip()  # remove comments
        text_records = [[p_text, p, self.__tokenize(p_text), 0] for (p, p_text) in enumerate(text.split("\n\n"))]
        return pd.DataFrame.from_records(text_records, columns=['Sentence', 'Paragraph', 'Token', 'Cohesion'],
                                         index='Paragraph')

    def __tokenize(self, p_text):
        p_text = p_text.translate(str.maketrans('', '', string.punctuation))
        lemmatizer = WordNetLemmatizer()
        splitted_text = map(lemmatizer.lemmatize, p_text.lower().split())
        splitted_text = [word for word in splitted_text if word not in stopwords.words("english")]
        return {i: splitted_text.count(i) for i in set(splitted_text)}

    def __compute_cohesion(self, df_document):
        for p, row in df_document.iterrows():
            cohesion = 0
            for p_i, row_i in df_document[df_document.index != p].iterrows():
                cohesion += self.__compute_paragraph_cohesion((p, row['Token']), (p_i, row_i['Token']))
            df_document.at[p, 'Cohesion'] = cohesion
        return df_document

    def __compute_paragraph_cohesion(self, paragraph1, paragraph2):
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
        ns1 = self.__get_nasari(w1)
        ns2 = self.__get_nasari(w2)
        if ns1 == [] or ns2 == []:
            return 0
        return max([self.__word_overlapse(*ns) for ns in product(ns1, ns2)])

    def __get_nasari(self, w):
        return list(self.nasari[self.nasari['Lemma'] == w]['Features'])

    @staticmethod
    @functools.lru_cache(maxsize=1024)
    def __word_overlapse(v1, v2):
        if v1 is None or v2 is None:
            return 0
        common_words = set(v1.keys()).intersection(set(v2.keys()))
        wo = 0
        for word in common_words:
            wo += float(v1[word]) + float(v2[word])
        return wo


summarizer = Summarizer(nasari_file_path="./data/nasari_small.txt")
print(summarizer.summarize_document(
    "./data/sample/Donald-Trump-vs-Barack-Obama-on-Nuclear-Weapons-in-East-Asia.txt").head())
