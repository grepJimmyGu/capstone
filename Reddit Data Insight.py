
# coding: utf-8

# #Background

# Reddit is one of the largest social news and entertainment website and it provides a platform for people to communicate and share information across different subjects. The data we used comes from a github respository with 2.5 million posts of 2498 subreddits (custom-made subforum/category). 
# 
# In total, we have 2498 CSV files with each one containing information on the top 1000 posts within a subreddit, selected based on their karma scores. Viewers can vote up/down posts, and the difference between up votes and down votes generates a score called Karma. Posts within each subreddit are ranked based on their karma values. The data was pulled between Aug 15-20, 2013. Note that although the data was retrieved during that time, posts were not necessarily generated within that time range.

# **Guideline of the Report**

# This report is generated as a pdf from our ipython notebook. All data and files shown below can be found on github at https://............ The report contains annotated code, test functions and methods used to run our analysis and everything should be replicatable.
# 
# For summary of our analysis, please refer to the "Result" section at the end of this report.

# #Whose Mind We Are Going To Change

# **Questions**

# We are interested in user behaviors and characteristics of popular posts. Specifically, we want to find out: 
# 
# 1) When do users post actively online? Do user act differently on weekdays and weekends? 
# 
# 2) What elements of titles/content characterize a popular post? Is there a difference between the most popular posts and the least popular posts? 

# $$\noindent$$**Motivation**

# By answering these questions, we hope to inform Reddit community of user behaviour in general and suggest them on how to post effectively in order to gain more attention. 

# # Method

# **To answer question one**

# We create two variables, karma value and care value, based on the number of up/down votes to measure popularity of each post. Because a post with a low karma value could possibaly have high popularity (i.e., a post with 1000 up votes and 999 down votes will only have a karma score of 1, but that doesn't mean it is unpopular). Thus, care value is calculated from the sum of up and down votes, and serves as a measure of total views for each post. Overall, karma value indicates the "reputation" of a post, while care value captures how much attention each post draws. User activity is measured using total number of posts generated within each hour/day of week for all the posts.
# 
# Plots are generated to observe how user activity behaves. Also, comparison of karma scores and care values are plotted to show how the trend changes with time.
# 

# $$\noindent$$**To answer question two**

# We decide to use text mining techniques to analyze titles and contents of the most popular posts and the least popular posts across all subreddit. Two measures of popularity serve as selection criteria for picking the most/least popular posts. To be more clear, the post with highest/lowest karma/care value will be selected within each subreddit, which will result in four datasets (i.e, posts with highest karma values, lowest karma values, highest care values and lowest care values), each containning 2498 selected posts and their titles and contents.
# 
# The package NLTK is used to analyze texts. Stop words like "I, you, and, the" are filtered out. For the remaining words, frequency of each word is calculated and used to generate word cloud.

# $$\noindent$$**Variables Selected**

# Based on the questions raised above, we selected the following variables to run our analysis: Time(when the post was generated), Subreddit, Number of Up Vote, Number of Down Vote, Title, Selt Text(content of a post). 

# $$\noindent$$**More on the variables**

# The time is stored in Epoch time (seconds elapsed since 00:00:00 on 01/01/1977). We will transform the time into a standard format and extract the hour and the day of week when each post was created. For self text, it could be texts as well as links the author posted, or empty.

# # Preparation

# ##Import packages used

# In[4]:

cd ~/Capstone/Meta/MetaData/


# In[5]:

import pandas as pd
import numpy as np
import datetime
import nltk 
from __future__ import division


# In[6]:

name = pd.read_table("Name", sep = ",", header = None)


# In[7]:

def test_1():
    assert len(name[0])==2500


# ## Data Cleaning

# The data cleaning part includes two parts: The first part is the UNIX shell command used to download the data from website and preprocess the information, so that they can be read into python to do further analysis. The second part is python code used to extract useful information from the preprocessed data. As we all know, data cleaning is a process weaved within the entire project, so this part does not necessarily include all the data cleaning efforts.

# The following chunk is used to select out variables that we are interested in and store them in the dataframe we have created such as Time_count, Time_karma and Time_care. Basically, those are the dataframes containing post counts, karma values and care values over 24 hours.

