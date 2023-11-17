import csv
import time
from FairSort_Offline import  FairSortForTheWhole as FairSortForTheWhole
import pandas as pd
import numpy as np
from FairSort_OffLine import  FairSort_Utils as Utils

if __name__ == '__main__':


    review_number_amazon = 24658
    item_number_amazon = 7538
    user_number_amazon = 1851
    provider_num_amazon = 161

    review_number_google = 97658
    item_number_google = 4927
    user_number_google = 3335
    provider_num_google = 4927

    m = user_number_google
    n = item_number_google
    provider_num = provider_num_google

    k = 25
    dataset_name = 'google'
    score_file = '/preference_score.csv'
    item_file = '/item_provider.csv'

    item_provider = pd.read_csv('../datasets/data_' + dataset_name + item_file)
    # item_provider = np.array(item_provider.values)
    w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file, header=None)#这里有错误，为什么连文件的socre名还引错，写成result.csv

    #对分数矩阵进行归一化操作
    score = np.array(w_score.values)
    for index in range(len(score)):
        score[index]= (score[index]/(max(score[index])*1000))#this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
        #and the NDCG ,which can be proof strictly!

    sorted_score = []
    for i in range(len(score)):
        sorted_score.append(np.argsort(-score[i]))

        # hyperParameter
    λ = 8
    ratio = 0.15
    low_bound = 0.9
    gap = 1/64
    qualityOrUniform = 0  # Fair appeal: 0 is Quality and 1 is Uniform
    userList = [i for i in range(m)]  # userList的构造
    # save result analyze
    #命名一个函数名，并且把文件创建好，把title
    # 给写好，给你返回文件的对象
    csvFile = Utils.SaveResult_WriteTitle_Offline(dataset_name, qualityOrUniform, λ, ratio, low_bound)
    writer = csv.writer(csvFile)
    t = time.time()
    for K in range(2,26):
        FairSortForTheWhole(userList, λ, score, sorted_score, ratio, K, low_bound, gap, item_provider, "provider",
                        qualityOrUniform, 0.1,dataset_name,
                        writer)  # （λ=128,ratio=1,K=23, low_bound=0.85，gap=1/256，force=0.1）+left+linearRate1
    print(f'Time spent:{time.time() - t:.3f}s')

    csvFile.close()
    print('Finished!')