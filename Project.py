# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

cd Meta/MetaData/

# <codecell>

import pandas as pd
import numpy as np
import datetime
import nltk 
from nltk.book import *
from __future__ import division
import re, pprint

# <codecell>

name = pd.read_table("Name", sep = ",", header = None)
name.head()
name[0][2076:2077]

# <codecell>

#test = name[0][411:412] + 'Clean' + '.csv'
#print test
#data = pd.read_table("promosClean.csv", sep = "\t")
#data.head()
#pd.read_table("GiffingToolClean.csv", sep = "\t").head()
#virgin = pd.read_table("VirginiaClean.csv", sep = "\t")

# <codecell>

pd.set_option('display.mpl_style', 'default')
Time_count = pd.DataFrame({'Time': range(24)})
Time_karma = pd.DataFrame({'Time': range(24)})
Time_care = pd.DataFrame({'Time': range(24)})
def f(x):
    x = datetime.datetime.fromtimestamp(x).strftime('%H')
    return int(x)
for i in name[0][0:2500]:
    original = i
    index = i + 'Clean' + '.csv'
    a = pd.read_table(index, sep = "\t")
    a['care_value'] = a['ups'] + a['downs']
    a['karma'] = a['ups'] - a['downs']
    try: 
        a['created_utc'] = a['created_utc'].apply(f)
        Time_count[original] = a['created_utc'].value_counts()
        temp_karma = pd.DataFrame({'Time': a['created_utc'],'karma': a['karma']})
        temp_care = pd.DataFrame({'Time': a['created_utc'],'care_value': a['care_value']})
        Time_karma[original] = temp_karma.groupby('Time', as_index = False).mean()['karma']
        Time_care[original] = temp_care.groupby('Time', as_index = False).max()['care_value']
    except: continue
Time_karma.drop('Time', axis = 1)
Time_care.drop('Time', axis = 1)

# <codecell>


# <codecell>

pd.set_option('display.mpl_style', 'default')
Time_count = pd.DataFrame({'Time': range(24)})
Time_karma = pd.DataFrame({'Time': range(24)})
Time_care = pd.DataFrame({'Time': range(24)})
def f(x):
    x = datetime.datetime.fromtimestamp(x).strftime('%d')
    return int(x)
for i in name[0][0:2500]:
    original = i
    index = i + 'Clean' + '.csv'
    a = pd.read_table(index, sep = "\t")
    a['care_value'] = a['ups'] + a['downs']
    a['karma'] = a['ups'] - a['downs']
    try: 
        a['created_utc'] = a['created_utc'].apply(f)
        Time_count[original] = a['created_utc'].value_counts()
        temp_karma = pd.DataFrame({'Time': a['created_utc'],'karma': a['karma']})
        temp_care = pd.DataFrame({'Time': a['created_utc'],'care_value': a['care_value']})
        Time_karma[original] = temp_karma.groupby('Time', as_index = False).mean()['karma']
        Time_care[original] = temp_care.groupby('Time', as_index = False).max()['care_value']
    except: continue
Time_karma.drop('Time', axis = 1)
Time_care.drop('Time', axis = 1)

# <codecell>

Date_count = pd.DataFrame({'Time': range(7)})
def g(x):
    x = datetime.datetime.fromtimestamp(x).strftime('%w')
    return int(x)
for i in name[0][0:2500]:
    original = i
    index = i + 'Clean' + '.csv'
    a = pd.read_table(index, sep = "\t")
    try: 
        a['created_utc'] = a['created_utc'].apply(g)
        Date_count[original] = a['created_utc'].value_counts()
    except: continue
Date_count.T.sum()

# <codecell>

fig = plt.figure()
axes = fig.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Date_count.T.sum(), 'b')
#plt.plot(Time_care.T.max(), 'r')
#plt.plot(Time_care.T.median(), 'r')
#plt.plot(Time_care.T.min(), 'b')
plt.plot()
axes.set_xlabel('Days')
Time = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
axes.set_xticks(range(7))
axes.set_ylabel('Counts')
axes.set_title('Comparison Among Different Week Days')
plt.savefig('weekday_counts.jpeg')

# <codecell>

%matplotlib inline
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
axes = fig.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_care.T.max(), 'b')
#plt.plot(Time_care.T.hist(), 'r')
#plt.plot(Time_care.T.median(), 'r')
#plt.plot(Time_care.T.min(), 'b')
plt.plot()
axes.set_xlabel('Time')
axes.set_xticks(range(24))
axes.set_ylabel('Care Value')
axes.set_title('Comparison Among Different Care Values')
plt.savefig('Care_value.jpeg')

# <codecell>

fig2 = plt.figure()
axes = fig2.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_care.T.median(), 'b')
#plt.plot(Time_care.T.hist(), 'r')
#plt.plot(Time_care.T.median(), 'r')
#plt.plot(Time_care.T.min(), 'b')
axes.set_xlabel('Time')
axes.set_xticks(range(24))
axes.set_ylabel('Care Value Median')
axes.set_title('Comparison Among Different Care Values')
#for i in Time_care.T.median():
#   axes.annotate()
# plt.savefig('cnm.jpeg')

# <codecell>

fig1 = plt.figure()
axes = fig1.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_karma.T.max(), 'r')
axes.set_xticks(range(24))
axes.set_xlabel('Time')
axes.set_ylabel('Karma')
axes.set_title('Comparison of Different Karma Values')
plt.savefig('karma.jpeg')

# <codecell>