# In[8]:

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
        Time_karma[original] = temp_karma.groupby('Time', as_index = False).max()['karma']
        #group by hour, calculate the mean karma value within each hour
        Time_care[original] = temp_care.groupby('Time', as_index = False).max()['care_value']
        #group by hour, calculate the max care value within each hour
    except: continue
#Time_karma.drop('Time', axis = 1)
#Time_care.drop('Time', axis = 1)


# In[9]:

def test_2():
    assert len(Time_karma.columns)==2499
    assert Time_karma.shape==(24, 2499) 
    if all(Time_karma.Time <24) and all(Time_karma.Time >=0):
        assert True


# In[10]:

def test_3():
    assert len(Time_care.columns)==2499
    assert Time_care.shape==(24, 2499) 
    if all(Time_care.Time <24) and all(Time_care.Time >=0):
        assert True


# In[11]:

Test = pd.read_table("2007scapeClean.csv")
# A sample of the cleaned data file
#Test.head(10)


# In[12]:

#print Time_care['0x10c'].head(5)
#print Time_karma['30ROCK'].head(5)
#print Time_count['zelda'].head(5)


# ## Data Extraction

# Date_count is the dataframe we used to count the number of posts over different weekdays over all subreddits, and we use this information to explore user activity on Reddit. To be specific, we want to know if they are more active on posting during weekdays or weekends.

# In[13]:

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


# $$\noindent$$**Sample**:

# In[14]:

print Date_count['0x10c']
print Date_count['backpacking']


# In[15]:

def test_4():
    assert Date_count.shape==(7, 2501) 
    if all(Date_count.Time <7) and all(Date_count.Time  >=0):
        assert True


# # Result

# ##Care Value Analysis

# **Plot: Users Active Hours** 

# Based on the posting time of 2.5 million posts (all created before August 20 2013), we created the plot of total post counts vs. users' posting hours. For example, if there are 40000 posts created between 1:00 to 1:59:59, then these posts are classified as the posts with a tag 1, and the data point corresponds to a y value of 40000. As we can see from the plot, the users involvment keeps increasing from 2:00 am to 10:00 am and reachs its peak at 10:00 am, then dies down progressively. If we treat 100000 posts per hour as a benchmark, 6:00 am to 7:00 pm would be the period during which users are more active.
# 
# The fact that most posts were created in the morning contradicts our assumption that users are more active during their free time. The truth is most people are posting online during working hours.

# In[16]:

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


# $$\noindent$$**Plot: Users Active Dates** 

# Using the same logic as the previous plot, we come up with another plot indicating the active dates of users on Reddit. Surprisingly, users are less active on weekends, which is different with my previous expectation. Obviously, users are more active from Monday to Thursday and starts to be less involved on Reddit from Thursday, then the decreasing trend continues until next Monday.

# In[17]:

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


# $$\noindent$$**Plot: Care Values Comparison Among Different Posting Time** 

# Basically, I want to figure out the relationship between the care value and posting time and I hope there will be some indication between the changing trend of care value and the changing trend of posting Time. Notice that for each posting time, I chose the maximum care value achieved over 2500 subreddits, which is more representative and robust than mean. It turns out I have the same trend as indicated in the plot 'Comparison Among Different Hours Every Day'.

# In[18]:

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


# $$\noindent$$**Intermediate Conclusion** 

# We can conclude that the care value, which is the indication of number of views the post would receive is closely correlated with the users' active time on Reddit. Thus, if you want to put a post looking for quick answer, it is recommended to post it during 7:00 to 14:00 during which Reddit users are more active.

# $$\noindent$$**Plot: Comparison between Care Value and Post Counts** 

# In order to compare the two trends shown above, we standardize care values and post counts, and plot them over different hours. The blue line indicates post counts, and the red indicates care values. We can see the two trends overlap most of the time.

# In[19]:

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


# ##Karma Value Analysis

# **Plot: Karma Value Over Different Subreddit** 

# Since karma valuse is the standard used for Reddit to rank all of the post, we are interested in knowing if karma value varies over different subreddit. However, each subreddit contains a number of posts with different karma values, we need to find out the representatives. Thus, we decided to pick out the median and max among all of karma values belonging to the same subreddit and draw them in the same graph. 
# 
# The Histogram below shows the karma max with red line and karma median with blue line over 2498 subreddits. Although the obvious information is not obvious, we still want to point out that for most of subreddits: the difference between karma max and karma median is comparably large indicating that most of posts have a really low karma value. We think it is intuitively true since seldom do we have really popular post on website and most of posts are pretty much trash.

