# -*- coding: UTF8 -*-

import time
import datetime

import os

file_dir= '/Users/mia/Desktop/now we have asci'

import os

def file_name(file_dir):
    filec = []
    for root, dirs, files in os.walk(file_dir):
        #print(0,root)  # 当前目录路径
       # print(1,dirs)  # 当前路径下所有子目录

        for file in files:
            file = file.split('.')[0]
            file = file.replace('_','  ')
            filec.append(file)
    return filec
    #print(filec)


postwehave = file_name(file_dir)
file = open("/Users/mia/PycharmProjects/facebook/acsi_postid.txt")
all = []
for line in file.readlines():
    line = line.strip('\n')
    all.append(line)
needtol = [x for x in all if x not in postwehave]
#print(needtol)
with open('needtorun.txt','w') as f:
    for i in needtol:
        f.write(i)
        f.write('\n')
