import pandas as pd
import numpy as np
import math
import dateutil.parser as dparser
import mybayes
import random
import decision


data_bot = pd.read_csv('data/bots_data.csv', encoding='iso-8859-1')
data_nonbot = pd.read_csv('data/nonbots_data.csv', encoding='iso-8859-1')
data_combine = data_bot
data_combine = data_combine.append(data_nonbot, ignore_index=True)

indexlist=[]

for i in range(len(data_combine)):
    indexlist.append(i)

trainmap={}
testmap={}
for name in data_combine.columns:
    trainmap[name]=[];
    testmap[name]=[]

trainid=[]
testid=[]
i=0;
for idnex in range(len(data_combine)):
    if (idnex>=len(data_bot)-200 and idnex<len(data_bot)+200):
        continue;
    trainid.append(i)
    for name in data_combine.columns:
        trainmap[name].append(data_combine[name][indexlist[idnex]]);
    i=i+1
print(len(trainid))
i=0;
for i in range(400):
    testid.append(i)
    for name in data_combine.columns:
        testmap[name].append(data_combine[name][indexlist[len(data_bot)-200+i]]);


    
sData_train = pd.DataFrame(index=trainid,columns=data_combine.columns);
for name in data_combine.columns:
    sData_train[name]=trainmap[name];
    
sData_test = pd.DataFrame(index=testid,columns=data_combine.columns);
for name in data_combine.columns:
    sData_test[name]=testmap[name];

print(len(sData_train))

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
labelStr = 'bot'

#data_Train = pd.DataFrame(np.random.randn(len(sData_train.index), 2),columns=['description', labelStr])    
#counter = 0
#for idx in np.random.choice(len(sData_train.index), len(sData_train.index)):
#    value = sData_train['description'][idx]
#    if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
#        abc=1;
#    else:
#        data_Train.loc[counter,'description'] = str(value)
#        data_Train.loc[counter,labelStr] = sData_train[labelStr][idx]
#        counter = counter+1

#print("start")
clf=["",""]
def checkBayesWords(data_source, data_class, attrstr, isBernoulli, indexOfC):
    global clf
    #return two class: 1/0/2 as bot or not bot or nan
    #Train a model and return predict result for both train and test set
    data_class[attrstr]=0
    doc = []
    target = [] 
    countertrain = 0
    countertest = 0
    for idx in range(len(sData_train)):
        value = sData_train[attrstr][idx]
        if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
            continue
        else:
            doc.append(str(value))
            target.append(sData_train[labelStr][idx])
            countertrain = countertrain+1
    for idx in range(len(sData_test)):
        value = sData_test[attrstr][idx]
        if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
            continue
        else:
            doc.append(str(value))
            target.append(sData_test[labelStr][idx])
            countertest = countertest+1
    #train
    count_vect = CountVectorizer()
    X_counts = count_vect.fit_transform(doc)
    X_train_counts = X_counts[0:countertrain];
    X_test_counts = X_counts[countertrain:countertrain+countertest];
    train_target = target[0:countertrain];
    test_target = target[countertrain:countertrain+countertest];

    if (clf[indexOfC] == ""):
    
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        if(isBernoulli == True):
            clf[indexOfC] = BernoulliNB().fit(X_train_tfidf, train_target)
        else:
            clf[indexOfC] = MultinomialNB().fit(X_train_tfidf, train_target)
        predictss = clf[indexOfC].predict(X_train_tfidf)
        print(len(predictss));
        print(len(data_source))
    #predict
    #data_Test = pd.DataFrame(np.random.randn(len(sData_test.index), 1),columns=[attrstr])
    #data_Test = data_combine[[attrstr]].copy(deep=True)
    #counter = 0
        cc = 0;
        for idx in range(len(data_source)):
            value = data_source[attrstr][idx]
            if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
                #data_Test[attrstr][counter] = "NaN NaN"
                data_class.loc[idx,attrstr] = 2
            else:
                #data_Test[attrstr][counter] = value
                #counter = counter+1
                data_class.loc[idx,attrstr] = predictss[cc]
                cc+=1;
        print(cc)
    else:
        tfidf_transformer = TfidfTransformer()
        X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)
        predictss = clf[indexOfC].predict(X_test_tfidf)
        print(len(predictss))
        print(len(data_source))
        cc = 0;
        for idx in range(len(data_source)):
            value = data_source[attrstr][idx]
            if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
                #data_Test[attrstr][counter] = "NaN NaN"
                data_class.loc[idx,attrstr] = 2
            else:
                #data_Test[attrstr][counter] = value
                #counter = counter+1
                data_class.loc[idx,attrstr] = predictss[cc]
                cc+=1;
        print(cc)


        
    #newdoc = data_Test.loc[:,(attrstr)][0:len(data_Test.index)-1]
    #X_new_counts = count_vect.transform(newdoc)
    #X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    #predicted = clf.predict(X_new_tfidf)
    #print(predicted)
    #idx = 0
    #data_class[attrstr]=0
    #for flag in predicted:
    #    data_class[attrstr][idx] = flag
    #    idx=idx+1