# In[21]:

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


# $$\noindent$$**Plot: Karma Value Comparison Among Different Posting Hours**

# Out of similar intention, we are interested in finding out the 'active hours' during which users are more likely to enjoy 'good post'. Suprprisingly, we have similar trend compared with the previous 'Care Value Over 24 Hours' plot, that is, karma values are higher during working hours. 

# In[22]:

fig3 = plt.figure()
axes = fig3.add_axes([0.2,0.2,1.5,1.5])
plt.plot(Time_karma.T.median(), 'r')
axes.set_xticks(range(24))
axes.set_xlabel('Time')
axes.set_ylabel('Karma')
axes.set_title('Comparison of Different Karma Values Over 24 Hours')


# $$\noindent$$**Plot: The Relationship of Posting Time and Karma Value** 

# As we can see from the bottom plot, it seems that karma trend does not follow the user's activity trend closely. Compared with the the previous plot 'Standardized Posting Counts & Care Value', which indicates that the number of views is closely related to the number of active users online. On the other hand, since karma represents the difference of uppost and downpost and it directly influence the position of a post under a subreddit. Thus, it seems posting post during the active time does not necessarily lead to a better rank for your post.

# In[19]:

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


# ## Text Mining

# ###General Analysis

# **From two perspectives: care value & karma value**

# Through out our whole project, we have been interested in comparing or extracting information based on two benchmarks: care value and karma value. Undoubtedly, we are going to use both of the benchmarks to do text mining, thus we are going to do every following step from two perspectives.

# In[23]:

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


# In[27]:

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


# In[28]:

def test_5():
    assert len(Top_Title)==len(Top_Content)==len(Bottom_Title)==len(Bottom_Content)==2498


# In[29]:

def test_6():
    assert len(Top_rank_Title)==len(Top_rank_Content)==len(Bottom_rank_Title)==len(Bottom_rank_Content)==2498


# $$\noindent$$**Compare the title of mostly viewed post (care value) with highest ranked view (karma value)**

# We used word cloud package to generate the following two wordclouds in order to find out the trend conceived in the title of different posts. However, it seems that we have a lot of meaningless words showing up in the wordcloud, which is due to the fact that we have not cleaned the text data in a deeper level. Despite of the fact that the text data are not cleaned very well, we still find some generally used words such as 'post','upvote', but we can hardly draw any conclusion based on the information.

# In[49]:

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


# $$\noindent$$**Top title from the perspective of care value**

# In[50]:

wordclouds(Top_Title)


# $$\noindent$$**Top title from the perspective of karma value**

# In[51]:

wordclouds(Top_rank_Title)


# $$\noindent$$**Compare the content of mostly viewed post with highest ranked view** 

# Similarly, we have more meaningless information showing up here, and we even can not find some meaningful words

# $$\noindent$$**Top content from the perspective of care value**

# In[47]:

wordclouds(Top_Content)


# $$\noindent$$**Top content from the perspective of karma value**

# In[48]:

wordclouds(Top_rank_Content)


# $$\noindent$$**Intermediate Conclusion ** 

# It seems the general analysis does not produce enough useful information since it contains too much useless information that should be cleaned from the word pool. Thus, the next step of our research is to conduct a deep analysis.

# ###Deep Analysis

# In this part, we used nltk package to do a deep text mining:
# 
# Firstly, we cleaned the raw text information using regular expression in order to eliminate some useless marks and meaningless messy codes. For example, words like 'https','nan','www' and 'com' are eliminated. Besides, we removed some stop words based on the stop words dictionary from nltk package, which includes 'the','I','you' and so on. After the cleaning part, we are left with more meaningful words.
# 
# Then, we used the pos_tag function from nltk package to tag the word with its property, for example, 'like' is tagged as verb, 'night' us tagged as noun and 'America' is tagged as proper noun. Although it is possible to use a training text data set to make the tag process more accurate and relevant with the background of our project, we did not attempt to contruct a training text data set due to time and knowledge constraint. Note that we do have word like 'start' which can be hardly categorized as noun or verb.
# 
# Finally, we will have the cleaned version of data and we can use them to derive further conclusions.

