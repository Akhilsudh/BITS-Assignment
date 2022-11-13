import re
import string
import math
import nltk
import numpy as np
import pandas as pd

from nltk import tokenize
from nltk.corpus import stopwords
from operator import itemgetter
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

class tfidf():

    def __init__(self):
        pass

    def computeTF(self, wordDict, bow):
        tfDict = {}
        bowCount = len(bow)
        for word, count in wordDict.items():
            tfDict[word] = count/float(bowCount)
        return tfDict


    def computeIDF(self, docList):
        idfDict = {}
        N = len(docList)
        idfDict = dict.fromkeys(docList[0].keys(), 0)
        for doc in docList:
            for word, val in doc.items():
                if val > 0:
                    if word not in idfDict:
                        idfDict[word] = 0
                    idfDict[word] += 1
        for word, val in idfDict.items():
            idfDict[word] = math.log10(N / float(val))
        return idfDict


    def computeTFIDF(self, tfBow, idfs):
        tfidf = {}
        for word, val in tfBow.items():
            tfidf[word] = val*idfs[word]
        return tfidf

    def preprocess(self, df):
        df["text_wo_punct"] = df["text"].apply(lambda text: self.removePunctuation(text))
        df["text_lower"] = df["text_wo_punct"].str.lower()
        df["text_no_number"] = df["text_lower"].apply(lambda text: self.removeNumbers(text))
        df["text_wo_stop"] = df["text_no_number"].apply(lambda text: self.removeStopwords(text))
        return df["text_wo_stop"]

    def removeNumbers(self, text):
        return re.sub(r'\s*\d+\s*\w*', '', text)

    def removePunctuation(self, text):
        punctuationfree="".join([i for i in text if i not in string.punctuation])
        return punctuationfree

    def removeStopwords(self, text):
        STOPWORDS = ", ".join(stopwords.words('english'))
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])

    def getTopN(self, dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result

    def extractKeywords(self, eduDetails: str, expDetails: str, skillDetails: str, topN: int):
        df = pd.DataFrame([eduDetails, expDetails, skillDetails], columns=['text'])
        preprocess_df=self.preprocess(df)
        bowEdu = tokenize.word_tokenize(preprocess_df.iloc[[0]].item())
        bowExp = tokenize.word_tokenize(preprocess_df.iloc[[1]].item())
        bowSki = tokenize.word_tokenize(preprocess_df.iloc[[2]].item())
        wordset=set(bowEdu).union(set(bowExp)).union(set(bowSki))
        wordDictEdu = dict.fromkeys(wordset, 0)
        wordDictExp = dict.fromkeys(wordset, 0)
        wordDictSki = dict.fromkeys(wordset, 0)
        for word in bowEdu:
            wordDictEdu[word] += 1
        for word in bowExp:
            wordDictExp[word] += 1
        for word in bowSki:
            wordDictSki[word] += 1
        tfBowEdu = self.computeTF(wordDictEdu, bowEdu)
        tfBowExp = self.computeTF(wordDictExp, bowExp)
        tfBowSki = self.computeTF(wordDictSki, bowSki)
        idfs = self.computeIDF([wordDictEdu, wordDictExp, wordDictSki])
        tfidfBowEdu = self.computeTFIDF(tfBowEdu, idfs)
        tfidfBowExp = self.computeTFIDF(tfBowExp, idfs)
        tfidfBowSki = self.computeTFIDF(tfBowSki, idfs)
        df=pd.DataFrame([tfidfBowEdu, tfidfBowExp,tfidfBowSki])
        print(df)
        tf_idf={}
        for word in wordset:
            maxClm = df[word].max()
            tf_idf[word]=maxClm
        return list(self.getTopN(tf_idf, topN).keys())

    def skLearnTest(self, eduDetails: str, expDetails: str, skillDetails: str, topN: int):
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([eduDetails, expDetails, skillDetails])
        feature_names = vectorizer.get_feature_names()
        feature_array = np.array(feature_names)
        tfidf_sorting = np.argsort(vectors.toarray()).flatten()[::-1]
        return feature_array[tfidf_sorting][:topN]

if __name__ == "__main__":
    obj = tfidf()
    print(obj.extractKeywords(
            "mtech in BITS  PILANI since 2021 in data analytics",
            "working in citibank  trading project since 2023",
            "java , python , angular since",
            12
        ))