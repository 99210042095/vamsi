# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZMsaUv-FNrTX38401cLdnbNRKFTv9pu9
"""

import numpy as np
import pandas as pd
import zipfile
import os
import plotly.express as px

from google.colab import drive
drive.mount('/content/drive')

!pip install selenium

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from bs4 import BeautifulSoup
import networkx as nx

import pickle

import warnings
import numpy as np


import seaborn as sns
import matplotlib.pyplot as plt


import plotly.express as px
import time

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from selenium import webdriver
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

phish_data = pd.read_csv('/content/archive (2).zip')

import os

# Check if the file exists
file_path = "/content/archive (2).zip"
if os.path.exists(file_path):
    print("File exists.")

    # Try to open the file as a zip archive
    try:
        import zipfile
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            print("File is a valid zip archive.")
    except zipfile.BadZipFile:
        print("File is not a valid zip archive.")
else:
    print("File does not exist. Check the file path.")

phish_data.head()

phish_data.tail()

phish_data.info()

phish_data.isnull().sum()

label_counts = pd.DataFrame(phish_data['Label'].value_counts())
# Rename the column from 0 to 'Label'

label_counts = label_counts.rename(columns={0: 'Label'})



tokenizer = RegexpTokenizer(r'[A-Za-z]+')#

phish_data.URL[0]

tokenizer.tokenize(phish_data.URL[0])

print('Getting words tokenized ...')
t0= time.perf_counter()
phish_data['text_tokenized'] = phish_data.URL.map(lambda t: tokenizer.tokenize(t)) # doing with all rows
t1 = time.perf_counter() - t0
print('Time taken',t1 ,'sec')

phish_data.sample(5)

stemmer = SnowballStemmer("english")

print('Getting words stemmed ...')
t0= time.perf_counter()
phish_data['text_stemmed'] = phish_data['text_tokenized'].map(lambda l: [stemmer.stem(word) for word in l])
t1= time.perf_counter() - t0
print('Time taken',t1 ,'sec')

phish_data.sample(5)

print('Getting joiningwords ...')
t0= time.perf_counter()
phish_data['text_sent'] = phish_data['text_stemmed'].map(lambda l: ' '.join(l))
t1= time.perf_counter() - t0
print('Time taken',t1 ,'sec')

phish_data.sample(5)

bad_sites = phish_data[phish_data.Label == 'bad']
good_sites = phish_data[phish_data.Label == 'good']

bad_sites.head()

good_sites.head()

def plot_wordcloud(text, mask=None, max_words=400, max_font_size=120, figure_size=(24.0,16.0),
                   title = None, title_size=40, image_color=False):
    stopwords = set(STOPWORDS)
    more_stopwords = {'com','http'}
    stopwords = stopwords.union(more_stopwords)

    wordcloud = WordCloud(background_color='white',
                    stopwords = stopwords,
                    max_words = max_words,
                    max_font_size = max_font_size,
                    random_state = 42,
                    mask = mask)
    wordcloud.generate(text)

    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,
                                  'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'green',
                                  'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()

d = '../input/masks/masks-wordclouds/'

data = good_sites.text_sent
data.reset_index(drop=True, inplace=True)



ata = bad_sites.text_sent
data.reset_index(drop=True, inplace=True)

help(CountVectorizer())

cv = CountVectorizer()

help(CountVectorizer())

feature = cv.fit_transform(phish_data.text_sent)

feature[:5].toarray()

trainX, testX, trainY, testY = train_test_split(feature, phish_data.Label)

lr = LogisticRegression()

lr.fit(trainX,trainY)

lr.score(testX,testY)

print('Training Accuracy :',lr.score(trainX,trainY))
print('Testing Accuracy :',lr.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(lr.predict(testX), testY),
            columns=['Predicted:Bad', 'Predicted:Good'],
            index=['Actual:Bad', 'Actual:Good'])

print('\nCLASSIFICATION REPORT\n')
print(classification_report(lr.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

mnb = MultinomialNB()

mnb.fit(trainX,trainY)

mnb.score(testX,testY)

Scores_ml = {}
Scores_ml['MultinomialNB'] = np.round(mnb.score(testX,testY),2)

print('Training Accuracy :',mnb.score(trainX,trainY))
print('Testing Accuracy :',mnb.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(mnb.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])


print('\nCLASSIFICATION REPORT\n')
print(classification_report(mnb.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

acc = pd.DataFrame.from_dict(Scores_ml,orient = 'index',columns=['Accuracy'])
sns.set_style('darkgrid')
sns.barplot(x=acc.index, y=acc.Accuracy)

pipeline_ls = make_pipeline(CountVectorizer(tokenizer = RegexpTokenizer(r'[A-Za-z]+').tokenize,stop_words='english'), LogisticRegression())

trainX, testX, trainY, testY = train_test_split(phish_data.URL, phish_data.Label)

pipeline_ls.fit(trainX,trainY)

pipeline_ls.score(testX,testY)

print('Training Accuracy :',pipeline_ls.score(trainX,trainY))
print('Testing Accuracy :',pipeline_ls.score(testX,testY))
con_mat = pd.DataFrame(confusion_matrix(pipeline_ls.predict(testX), testY),
            columns = ['Predicted:Bad', 'Predicted:Good'],
            index = ['Actual:Bad', 'Actual:Good'])


print('\nCLASSIFICATION REPORT\n')
print(classification_report(pipeline_ls.predict(testX), testY,
                            target_names =['Bad','Good']))

print('\nCONFUSION MATRIX')
plt.figure(figsize= (6,4))
sns.heatmap(con_mat, annot = True,fmt='d',cmap="YlGnBu")

pickle.dump(pipeline_ls,open('phishing.pkl','wb'))

loaded_model = pickle.load(open('phishing.pkl', 'rb'))
result = loaded_model.score(testX,testY)
print(result)

predict_bad = ['yeniik.com.tr/wp-admin/js/login.alibaba.com/login.jsp.php','youtube.com/watch?v=qI0TQJI3vdU','fazan-pacir.rs/temp/libraries/ipad','tubemoviez.exe','svision-online.de/mgfi/administrator/components/com_babackup/classes/fx29id1.txt']
predict_good = ['youtube.com/','youtube.com/watch?v=qI0TQJI3vdU','retailhellunderground.com/','restorevisioncenters.com/html/technology.html','tubemoviez.exe']
loaded_model = pickle.load(open('phishing.pkl', 'rb'))
result = loaded_model.predict(predict_bad)
result2 = loaded_model.predict(predict_good)
print(result)
print("*"*35)
print(result2)