# In[1]:

import nltk
import nltk.data
from nltk.corpus import stopwords
import re
stop = stopwords.words('english')
stop = stop + ['nan','http','www','xe','com','The','the','WWW','When','Where']
def getword(x):
    Important_word = []
    title_token = nltk.regexp_tokenize(str(x), pattern = "\w+(?:[-']\w+)*|'|[-.(]+|\S\w*")
    for i in title_token:
        if i not in stop:
            Important_word.append(i)
    Important_word = str(Important_word)
    word = re.findall(r'\w{5,}', Important_word) # Here 4 can be changed to any number to extract the words with different length
    return(word)


# In[2]:

# See if the function works well. Note: this is checked by ourselves rather than by nose
test_word = ['nan','http://www.hao123.com','www is the life','xe is useless','This']
# getword(test_word)


# All the cleaned words are put into a 'word pool', which makes them available for further steps. Since we are interested in the popularity of posts and characteristics of their texts, we created 8 word pools ( 4 categories):
# 
# 1. Titles from the most/least viewed posts (Top_Title and Bottom_Title below)
# 
# 
# 2. Contents from the most/least viewed posts (Top_Content and Bottom_Content below)
# 
# 
# 3. Titles from the highest/lowest ranking posts (Top_rank_Title and Bottom_rank_Title)
# 
# 
# 4. Contents from the highest/lowest ranking posts (Top_rank_Content and Bottom_rank_Content)
# 

# In[2]:

word_pool_top_title = getword(Top_Title)
word_pool_bottom_title = getword(Bottom_Title)
word_pool_top_rank_title = getword(Top_rank_Title)
word_pool_bottom_rank_title = getword(Bottom_rank_Title)
word_pool_top_content = getword(Top_Content)
word_pool_bottom_content = getword(Bottom_Content)
word_pool_top_rank_content = getword(Top_rank_Content)
word_pool_bottom_rank_content = getword(Bottom_rank_Content)
print word_pool_top_content[:100]


# In[3]:

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
            words = nltk.pos_tag(x[num:end])
            tagged +=words
    return(pd.DataFrame(tagged))


# In[41]:

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


# In[34]:

tagged_top_content = addtag(word_pool_top_content)
tagged_bottom_content = addtag(word_pool_bottom_content)
tagged_top_title = addtag(word_pool_top_title)
tagged_bottom_title = addtag(word_pool_bottom_title)


# In[35]:

tagged_top_rank_content = addtag(word_pool_top_rank_content)
tagged_bottom_rank_content = addtag(word_pool_bottom_rank_content)
tagged_top_rank_title = addtag(word_pool_top_rank_title)
tagged_bottom_rank_title = addtag(word_pool_bottom_rank_title)


# ### WordCloud

# In order to explore the characterictics of different posts, we decide to use wordcloud and frequency plots to present the 8 word pools that we extracted in previous steps.
# 
# Since the tags are generated automatically using the NLTK package, the tags ("class" below) contain different parts of speech that we need to choose from. Each word cloud will contain at most 500 words for the sake of clarity, and the size of each word is proportional to its frequency. To better reflect the contents of texts, we decide to choose "NN" and "NNP" to generate word clouds. "NN" indicates nouns, and "NNP" indicates proper nouns like " Alison" or "Washington". Frequency plots are generated using the word pool without differencing among parts of speech, which gives us a broader look on the texts.

# **Note**

# We also define a function verb to extract verbs from word pools in order to have a peek on the comparison between verbs and nouns.

# In[36]:

tagged_top_content.columns = ["word","class"]
tagged_bottom_content.columns = ["word","class"]
tagged_top_title.columns = ["word","class"]
tagged_bottom_title.columns = ["word","class"]
tagged_top_rank_content.columns = ["word","class"]
tagged_bottom_rank_content.columns = ["word","class"]
tagged_top_rank_title.columns = ["word","class"]
tagged_bottom_rank_title.columns = ["word","class"]


# In[67]:

def noun(x):
    noun_list = x.loc[x['class'] == ('NNP' or 'NN'), 'word'].tolist()
    return(noun_list)