def checkNone(data_source, data_class, attrstr):
    #return two class: 1/0
    #None:1    not-None:0
    data_class[attrstr]=0
    idx = 0
    for value in data_source[attrstr]:
        if value == "" or value == "None" or value == "\"\"" or value == "null" or pd.isnull(value):
            data_class.loc[idx,attrstr] = 1
        idx += 1

def checkTF(data_source, data_class, attrstr):
    #return two class: 1/0
    #True:0    False:1
    data_class[attrstr]=0
    idx = 0
    print('total',len(data_source))
    count=0;
    for value in data_source[attrstr]:
        v = value
       
        if (type(value)==str):
            if value == "TRUE" or value == 'true':
                v=True
            else:
                v=False
        if (idx==1):
            print(type(v))
        if v == False:
            data_class.loc[idx,attrstr] = 1
        else:
            count+=1
        idx += 1
    print('c',count)

def checkNumber(data_source, data_class, attrstr, effi):
    #return n=log with base-effi 0:non-int type
    data_class[attrstr]=0
    idx = 0
    for value in data_source[attrstr]:
        if (idx==0):
            print(type(value))
        v = value;
        if type(v) is str:
            try:
                v = int(v)
            except ValueError:
                v = 0;
        if type(v) is np.int64:
            if effi == 10:
                data_class.loc[idx,attrstr] = int(math.log10(v+1))
            elif effi == 2:
                data_class.loc[idx,attrstr] = int(math.log2(v+1))
            else:
                data_class.loc[idx,attrstr] = int(math.log(v+1, effi))
        else:
            data_class.loc[idx,attrstr]=0
        
        idx += 1

def checkEnglish(data_source, data_class, attrstr):
    #return isEnglish:1    other:...
    data_class[attrstr]=0
    idx = 0
    for value in data_source[attrstr]:
        if value == "en":
            data_class.loc[idx,attrstr] = 1
        elif value == "fr":
            data_class.loc[idx,attrstr] = 2
        elif value == "ja":
            data_class.loc[idx,attrstr] = 3
        elif value == "ko":
             data_class.loc[idx,attrstr] = 4
        idx += 1

def checkDate(data_source, data_class, attrstr):
    #date index:
    #    year<=2012: 0:3
    #    year==2013: 4:7
    #    year==2014: 8:11
    #    year==2015: 12:15
    #    year==2016: 16:19
    #    year==2017: 20:23
    data_class[attrstr]=0
    idx = 0
    for value in data_source[attrstr]:
        times =0;
        try:
            y = dparser.parse(value,fuzzy=True).year
            m = dparser.parse(value,fuzzy=True).month
            if y ==2013:
                times = 4
            elif y == 2014:
                times = 8
            elif y == 2015:
                times = 12
            elif y == 2016:
                times = 16
            elif y == 2017:
                times = 20
        #month
            if m>6:
                times+= 1
        except TypeError:
            times=24
        data_class.loc[idx,attrstr]=times
        idx += 1

botDict = ["bot",
           "Bot",
           "robot",
           "Robot"]

def checkStringBot(data_source, data_class, attrstr):
    #return has sub string in botDict:1     else:0    typeError:2
    data_class[attrstr]=0
    idx = 0
    for value in data_source[attrstr]:
        if type(value) is str:
            for dic in botDict:
                if value.find(dic) != -1:
                    data_class.loc[idx,attrstr] = 1
        else:
            data_class.loc[idx,attrstr] = 2
        idx += 1