fig3 = plt.figure()
axes = fig3.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_karma.T.median(), 'r')
axes.set_xticks(range(24))
axes.set_xlabel('Time')
axes.set_ylabel('Karma')
axes.set_title('Comparison of Different Karma Values')
# plt.savefig('')
# Time_care.T.median().plot(kind = 'line')
# print Time_care.T.max()
# print Time_care.T.min()
#plt.scatter(range(2498), Time_care.loc[0][1:])
# plt.scatter(range(2498), Time_care.loc[23][1:])
#plt.scatter(range(2498), Time_care.loc[2][1:])
#plt.scatter(range(2498), Time_care.loc[10][1:])

# <codecell>

fig_count = plt.gcf()
axes = fig_count.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_count.T.sum(), 'b')
plt.plot(Time_care.T.max(), 'r')
#plt.plot(Time_care.T.median(), 'r')
#plt.plot(Time_care.T.min(), 'b')
plt.plot()
axes.set_xlabel('Time')
axes.set_xticks(range(24))
axes.set_ylabel('Number of Posts ')
axes.set_title('Post Counts Over Time & Maximum Care')
plt.legend(('post_count','care_value'))
plt.savefig('/Users/MrG/Capstone/Meta/count.png')

# <codecell>

# Text Mining !
# Extract the title and content data that are most popular and least popular
Top_Title = []
Top_Content = []
Bottom_Title = []
Bottom_Content = []
def f(x):
    x = datetime.datetime.fromtimestamp(x).strftime('%H')
    return int(x)
for i in name[0][0:2500]:
    try:
        original = i
        index = i + 'Clean' + '.csv'
        a = pd.read_table(index, sep = "\t")
        a['care_value'] = a['ups'] + a['downs'] 
        a['care_value']
        Top_Title.append(a['title'][a['care_value'].argmax()])
        Top_Content.append(a['selftext'][a['care_value'].argmax()])
        Bottom_Title.append(a['title'][a['care_value'].argmin()])
        Bottom_Content.append(a['selftext'][a['care_value'].argmin()])
    except:continue

# <codecell>

import nltk
import nltk.data
from nltk.corpus import stopwords
stop = stopwords.words('english')
stop = stop + ['nan','http','www','xe','com','The','the','WWW','When','Where']
Important_word = []
title_token = nltk.regexp_tokenize(str(Bottom_Title), pattern = '\w+|[^\w\s]+|')
for i in title_token:
   if i not in stop:
       Important_word.append(i)
Important_word = str(Important_word)
content_text = nltk.Text(str(Top_Content[0:2498]))
word_pool = re.findall(r'\w{2,}', Important_word)
# tagged = nltk.pos_tag(word_pool)
# nltk.tag.str2tuple(Important_word, sep = '|')
#a = nltk.FreqDist(word_pool)
len(word_pool)

# <codecell>


# <codecell>

# Tag words

tagged=[]
for i in range(2):
    num = i*10000
    end = num+10000
    if i==1:
        words = nltk.pos_tag(word_pool[num:])
        tagged +=words
    else:
        print num, end
        words = nltk.pos_tag(word_pool[num:end])
        tagged +=words
len(tagged)

# <codecell>

# Write out word_pool so that we can read it again
import csv
outTag =open("word_pool2.csv",'w')
wr = csv.writer(outTag, lineterminator='\n')
for item in tagged:
    out = item[0]+'\t'+item[1]
    wr.writerow([out])

# <codecell>

Bottom_title_tag = pd.read_table('word_pool2.csv', header=False)
Bottom_title_tag.columns=['word','tag']
Bottom_title_tag

# <codecell>

# The output program 
noun_list = Bottom_title_tag.loc[Bottom_title_tag['tag'] == ('NNP' or 'NNPS'), 'word'].tolist()
noun = nltk.FreqDist(noun_list)
noun.items()
outNoun =open("noun.csv",'w')
wr = csv.writer(outNoun, lineterminator='\n')
for item in noun.items():
    out = str(item[0]) + '\t' + str(item[1])
    wr.writerow([out])

# <codecell>

verb_list = Top_Content_tag.loc[Top_Content_tag['tag'] == 'VB', 'word'].tolist()
verb = nltk.FreqDist(verb_list)
verb.items()
outverb =open("verb.csv",'w')
wr = csv.writer(outverb, lineterminator='\n')
for item in verb.items():
    out = item[0]+'\t'+str(item[1])
    wr.writerow([out])

# <codecell>


# <codecell>

text4.dispersion_plot(["citizens","democracy","policy","American","China"])
type (text4)
len(text1)
content_text = str(Top_Content)
content_text = nltk.Text(content_text)
content_text.dispersion_plot(["reddit","something"])

# <codecell>

Title_token = nltk.wordpunct_tokenize(str(Top_Title[0:2498]))
Title_key = []
for i in Title_token:
    if i not in stop:
        Title_key.append(i)
Title_key = str(Title_key)
Title_key = re.findall(r'[A-Z]*[a-z]{5,}', Title_key)
tagged_1 = nltk.pos_tag(Title_key[:1000])
Title_key_dist = nltk.FreqDist(Title_key)

# <codecell>

Title_key_dist.plot(30)

# <codecell>


# <codecell>

# Clustering and Further Analysis
from sklearn.decomposition import PCA
#pca = PCA(n_components=2)
# np.array(Time_count.columns())
# Time_score = Time_score.drop('Time_Interval', axis = 1)
#pca.fit(np.array(Time_.T))
#print pca.explained_variance_ratio_
#print pca.components_[0]
#print pca.components_[1]
# print pca.transform
#plt.scatter(pca.components_[0], pca.components_[1])

# <codecell>

# Bottom_Content_tag['tag'] == ('NN' or 'NNP' or 'NNPS' or 'NNS')

# <codecell>


# <codecell>

quit()

# <codecell>


