import pandas as pd
import numpy as np
import math
class node:
    def __init__(self):
        self.list = {};
        self.leaf = False;
        self.judge = -1;
        self.attribute = '';
        self.percent=-1;

    def addchild(self,key,newnode):
        self.list[key]=newnode;

def subentropy(l):
    if l[0]==0 or l[1]==0:
        return 0,l[0]+l[1];
    sub1 = l[0]/(l[0]+l[1])
    sub2 = l[1]/(l[0]+l[1])

    return -sub1*math.log(sub1,2)-sub2*math.log(sub2,2),l[0]+l[1]

def entropy(df,name,resultname,indexlist):
    total = len(indexlist)
    entro=0;
    ma = {};
    for index in indexlist:
        i = df[name][index];
        result = df[resultname][index]
        if i in ma:
            ma[i][result]+=1
        else:
            ma[i] = [0,0]
            ma[i][result]+=1;
    for i in ma.keys():
        sube,subt = subentropy(ma[i])
        entro += subt / total * sube;
    return entro;

def makesubtree(df,namelist,resultname,indexlist):
    mynode = node()
    judge = -1;
    pos=0;
    neg=0;
    for index in indexlist:
        t = df[resultname][index]
        if t==1:
            pos+=1
        else:
            neg+=1;

    mynode.percent = pos / (pos+neg)
    
    if (pos*neg==0):
        mynode.leaf = True
        mynode.judge = t
        
        return mynode;
    
    min=32767
    for name in namelist:
        val = entropy(df,name,resultname,indexlist)
        if val<min:
            
            min = val
            ans = name
    if (min==32767):
        mynode.leaf = True
        if (pos>=neg):
            mynode.judge = 1;
        else:
            mynode.judge
        
        return mynode
    ma = {}
    mynode.attribute = ans;
    
    for index in indexlist:
        i = df[ans][index]
        result = df[resultname][index]
        if i in ma:
            ma[i].append(index)
        else:
            ma[i]=[]
            ma[i].append(index)
    namelist.remove(ans)
    for key in ma.keys():
        mynode.addchild(key,makesubtree(df,namelist,resultname,ma[key]))
            
    namelist.append(ans)
    return mynode;
#def maketree(df,namelist,resultname):
    

def walk(root,s):
    if (root.leaf):
        print(s,root.judge,root.percent)
    else:
        print(s,root.percent)
        for key in root.list.keys():
            walk(root.list[key],s+" ")

def judge(node,ma):


    if node.leaf:
        return node.judge;
    else:
        try:
            return judge(node.list[ma[node.attribute]],ma);
        except KeyError:
            return node.percent > 0.5;
    
def judgeData(node, df, namelist, resultname,indexlist):
    ans=[0,0,0,0]
    for index in indexlist:
        ma={}
        for name in namelist:
            ma[name]=df[name][index]
        result = judge(node,ma)
        trueresult=df[resultname][index]
        if (trueresult==1):
            if (result):
                ans[0]+=1
            else:
                ans[2]+=1
        else:
            if (result):
                ans[1]+=1
            else:
                ans[3]+=1

    return ans;




