
# coding: utf-8

# # Preparation: Import the useful packages that I need

# In[1]:

cd ~/Capstone/Meta/MetaData/


# In[2]:

import pandas as pd
import numpy as np
import datetime
import nltk 
from nltk.book import *
from __future__ import division


# I have a file containing all of the Name information

# In[3]:

name = pd.read_table("Name", sep = ",", header = None)
name.head()


# Test: test function which would be used by nose package, and it is used to make sure all names have been imported properly

# In[4]:

def test_1():
    assert len(name[0])==2500


# #Data Cleaning:

# The data cleaning part includes two part of codes, the first part is the UNIX shell command used to download the data from website and preprocess the information so that they can be read into python to do further analysis. The second part is python code used to extract the useful information from the preprocessed data. As we all know, data cleaning is a process weaved in the whole analytic project, so this part does not necessarity include all the data cleaning efforts. 

# The following chunk is used to select out the useful information and store them in the dataframe we have created such as Time_count, Time_karma and Time_care. Basically, those are the dataframe containing the number of posts, karma values and care values(the number of uppost + the number of down downpost) over 24 hours.

# In[5]:

pd.set_option('display.mpl_style', 'default')
Time_count = pd.DataFrame({'Time': range(24)})
Time_karma = pd.DataFrame({'Time': range(24)})
Time_care = pd.DataFrame({'Time': range(24)})
def f(x):
    x = datetime.datetime.fromtimestamp(x).strftime('%H')
    return int(x)

for i in name[0][0:2500]:  #should it be 0 to 2499?????
    original = i
    index = i + 'Clean' + '.csv'
    a = pd.read_table(index, sep = "\t") #read in each subreddit CSV file
    a['care_value'] = a['ups'] + a['downs'] #calculate care value from adding up votes and down votes
    a['karma'] = a['ups'] - a['downs'] #calculate karma value using upvotes subtracting down votes
    try: 
        a['created_utc'] = a['created_utc'].apply(f) #convert epoch time to hours
        Time_count[original] = a['created_utc'].value_counts() # count how many posts are created wthin each hour??
        temp_karma = pd.DataFrame({'Time': a['created_utc'],'karma': a['karma']})
        #store hour and karma into a data frame
        temp_care = pd.DataFrame({'Time': a['created_utc'],'care_value': a['care_value']})
        #store hour and care value to a data frame
        Time_karma[original] = temp_karma.groupby('Time', as_index = False).mean()['karma']
        #group by hour, calculate the mean karma value within each hour
        Time_care[original] = temp_care.groupby('Time', as_index = False).max()['care_value']
        #group by hour, calculate the max care value within each hour
    except: continue
Time_karma.drop('Time', axis = 1)
Time_care.drop('Time', axis = 1)


# Test: test function which would be used by nose package to make sure our cleaned file is correct

# In[6]:

def test_2():
    assert len(Time_karma.columns)==2499
    assert Time_karma.shape==(24, 2499) 
    if all(Time_karma.Time <24) and all(Time_karma.Time >=0):
        assert True


# In[7]:

def test_3():
    assert len(Time_care.columns)==2499
    assert Time_care.shape==(24, 2499) 
    if all(Time_care.Time <24) and all(Time_care.Time >=0):
        assert True


# Test: The previous code works fairly well since the result is the same compared with the original data file "2007scapeClean.csv". Note: this is not run by nose

# In[8]:

Test = pd.read_table("2007scapeClean.csv")
# A sample of the cleaned data file
Test.head(10)


# # A sample of the data frame that we created 

# In[9]:

print Time_care['0x10c'].head(5)
print Time_karma['30ROCK'].head(5)
print Time_count['zelda'].head(5)


# # Data Extraction and Initial Plots 

# Date_count is the dataframe we used to count the number of posts over different weekdays over different subreddit, and we want use this information to figure out the active time of Reddit's users. To be specific, we want to know if they are more active on posting during weekdays or weekends.

