import random

import numpy
import numpy as np
import pickle as pickle
# score=[[1,2,3],[21,3,5]]
# score=numpy.array(score)
# score_sock=[]
# # score_sock=numpy.array(score_sock)
# print(len(score))
# for i in range(len(score)):
#     score_sock.append(np.argsort(-score[i]))
#
# print(score_sock)
# print(type(score_sock[0]))
# def save_variable(v,filename):
#   f=open(filename,'wb')          #打开或创建名叫filename的文档。
#   pickle.dump(v,f)               #在文件filename中写入v
#   f.close()                      #关闭文件，释放内存。
#   return filename
#
#
# def load_variavle(filename):
#
#         f = open(filename, 'rb+')
#         r = pickle.load(f)
#         f.close()
#         return r
#
#
# file_Name = 'datasets/Temp_Value/TFROM_ctrip_provider_quality.pkl'
# arr=[14,21]
# arr2=[212,12]
# name=save_variable(arr,file_Name)
# name=save_variable(arr2,file_Name)
# print(name)
# pick=open(file_Name,"rb+")
# arr1=pickle.load(pick)
# arr2=pickle.load(pick)
#
# print(arr1) rank_user_satisfaction.sort(key=lambda x: user_satisfaction[x], reverse=True)
# # print(arr2)
# arr=[0,0,0,0]
# arr2=[temp for temp in range(len(arr))]
# print(arr2)
# random.shuffle(arr2)
# print(arr2)
# arr2.sort(key=lambda x:arr[x],reverse=True)
# print(arr2)
# arr=[[2,4,6],[2,4,6]]
# arr=[arr[i][0:2] for i in range(2)]
#
# print(arr)
a=53*49069
for i in range(1,a+1):
    if(a%i==0):
        print(i)