def verb(x):
    verb_list = x.loc[x['class'] == 'VB', 'word'].tolist()
    return(verb_list)


# $$\noindent$$**Contents from the Most Viewed Posts**

# For top contents, the word "start" is used most frequently and displayed as the largest, probably because the dictionary treats "start" both as verb and noun, but does not separate the frequency accordingly. 
# 
# "YouTube" has a high frequency because many users are posting youtube links on Reddit. The link itself becomes the content.

# $$\noindent$$**Note**

# It's reasonable that the frequency plot does not correspond to the wordcloud, due to the mechanism of different dictionaries used by the NLTK package.

# In[68]:

wordclouds(str(noun(tagged_top_content)))


# In[71]:

freqPlot(Top_Content, 30)


# $$\noindent$$**Contents from the Highest Ranked Posts**

# The word cloud below is very similar to the most viewed posts, as there might be a large overlap between the most viewed and the highest ranked posts. Some topic-specific words show up such as "Remix" and "Update".

# In[43]:

wordclouds(str(noun(tagged_top_rank_content)))


# In[44]:

freqPlot(Top_rank_Content, 30)


# $$\noindent$$**Contents from the Least Viewed Posts**

# Some frequently used words such as "Start" and "Google" also appear in the least viewed posts. Besides that, most high frequency nouns appeared below do not relate to a specific topic. 

# In[45]:

wordclouds(str(noun(tagged_bottom_content)))


# In[46]:

freqPlot(Bottom_Content, 30)


# $$\noindent$$**Contents from the Lowest Ranked Posts**

# Different from the least viewed posts, the lowest ranked posts have some words that are more frequently used than the others, such as "Unusual", "Round" and "Wonka". Our interpretation for this difference is that lowest ranked posts have some common features which distinguish themselves from those on the least viewed side.

# In[47]:

wordclouds(str(noun(tagged_bottom_rank_content)))


# In[49]:

freqPlot(Bottom_rank_Content, 30)


# $$\noindent$$**Titles from the Most Viewed Posts** 

# It's not surprising to see "Reddit" here as lot of posts are related to the site itself. For example, a typical post could have a title like "Just a quick question on using Reddit, please don't upvote". We also see some other interesting words like "Boston" or "Obama", which might come from heated discussion on the Boston Marathon Bombings and the Presidential Election.
# 
# Another big part of high frequency words is social media and gaming. "Facebook" and "Youtube" appear quite frequently. It's also interesting to see "North" and "Korea" show up as two words. Again, this might be a result from our untrained dictionary.

# In[50]:

wordclouds(str(noun(tagged_top_title)))


# In[51]:

freqPlot(Top_Title, 30)


# $$\noindent$$**Titles from the Highest Ranked Posts**

# In[52]:

wordclouds(str(noun(tagged_top_rank_title)))


# In[53]:

freqPlot(Top_rank_Title, 30)


# $$\noindent$$**Titles from the Least Viewed Posts**

# In[54]:

wordclouds(str(noun(tagged_bottom_title)))


# In[55]:

freqPlot(Bottom_Title, 30)


# $$\noindent$$**Titles from the Lowest Ranked Posts**

# In[56]:

wordclouds(str(noun(tagged_bottom_rank_title)))


# In[57]:

freqPlot(Bottom_rank_Title, 30)


# $$\noindent$$**Verb Analysis from Most Viewed Post**

# In[65]:

wordclouds(str(verb(tagged_top_content)))


# $$\noindent$$**Verb Analysis from Least Viewed Post**

# In[66]:

wordclouds(str(verb(tagged_bottom_content)))


# Also we want to create a distribution plot of the top used words in the title of most popular posts. Similarly, we can create many kinds of similar plot if we are interested in.

# #Test Function Used to Validate Analysis

# In[62]:

cd ~/Capstone/Nose_extension/


# Basically this is the chunk used to run the test function. 
# If your computer has installed extension of nose, then you can just run. Or you can clone the Nose_ipython document in my github and run the following code in the next two cells, it shouldwork if you can download/clone the nose_extension document successfully.

# In[63]:

get_ipython().magic(u'load_ext ipython_nose')
get_ipython().magic(u'nose -v -x')


# #Conclusion

# In[ ]:



