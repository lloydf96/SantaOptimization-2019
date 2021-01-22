# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:02:03 2019

@author: ABC
"""
import numpy as np
import pandas as pd
import math as m
global familyChoice,choicePenalty,familyCount,obj,subject,binary,general

class SantaOptimization ():
    

    def readTrainingData(self):
        data=pd.read_csv('family_data.csv')
    
        self.familyChoice=data.drop(columns=['n_people'])
        self.familyChoice.loc[:,self.familyChoice.columns != 'family_id']=\
        self.familyChoice.loc[:,self.familyChoice.columns != 'family_id'].astype(int)
        self.familyChoice=self.familyChoice.set_index('family_id')
        
        data1 = pd.read_csv('penalty_rule.csv')
        self.choicePenalty = data1
        self.familyCount=data.loc[:,['family_id','n_people']]
        self.familyCount=self.familyCount.set_index('family_id')
        
        
        self.choicePenalty=self.choicePenalty.set_index('choice_ID')
        
        self.familyPenalty=self.familyChoice.copy()
        self.familyPenalty['choice_10']=np.nan
        
        for i,row in self.familyPenalty.iterrows():
            for i1,element in row.iteritems():
                self.familyPenalty.loc[i,i1]=self.choicePenalty.loc[i1,'fixedCost']+self.choicePenalty.loc[i1,'variableCost']*self.familyCount.loc[i,'n_people']
         
        self.accPenalty=pd.DataFrame(columns=list(range(125,301)))
        
        for i in range(125,301):
            a=pd.Series(i1 for i1 in list(range(125,301))).apply(lambda x: self.CalcAccountingCost(i,x))
            a.name=i
            a.index=list(range(125,301))
            self.accPenalty.loc[i]=a
         
            
    def testData(self):
        self.familyCount=self.familyCount.head(self.rowCount)
        self.familyChoice=self.familyChoice.head(self.rowCount)
        self.familyPenalty=self.familyPenalty.head(self.rowCount)
     
    @staticmethod
    def CalcAccountingCost(N1,N2):
        
        acc = m.floor(((N1-125)/400)*N1**(0.5+(abs(N1-N2)/50)))
        return int(acc)
   
    def writeProblemFile(self):
        self.obj="\n Maximize \n"
        self.subject="\n Subject to \n"
        self.general="\n General \n"
        self.binary="\n Binary \n"
        self.subject1="\n"
        self.subject2="\n"
        self.subject3="\n"
        
        days=list(range(1,101))
        
        self.subject+="\\\\Family to be assigned one day only \n"
        for i,row in self.familyChoice.iterrows():
            for i1,element in row.iteritems():
                self.obj+= " - "+str(self.familyPenalty.loc[i,i1])+" F"+str(i)+"D"+str(element)
                self.binary+= " F"+str(i)+"D"+str(element)+ "\n"
                
            x1 = [x for x in days if x not in list(row)]
            for i2 in x1:
                self.obj+= " - "+str(self.familyPenalty.loc[i,'choice_10'])+" F"+str(i)+"D"+str(i2)
                self.binary+= " F"+str(i)+"D"+str(i2)+ "\n"
            
        
            for i1 in days:
                self.subject+= " + F"+str(i)+"D"+str(i1)
            
                
            self.subject+= " = 1 \n"
            self.obj+= "\n"
            
        for i in days:
            for i1,row in self.familyCount.iterrows():
                self.subject+=" + "+str(row.loc['n_people'])+" F"+str(i1)+"D"+str(i)
            self.subject+= " - N"+str(i)+" = 0\n"
            
            self.subject1+= " + N"+str(i)+" <= 300\n"
         
            self.subject1+=" + N"+str(i)+" >= 125\n"
            
        for i2 in days:       
            for i in range(125,301):
                
                self.subject3+= " N"+str(i2)+" - "+str(i)+" <= + 10000 - 10000 N"+str(i2)+"V"+str(i)+"\n"
                self.subject3+= " N"+str(i2)+" - "+str(i)+" >= - 10000 + 10000 N"+str(i2)+"V"+str(i)+"\n"
                
                for i1 in range(125,301):
                    if self.
          
                    self.subject2+=" 1000 (2 - N"+str(i2)+"V"+str(i)+" - N"+str(i2+1)+"V"+str(i1)+") + N"+str(i2)+"V"+str(i)+"N"+str(i2+1)+"V"+str(i1)+" >= 1\n"
                    self.obj+= " - "+str(self.accPenalty.loc[i,i1])+ " N"+str(i2)+"V"+str(i)+"N"+str(i2+1)+"V"+str(i1)
          
        self.obj+= "\n"
        self.subject+=self.subject1
        self.subject+=self.subject2
        self.subject+=self.subject3
        
    def tempPrint(self):
        days=list(range(1,101))
        
        self.subject2="\n"
        self.obj="\n"
               
        for i in days:
           
            if i<100 :
                self.subject2+=" +  N"+str(i+1)+" - N"+str(i)+" - NA"+str(i)+" + NB"+str(i)+" = 0\n"
                
                self.obj+= " - 1000000000 NA"+str(i)+" - 1000000000 NB"+ str(i)
                
        file = open("Problem1.lp","w") 
        
        file.write(self.obj+"\n\n\n")
        file.write(self.subject2) 
             
    
    def printProblemFile(self):
        file = open("Problem1.lp","w") 
        file.write(self.obj)
        file.write(self.subject)
        file.write(self.binary)
        file.write(self.general)
        
        
        
        
    
    
            
            
            
                
                
                
            
                
                
        
        