def DataFrameFilter(dataSource):
    data_class = dataSource[['bot']].copy(deep=True)
    attrList = dataSource.columns.values
    for attrStr in attrList:
        if attrStr == "id":
            checkNumber(dataSource, data_class, attrStr, 10)
            print(attrStr)
        
        elif attrStr == "id_str":
            print(attrStr)
        
        elif attrStr == "screen_name":
            checkStringBot(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "location":
            checkNone(dataSource, data_class, attrStr)
            #checkBayesWords(dataSource, data_class, attrStr, False,1)
            print(attrStr)
        
        elif attrStr == "description":
            #checkNone(dataSource,data_class, attrStr)
            checkBayesWords(dataSource, data_class, attrStr, False,0)
            print(attrStr)
        
        elif attrStr == "url":
            checkNone(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "followers_count":
            checkNumber(dataSource, data_class, attrStr, 2)
            print(attrStr)
        
        elif attrStr == "friends_count":
            checkNumber(dataSource, data_class, attrStr, 2)
            print(attrStr)
        
        elif (attrStr == "listedcount" or attrStr == "listed_count"):
            checkNumber(dataSource, data_class, attrStr, 2)
            print(attrStr)
        
        elif attrStr == "created_at":
            checkDate(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif (attrStr == "favorites_count" or attrStr=="favourites_count"):
            checkNumber(dataSource, data_class, attrStr, 2)
            print(attrStr)
        
        elif attrStr == "verified":
            checkTF(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "statuses_count":
            checkNumber(dataSource, data_class, attrStr, 2)
            print(attrStr)
        
        elif attrStr == "lang":
            checkEnglish(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "status":
            checkNone(dataSource, data_class, attrStr)
            #checkBayesWords(dataSource, data_class, attrStr, False,1)
            print(attrStr)
        
        elif attrStr == "default_profile":
            checkTF(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "default_profile_image":
            checkTF(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "has_extended_profile":
            checkTF(dataSource, data_class, attrStr)
            print(attrStr)
        
        elif attrStr == "name":
            print(attrStr)       

    return data_class


sData_test.columns = ['id', 'id_str', 'screen_name', 'location', 'description', 'url',
       'followers_count', 'friends_count', 'listedcount', 'created_at',
       'favourites_count', 'verified', 'statuses_count', 'lang', 'status',
       'default_profile', 'default_profile_image', 'has_extended_profile',
       'name', 'bot']



clf = ["",""];
data_trai = DataFrameFilter(sData_train)
data_trai.head(10)
print("123")
data_test = DataFrameFilter(sData_test)
data_test.head(10)

ma=[]
for name in data_trai.columns:
    if name!='bot' and name!='id' and name!='id_str' and name!='name':
        ma.append(name);



accuracy = 0.0
precision = 0.0
recall = 0.0
f1score = 0.0

trainindexlist=[];
import csv
testindexlist=[]
for i in range(len(data_trai)):
    trainindexlist.append(i)
i=0;

for i in range(len(data_test)):
    testindexlist.append(i)

thedatatr = [];
thedatate = [];
targettr = [];

for i in range(len(data_trai)):
    row = [];
    for name in ma:
        row.append(data_trai[name][i])
    thedatatr.append(row);
    targettr.append(data_trai['bot'][i]);
for i in range(len(data_test)):
    row = [];
    for name in ma:
        row.append(data_test[name][i])
    thedatate.append(row);

for k in range(1):
    model = mybayes.buildmodel(data_trai,ma,'bot',trainindexlist);
    result1 = model.getResult(data_test, ma, 'bot',testindexlist )
    mynode = decision.makesubtree(data_trai,ma,'bot',trainindexlist)
    result2 = decision.getResult(mynode,data_test, ma, 'bot',testindexlist )
    logreg = LogisticRegression(C=1000).fit(thedatatr, targettr)
    thetar = logreg.predict(thedatate)
    result = [];
    for i in range(len(result1)):
        t = result1[i]+result2[i]+thetar[i]
        if t>=2:
            result.append(1)
        else:
            result.append(0)
    accuracy = 0.0
    precision = 0.0
    recall = 0.0
    f1score = 0.0
    tp=0
    fp=0
    fn=0
    tn=0
    for i in range(len(result)):
        if result[i]==1:
            if data_test['bot'][i]==1:
                tp+=1;
            else:
                fp+=1;
        else:
            if data_test['bot'][i]==1:
                fn+=1;
            else:
                tn+=1;
    
    accuracy += (tp+tn)/len(result)
    precise = tp/(tp+fp)
    recal = tp/(tp+fn)
    precision += precise
    recall+=recal
    f1score+=2*(1/((1/precise)+(1/recal)))
    print("accuracy:",accuracy)
    print("precision:",precision)
    print("recall:",recall)
    print("f1score:",f1score)
    





