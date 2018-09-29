#--*- coding:utf-8 -*-
import os

file = open("acsi_postids.txt")             # 返回一个文件对象
fileidl = []
postidl = []
for line in file.readlines():
    line=line.strip('\n')
    l = line.split(':')
    fileid = l[0]
    both = l[1].split('_')
    postid = both[-1]
    fileidl.append(fileid)
    postidl.append(postid)
    #print(fileid,postid)
#print(fileidl,postidl)
with open('acsi_postid.txt','w') as f:
    for i in range(len(postidl)):
        fileid = fileidl[i]
        postid = postidl[i]
        f.write(fileid+'  '+postid+'\n')
        print(fileid,postid)

file.close()