# In[10]:

Date_count = pd.DataFrame({'Time': range(7)})
def g(x):
    x = datetime.datetime.fromtimestamp(x).strftime('%w') #extract week days
    return int(x)
for i in name[0][0:2500]:
    original = i
    index = i + 'Clean' + '.csv'
    a = pd.read_table(index, sep = "\t")
    try: 
        a['created_utc'] = a['created_utc'].apply(g)
        Date_count[original] = a['created_utc'].value_counts() 
        #count how many posts are created within each week day
    except: continue


# # Sample:

# In[11]:

print Date_count['0x10c']
print Date_count['backpacking']


# Test: test function which would be used by nose package to guarantee the data we extracted is correct

# In[12]:

def test_4():
    assert Date_count.shape==(7, 2501) 
    if all(Date_count.Time <7) and all(Date_count.Time  >=0):
        assert True


##### Plot: Users Active Hours(Unfinished)

# Based on the posting time 2.5 million posts which are posted before August 20 2013, we have created the plot of users' posting hours in the range of 0 to 23. For example, if there are 40000 posts between 1:00 to 2:00, then these posts are classified as the posts with a tag 1. As we can see from the plot, the users involvment in Reddit keeps increasing from 2:00 am to 10:00 am and reachs its peak, then the activity keeps decreasing progressively. If we treat 100000 posts per hour as a benchmark, 6:00 am to 7:00 pm would be the period during which users are more active. 
# Conclusion and trend

# In[13]:

get_ipython().magic(u'matplotlib inline')
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
axes = fig.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_count.T.sum(), 'b')
plt.plot()
axes.set_xlabel('Hours')
axes.set_xticks(range(24))
axes.set_ylabel('Counts')
axes.set_title('Comparison Among Different Hours Every Day')


##### Plot: Users Active Dates

# Using the same logic as the previous plot, we come up with another plot indicating the active dates of users on Reddit. Surprisingly, users are less active on weekends, which is different with my previous expectation. Obviously, users are more active from Monday to Thursday and starts to be less involved on Reddit from Thursday, then the decreasing trend continues until next Monday.

# In[14]:

get_ipython().magic(u'matplotlib inline')
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
axes = fig.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Date_count.T.sum(), 'b')
plt.plot()
Time = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
axes.set_xlabel('Days')
axes.set_xticklabels(Time)
axes.set_ylabel('Counts')
axes.set_title('Comparison Among Different Week Days')


##### Plot: Care Values Comparison Among Different Posting Time 

# Basically, I want to figure out the relationship between the Care Value and Posting time and I hope there will be some inditation between the changing trend of Care Value and the changing trend of Posting Time. Notice that for each posting time, I chose the maximum care value achieved over 2500 subreddits, which is more representative and robust than mean. It turns out I have the same trend as indicated in the plot 'Comparison Among Different Hours Every Day'.

# In[15]:

get_ipython().magic(u'matplotlib inline')
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
axes = fig.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_care.T.median(), 'r')
plt.plot()
axes.set_xlabel('Posting Time')
axes.set_xticks(range(24))
axes.set_xticklabels(range(24))
axes.set_ylabel('Counts')
axes.set_title('The Relationship between Care Values and Posting Hour')


##### Intermediate Conclusion:

# We can conclude that the care value, which is the indication of number of views the post would receive is closely correlated with the users' active time on Reddit. Thus, if you want to put a post looking for quick answer, it is recommended to post it during 7:00 to 14:00 during which Reddit users are more active.

# In[16]:

