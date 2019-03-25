
# coding: utf-8

# In[ ]:


from __future__ import division
import os
import numpy
import csv
#from __future__ import division
count1=0
count2=0
rootdir='dis'
list=os.listdir(rootdir)
for i in range(0,len(list)):
        path = os.path.join(rootdir,list[i])
        #print(path)
        name=path.strip('dis/')
        f=open('rank','a')
        f.write(name)
        f.write(',')
        f.close()
        #print(path)
        number=0
        if os.path.isfile(path):
            count1=0
            count2=0
            count3=0
            number=0
            for line in open(path):
                number=number+1
                if (number<11):
                    lineArr=line.strip().split()
                    watch=(str(lineArr[1]))
                    #print(watch)
                    for line in open('lebellist1.csv'):
                        strlist = line.split(',', -1)
                        a=str(strlist[1])
                        a=a.strip()
                        #print (a)
                    #print (watch)
                        if a == watch:
                            count1=count1+1
                        #print(count1)
            print(count1)
            pre10=count1/10
            #print(pre10)
            pre1=str(pre10)
            rec10=count1/66
            rec1=str(rec10)
            f=open('rank','a')
            f.write(pre1)
            f.write(',')
            f.write(rec1)
            f.write(',')
            f.close()
            number=0
            for line in open(path):
                number=number+1  
                if (number<51):
                    lineArr=line.strip().split()
                    watch=(str(lineArr[1]))
                    for line in open('lebellist1.csv'):
                        strlist = line.split(',', -1)
                        a=str(strlist[1])
                        a=a.strip()
                    #print (a)
                    #print (watch)
                        if a == watch:
                           count2=count2+1
            pre20=count2/50
            rec20=count2/66
            pre2=str(pre20)
            rec2=str(rec20)
            f=open('rank','a')
            f.write(pre2)
            f.write(',')
            f.write(rec2)
            f.write(',')
            f.close()
            number=0
            for line in open(path):
                number=number+1
                if (number<151):
                    lineArr=line.strip().split()
                    watch=(str(lineArr[1]))
                    for line in open('lebellist1.csv'):
                        strlist = line.split(',', -1)
                        a=str(strlist[1])
                        a=a.strip()
                    #print (a)
                    #print (watch)
                        if a == watch:
                           count3=count3+1
            pre50=count3/150
            rec50=count3/66
            pre3=str(pre50)
            rec3=str(rec50)
            f=open('rank','a')
            f.write(pre3)
            f.write(',')
            f.write(rec3)
            f.write('\n')
            f.close()

