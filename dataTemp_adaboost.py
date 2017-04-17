
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
import wr
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
        if name!='id':
            ma.append(name);

print(ma)

accuracy = 0.0
precision = 0.0
recall = 0.0
f1score = 0.0

indexlist=[];
weightlist=[];
for i in range(len(data_example)):
    indexlist.append(i)
    weightlist.append(1.0)

random.shuffle(indexlist)
size = len(indexlist)
datatotrain  = [];

for i in range(len(data_example)):
    datatotrain.append(-1);
for kk in range(10):

    train = []
    test = []
    print(kk)
    print(size)
    for i in range(size):
        if (i >= kk * size/10) and ( i <=(kk+1)*size/10):
            test.append(indexlist[i])
        else:
            train.append(indexlist[i])
    weightlist=[];
    for i in range(len(train)):
        weightlist.append(1.0/len(train))
        datatotrain[train[i]]=i;
    learner = [];
    beta = [];
    #train
    for j in range(5):
        rand = wr.wr(weightlist);
        trainindex = [];
        trainset = [];
        for k in range(500):
            s = rand.next()
            if (s>=len(train)) or (s in trainindex):
                continue;
            trainindex.append(s);
            trainset.append(train[s])
        mynode=decision.makesubtree(data_example,ma,'bot',trainset);
        match,miss = decision.judgeError(mynode,data_example,ma,'bot',train);
        error = 0;
        for fail in miss:
            error += weightlist[datatotrain[fail]]
        if (error > 0.5):
            break;
        learner.append(mynode);
        beta.append(error / (1-error));
        for tr in match:
            weightlist[datatotrain[tr]] *= beta[-1]
        sum = 0;
        for i in weightlist:
            sum+=i;
        for i in range(len(weightlist)):
            weightlist[i]/=sum;
        print(error);
    #test
    sum = 0
    tp=0
    fp=0
    fn=0
    tn=0
    result = [];
    for lea in learner:
        result.append(decision.getResult(lea,data_example,ma,'bot',test))
    rs=[];
    for i in range(len(test)):
        total = 0;
        rs.append(0);
        for j in range(len(learner)):
            total += 1;
            if result[j][i]==1:
                rs[-1]+= math.log(1/beta[j],2);
            else:
                rs[-1]-= math.log(1/beta[j],2);
        if rs[-1]>0:
            rs[-1]=1;
        elif rs[-1]<0:
            rs[-1]=0;
        elif i % 2 ==0:
            rs[-1]=1
        else:
            rs[-1]=0
    for i in range(len(test)):
        if rs[i]==1:
            if data_example['bot'][test[i]]==1:
                tp+=1;
            else:
                fp+=1
        else:
            if data_example['bot'][test[i]]==1:
                fn+=1
            else:
                tn+=1;
                
    print(tp,' ',fp,' ',fn,' ',tn)
    accuracy += (tp+tn)/len(test)
    precise = tp/(tp+fp)
    recal = tp/(tp+fn)
    precision += precise
    recall+=recal
    f1score+=2*(1/((1/precise)+(1/recal)))
print("accuracy:",accuracy/10)
print("precision:",precision/10)
print("recall:",recall/10)
print("f1score:",f1score/10)

endtime = time.time()
usetime=endtime-starttime;
print(usetime)

