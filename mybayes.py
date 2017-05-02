import pandas as pd
import numpy as np
import math

class bayes:
    def __init__(self):
        self.test = 0;
        self.positive = 0
        self.negative = 0
        self.poslist = {}
        self.neglist = {}

    def judge(self,ma,k=0.01):
        pos = self.positive / (self.positive + self.negative);
        neg = self.negative / (self.positive + self.negative);
        for key in ma.keys():
            value = ma[key]
            values = len(self.poslist[key].keys())
            pc = 0;
            if value in self.poslist[key]:
                pc = self.poslist[key][value]
            pos *= (pc + k) / (self.positive + k *values)
            nc = 0;
            if value in self.neglist[key]:
                nc = self.neglist[key][value]
            neg *= (nc + k) / (self.negative + k *values)
 
        if (pos>neg):
            return 1
        else:
            return 0

    def judgeData(self,df, namelist, resultname,indexlist):
        ans=[0,0,0,0]
        for index in indexlist:
            ma={}
            for name in namelist:
                
                ma[name]=df[name][index]
            result = self.judge(ma)
            trueresult=df[resultname][index]
            if (trueresult==1):
                if (result==1):
                    ans[0]+=1
                else:
                    ans[2]+=1
            else:
                if (result==1):
                    ans[1]+=1
                else:
                    ans[3]+=1

        return ans;

    def judgeError(self, df, namelist, resultname,indexlist):
        match = [];
        miss = [];
        for index in indexlist:
            ma={}
            for name in namelist:
                ma[name]=df[name][index]
            result = self.judge(ma)
            trueresult=df[resultname][index]
            if (result==trueresult):
                match.append(index)
            else:
                miss.append(index)
        return match,miss

    def getResult(self, df, namelist, resultname,indexlist):
        ans = [];
        for index in indexlist:
            ma={}
            for name in namelist:
                ma[name]=df[name][index]
            result = self.judge(ma)
            ans.append(result);
        return ans;

def buildmodel(df,namelist,resultname,indexlist):
    mybayes = bayes();
    for name in namelist:
        mybayes.poslist[name]={};
        mybayes.neglist[name]={};
    for i in indexlist:
        
        if df[resultname][i]==1:
            mybayes.positive+=1
            for name in namelist:
                posmap = mybayes.poslist[name];
                negmap = mybayes.neglist[name];
                if df[name][i] in posmap:
                    posmap[df[name][i]] += 1
                else:
                    posmap[df[name][i]] = 1
                if not(df[name][i] in negmap):
                    negmap[df[name][i]] = 0;


        else:
            mybayes.negative+=1
            for name in namelist:
                posmap = mybayes.poslist[name];
                negmap = mybayes.neglist[name];
                if df[name][i] in negmap:
                    negmap[df[name][i]] += 1
                else:
                    negmap[df[name][i]] = 1
                if not(df[name][i] in posmap):
                    posmap[df[name][i]] = 0;

    return mybayes