fig_count = plt.gcf()
axes = fig_count.add_axes([0.2,0.2,1.5,1.5])
stand_Time_count = (Time_count.T.sum() - np.mean(Time_count.T.sum()))/np.std(Time_count.T.sum())
stand_Time_care = (Time_care.T.median() - np.mean(Time_care.T.median()))/np.std(Time_care.T.median())
plt.plot(stand_Time_count, 'b')
plt.plot(stand_Time_care, 'r')
plt.plot()
axes.set_xlabel('Time')
axes.set_xticks(range(24))
axes.set_ylabel('Standardized Value')
axes.set_title('Standardized Posting Counts & Care Value')
plt.legend(('post_time','care_value'))


##### Plot: What do I want to say?

# In[17]:

get_ipython().magic(u'matplotlib inline')
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
axes = fig.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_karma.max(), 'r')
plt.plot(Time_karma.median(), 'b')
plt.plot()
axes.set_xlabel('Different Subreddits')
axes.set_ylabel('Care Value')
axes.set_title('Karma Value Over Different Subreddit')
plt.legend(('karma max', 'karma median'))


##### Plot: Karma Value Comparison Among Different Posting Hours

# In[18]:

fig3 = plt.figure()
axes = fig3.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_karma.T.median(), 'r')
axes.set_xticks(range(24))
axes.set_xlabel('Time')
axes.set_ylabel('Karma')
axes.set_title('Comparison of Different Karma Values Over 24 Hours')


##### Plot: The Relationship of Posting Time and Karma Value

# As we can see from the bottom plot, it seems the karma trend does not follow the user's activity trend closely. Compared with the the previous plot 'Standardized Posting Counts & Care Value', which indicates that the number of views is closely related to the number of active users online. On the other hand, since karma represents the difference of uppost and downpost and it directly influence the position of a post under a subreddit. Thus, it seems posting post during the active time does not necessarily lead to a better rank for your post.

# In[37]:

fig1 = plt.figure()
axes = fig1.add_axes([0.2,0.2,1.5,1.5])
stand_Time_count = (Time_count.T.sum() - np.mean(Time_count.T.sum()))/np.std(Time_count.T.sum())
stand_Time_karma = (Time_karma.T.median() - np.mean(Time_karma.T.median()))/np.std(Time_karma.T.median())
plt.plot(stand_Time_karma, 'r')
plt.plot(stand_Time_count, 'b')
axes.set_xticks(range(24))
axes.set_xlabel('Time')
axes.set_ylabel('Karma Value')
axes.set_title('Standardized Posting Counts and Karma Values')


# # Text Mining

### General Analysis

##### From the perspective of care value:

# The function below is used to extract the title and content parts that in most popular(evaluated by care value) and least popular (evaluated by care value)posts over 2498 subreddits.

# In[20]:

Top_Title = []
Top_Content = []
Bottom_Title = []
Bottom_Content = []

for i in name[0][0:2500]:
    try:
        original = i
        index = i + 'Clean' + '.csv'
        a = pd.read_table(index, sep = "\t")
        a['care_value'] = a['ups'] + a['downs'] 
        Top_Title.append(a['title'][a['care_value'].argmax()])
        Top_Content.append(a['selftext'][a['care_value'].argmax()])
        Bottom_Title.append(a['title'][a['care_value'].argmin()])
        Bottom_Content.append(a['selftext'][a['care_value'].argmin()])
    except:continue


##### From the perspective of care value:

# The function below is used to extract the title and content parts that in most popular(evaluated by karma value) and least popular (evaluated by karma value)posts over 2498 subreddits.

# In[21]:

Top_rank_Title = []
Top_rank_Content = []
Bottom_rank_Title = []
Bottom_rank_Content = []

for i in name[0][0:2500]:
    try:
        original = i
        index = i + 'Clean' + '.csv'
        a = pd.read_table(index, sep = "\t")
        a['karma'] = a['ups'] - a['downs'] 
        Top_rank_Title.append(a['title'][a['karma'].argmax()])
        Top_rank_Content.append(a['selftext'][a['karma'].argmax()])
        Bottom_rank_Title.append(a['title'][a['karma'].argmin()])
        Bottom_rank_Content.append(a['selftext'][a['karma'].argmin()])
    except:continue


