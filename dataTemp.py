
# coding: utf-8

# Read Data set

# In[1]:

import decision

import pandas as pd
import numpy as np
import math
import dateutil.parser as dparser
import time
import random
# In[2]:

starttime = time.time();

data_bot = pd.read_csv('data/bots_data.csv', encoding='iso-8859-1')
data_nonbot = pd.read_csv('data/nonbots_data.csv', encoding='iso-8859-1')
data_combine = data_bot
data_combine = data_combine.append(data_nonbot, ignore_index=True)
#data_combine.head(100)


# In[3]:

def checkNone(data_class, attrstr):
    #return two class: 1/0
    #None:1    not-None:0
    data_class[attrstr]=0
    idx = 0
    for value in data_combine[attrstr]:
        if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
            data_class[attrstr][idx] = 1
        idx += 1


# In[4]:

def checkTF(data_class, attrstr):
    #return two class: 1/0
    #True:0    False:1
    data_class[attrstr]=0
    idx = 0
    for value in data_combine[attrstr]:
        if value == False:
            data_class[attrstr][idx] = 1
        idx += 1


# In[5]:

def checkNumber(data_class, attrstr, effi):
    #return n=log with base-effi
    data_class[attrstr]=0
    idx = 0
    for value in data_combine[attrstr]:
        if effi == 10:
            data_class[attrstr][idx] = int(math.log10(data_combine[attrstr][idx]+1))
        elif effi == 2:
            data_class[attrstr][idx] = int(math.log2(data_combine[attrstr][idx]+1))
        else:
            data_class[attrstr][idx] = int(math.log(data_combine[attrstr][idx]+1, effi))
        idx += 1


# In[6]:

def checkEnglish(data_class, attrstr):
    #return isEnglish:1    other:0
    data_class[attrstr]=0
    idx = 0
    for value in data_combine[attrstr]:
        if value == "en":
            data_class[attrstr][idx] = 1
        idx += 1


# In[7]:

def checkDate(data_class, attrstr):
    #date index:
    #    year<=2012: 0:3
    #    year==2013: 4:7
    #    year==2014: 8:11
    #    year==2015: 12:15
    #    year==2016: 16:19
    #    year==2017: 20:23
    data_class[attrstr]=0
    idx = 0
    for value in data_combine[attrstr]:
        y = dparser.parse(value,fuzzy=True).year
        m = dparser.parse(value,fuzzy=True).month
        if y ==2013:
            data_class[attrstr][idx] = 4
        elif y == 2014:
            data_class[attrstr][idx] = 8
        elif y == 2015:
            data_class[attrstr][idx] = 12
        elif y == 2016:
            data_class[attrstr][idx] = 16
        elif y == 2017:
            data_class[attrstr][idx] = 20
        #month
        if m>6:
            data_class[attrstr][idx]+= 1
        idx += 1


# In[8]:

#Defined robot dictionary here
botDict = ["bot",
           "Bot",
           "robot",
           "Robot"]


# In[9]:

def checkStringBot(data_class, attrstr):
    #return has sub string in botDict:1     else:0
    data_class[attrstr]=0
    idx = 0
    for value in data_combine[attrstr]:
        for dic in botDict:
            if value.find(dic) != -1:
                data_class[attrstr][idx] = 1
        idx += 1


# In[10]:

def DataFrameFilter():
    data_class = data_combine[['bot']].copy(deep=True)
    attrList = data_combine.columns.values
    for attrStr in attrList:
        if attrStr == "id":
            checkNumber(data_class, attrStr, 10)
            #print(attrStr)
        
        #elif attrStr == "id_str":
        #    print(attrStr)
        
        elif attrStr == "screen_name":
            checkStringBot(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "location":
            checkNone(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "description":
            checkNone(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "url":
            checkNone(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "followers_count":
            checkNumber(data_class, attrStr, 2)
            #print(attrStr)
        
        elif attrStr == "friends_count":
            checkNumber(data_class, attrStr, 2)
            #print(attrStr)
        
        elif attrStr == "listedcount":
            checkNumber(data_class, attrStr, 2)
            #print(attrStr)
        
        elif attrStr == "created_at":
            checkDate(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "favorites_count":
            checkNumber(data_class, attrStr, 2)
            #print(attrStr)
        
        elif attrStr == "verified":
            checkTF(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "statuses_count":
            checkNumber(data_class, attrStr, 2)
            #print(attrStr)
        
        elif attrStr == "lang":
            checkEnglish(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "status":
            checkNone(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "default_profile":
            checkTF(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "default_profile_image":
            checkTF(data_class, attrStr)
            #print(attrStr)
        
        elif attrStr == "has_extended_profile":
            checkTF(data_class, attrStr)
            #print(attrStr)
        
        #elif attrStr == "name":
            #print(attrStr)       

    return data_class


# In[11]:

#example

data_example = DataFrameFilter()
ma=[];
for name in data_example.columns:
    if name!='bot':
        ma.append(name);

accuracy = 0.0
precision = 0.0
recall = 0.0
f1score = 0.0

for kk in range(5):
    print(kk)
    indexlist=[];

    for i in range(len(data_example)):
        indexlist.append(i)

    random.shuffle(indexlist)
    size = len(indexlist)
    for k in range(10):
        train = []
        test = []
        for i in range(size):
            if (i >= k * size/10) and ( i <=(k+1)*size/10):
                test.append(indexlist[i])
            else:
                train.append(indexlist[i])
        mynode = decision.makesubtree(data_example,ma,'bot',train)
        result = decision.judgeData(mynode, data_example, ma, 'bot',test )
        tp=result[0]
        fp=result[1]
        fn=result[2]
        tn=result[3]
        accuracy += (tp+tn)/len(test)
        precise = tp/(tp+fp)
        recal = tp/(tp+fn)
        precision += precise
        recall+=recal
        f1score+=2*(1/((1/precise)+(1/recal)))
print("accuracy:",accuracy/50)
print("precision:",precision/50)
print("recall:",recall/50)
print("f1score:",f1score/50)

endtime = time.time()
usetime=endtime-starttime;
print(usetime)