# Test: test function which would be used by nose package to check if the extrcated information is correct

# In[22]:

def test_5():
    assert len(Top_Title)==len(Top_Content)==len(Bottom_Title)==len(Bottom_Content)==2498


# In[23]:

def test_6():
    assert len(Top_rank_Title)==len(Top_rank_Content)==len(Bottom_rank_Title)==len(Bottom_rank_Content)==2498


##### Compare the title of mostly viewed post with highest ranked view

# We defined a function called wordclouds to create wordcloud for the input word information

# In[218]:

from os import path
import sys
import wordcloud
from IPython.display import Image
def wordclouds(x):
    d = path.dirname("/Users/MrG/Capstone/")
    words = wordcloud.process_text(str(x), max_features = 500)
    elements = wordcloud.fit_words(words)
    wordcloud.draw(elements, path.join(d,"WC.png"), scale = 5)
    return Image(filename='/Users/MrG/Capstone/WC.png', height= 1000, width= 618)


# In[219]:

wordclouds(Top_Title)


# In[220]:

wordclouds(Top_rank_Title)


##### Compare the content of mostly viewed post with highest ranked view

# In[221]:

wordclouds(Top_Content)


# In[222]:

wordclouds(Top_rank_Content)


# Conclusion: It seems the general analysis does not produce enough useful information since it contains too much useless information that should be cleaned from the word pool. Thus, the next step of our research is to conduct a deeper analysis.

### Deeper Analysis

# Here we define a function to do text cleaning. Basically, The function will be used several times to extract useful information from the title and content of a post.

# In[181]:

import nltk
import nltk.data
from nltk.corpus import stopwords
import re
stop = stopwords.words('english')
stop = stop + ['nan','http','www','xe','com','The','the','WWW','When','Where','\n','\nThe','\nThis','nThe','nthe','nThis','nthis']
def getword(x):
    Important_word = []
    title_token = nltk.regexp_tokenize(str(x), pattern = "\w+(?:[-']\w+)*|'|[-.(]+|\S\w*")
    for i in title_token:
        if i not in stop:
            Important_word.append(i)
    Important_word = str(Important_word)
    word = re.findall(r'\w{5,}', Important_word) # Here 4 can be changed to any number to extract the words with different length
    return(word)


# Test: an example to see how the function works

# In[182]:

# See if the function works well. Note: this is checked by ourselves rather than by nose
test_word = ['nan','http://www.hao123.com','www is the life','xe is useless','This','\nThe word//: http','com','I know this is the life','remember the name','one 21 guns','no body has any idea']
getword(test_word)


# All the cleaned word pool available("Add more detail")

# In[183]:

word_pool_top_title = getword(Top_Title)
word_pool_bottom_title = getword(Bottom_Title)
word_pool_top_rank_title = getword(Top_rank_Title)
word_pool_bottom_rank_title = getword(Bottom_rank_Title)
word_pool_top_content = getword(Top_Content)
word_pool_bottom_content = getword(Bottom_Content)
word_pool_top_rank_content = getword(Top_rank_Content)
word_pool_bottom_rank_content = getword(Bottom_rank_Content)
print word_pool_top_content[:100]


# Tag words with its property. The function addtag is used to add the property of words to the tag

# In[184]:

def addtag(x):
    tagged=[]
    rep = len(x)//10000 + 1
    for i in range(rep):
        num = i*10000
        end = num+10000
        if i== rep - 1:
            words = nltk.pos_tag(x[num:])
            tagged +=words
        else:
            print num, end
            words = nltk.pos_tag(x[num:end])
            tagged +=words
    return(pd.DataFrame(tagged))


# Now we tag the four word pools that we have drawn previously. We need to say more about it

# In[185]:

tagged_top_content = addtag(word_pool_top_content)
tagged_bottom_content = addtag(word_pool_bottom_content)
tagged_top_title = addtag(word_pool_top_title)
tagged_bottom_title = addtag(word_pool_bottom_title)


# In[186]:

tagged_top_rank_content = addtag(word_pool_top_rank_content)
tagged_bottom_rank_content = addtag(word_pool_bottom_rank_content)
tagged_top_rank_title = addtag(word_pool_top_rank_title)
tagged_bottom_rank_title = addtag(word_pool_bottom_rank_title)


# # Graphs from Deeper Analysis

# Write out word_pool so that we can read them into R where we use a more mature wordcloud package to create our word cloud Notice the word_pool2.csv is the name of the output file. We use this output chunk several times but we did not repeatedly writeit in several chunks.
# Note: we have found an alternative way to create word cloud using python package, the sample is in the bottom of the ipython notebook

# In[204]:

tagged_top_content.columns = ["word","class"]
tagged_bottom_content.columns = ["word","class"]
tagged_top_title.columns = ["word","class"]
tagged_bottom_title.columns = ["word","class"]
tagged_top_rank_content.columns = ["word","class"]
tagged_bottom_rank_content.columns = ["word","class"]
tagged_top_rank_title.columns = ["word","class"]
tagged_bottom_rank_title.columns = ["word","class"]


# In[254]:

def noun(x):
    noun_list = x.loc[x['class'] == ('NNP' or 'NN' or 'NNPS' or 'NNS'), 'word'].tolist()
    return(noun_list)
def verb(x):
    verb_list = x.loc[x['class'] == 'VB', 'word'].tolist()
    return(noun_list)


# In[244]:

wordclouds(str(noun(tagged_top_content)))


# In[245]:

wordclouds(str(noun(tagged_top_rank_content)))


# In[246]:

wordclouds(str(noun(tagged_bottom_content)))


# In[247]:

wordclouds(str(noun(tagged_bottom_rank_content)))


# The output program :
# You can change Top_tag to whatever name that indicate the tag file you created before. Anyway, we use the code several times for creating different csv files to generate word cloud plots.

# In[248]:

wordclouds(str(noun(tagged_top_title)))


# In[249]:

wordclouds(str(noun(tagged_top_rank_title)))


# In[252]:

wordclouds(str(noun(tagged_bottom_title)))


# In[251]:

wordclouds(str(noun(tagged_bottom_rank_title)))


# In[255]:

wordclouds(str(verb(tagged_top_content)))


# In[256]:

wordclouds(str(verb(tagged_top_rank_content)))


# Also we want to create a distribution plot of the top used words in the title of most popular posts. Similarly, we can create many kinds of similar plot if we are interested in.

# In[273]:

def freqPlot(x, y):
    Title_token = nltk.wordpunct_tokenize(str(x))
    Title_key = []
    for i in Title_token:
        if i not in stop:
            Title_key.append(i)
    Title_key = str(Title_key)
    Title_key = re.findall(r'[A-Z]*[a-z]{5,}', Title_key)
    Title_key_dist = nltk.FreqDist(Title_key)
    return Title_key_dist.plot(y)


# In[274]:

freqPlot(Top_rank_Content, 30)


# In[275]:

freqPlot(Top_Content, 30)


# In[278]:

freqPlot(Top_rank_Title, 30)


# In[277]:

freqPlot(Top_Title, 20)


# In[280]:

freqPlot(Bottom_Content, 30)


# In[281]:

freqPlot(Bottom_Title, 30)


# #Test Function:

# In[259]:

cd ~/Capstone/Nose_extension/


# Basically this is the chunk used to run the test function. 
# If your computer has installed extension of nose, then you can just run. Or you can clone the Nose_ipython document in my github and run the following code in the next two cells, it shouldwork if you can download/clone the nose_extension document successfully.

# In[260]:

get_ipython().magic(u'load_ext ipython_nose')
get_ipython().magic(u'nose -v -x')

