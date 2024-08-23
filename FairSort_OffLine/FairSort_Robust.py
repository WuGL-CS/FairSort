import csv
import time
from FairSort_Offline import  FairSortForTheWhole as FairSortForTheWhole
import pandas as pd
import numpy as np

def SaveResult_WriteTitle_Offline_Robust(dataset_name,qualityOrUniform):
    if qualityOrUniform==0:
        fileName="/FairSort_Robust(threadhold)_QF"+".csv"
    else:
        fileName = "/FairSort_Robust(threadhold)_UF" + ".csv"
    csvFile = open("../results_Robust/threadhold_Robust/" + dataset_name + fileName
                   , 'w', newline='')
    writer = csv.writer(csvFile)
    title = []
    title.append('k')
    title.append('satisfaction_var')
    title.append('satisfaction_diverse')
    title.append('satisfaction_total')
    if(qualityOrUniform==0):
        title.append('Top-k_qualityVar')
        title.append('exposure_quality_var')
        title.append('exposure_quality_diverse')
    elif(qualityOrUniform==1):
        title.append('Top-k_SizeVar')
        title.append('exposure_var')
        title.append('exposure_diverse')
    title.append('fair_VarAtFirst')
    title.append('fair_Var')  # 公平要求下的方差值：越小越好，说明地整的越平
    title.append("Top-K转化率分布")
    title.append("FairSort转化率分布")
    title.append("公平曝光资源分布")
    title.append("Top-K曝光err")
    title.append("FairSort曝光err")
    title.append("提供商物品数分布")
    title.append("提供商价值量分布")
    title.append("Threadhold")
    writer.writerow(title)
    return csvFile

def testFairSortRobust_Offline(userList, λ, score, sorted_score, ratio, K, Robust_direc, gap, item_provider,
                                      providerIndex,
                                      qualityOrUniform,force, dataset_name,writer):

        for low_bound in Robust_direc:
            row = FairSortForTheWhole(userList, λ, score, sorted_score, ratio, K, low_bound, gap, item_provider,
                                      providerIndex,
                                      qualityOrUniform, force, dataset_name)
            row.append(low_bound)
            writer.writerow(row)

def Run_TestRobust(dataSetName,FairType,Robust_direc):
    k = 25
    λ = 128
    if dataSetName=="amazon":


        user_number_amazon = 1851
        m = user_number_amazon

        dataset_name = 'amazon'
        score_file = '/preference_score.csv'
        item_file = '/item_provider.csv'

        item_provider = pd.read_csv('../datasets/data_' + dataset_name + item_file)
        # item_provider = np.array(item_provider.values)
        w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file,
                              header=None)  # 这里有错误，为什么连文件的socre名还引错，写成result.csv

        # 对分数矩阵进行归一化操作
        score = np.array(w_score.values)
        for index in range(len(score)):
            score[index] = (score[index] / (max(score[
                                                    index]) * 100))  # this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
            # and the NDCG ,which can be proof strictly!

        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))

            # hyperParameter


        ratio = 0.1

        gap = 1 / 32
        userList = [i for i in range(m)]  # userList的构造
        # save result analyze

        csvFile = SaveResult_WriteTitle_Offline_Robust(dataset_name, FairType)
        writer = csv.writer(csvFile)
        t = time.time()
        testFairSortRobust_Offline(userList,λ,score,sorted_score,ratio,k,Robust_direc,gap,item_provider
                                   ,"provider",FairType,0.1,dataset_name,writer)

        print(f'Time spent:{time.time() - t:.3f}s')

        csvFile.close()
        print('Finished!')
    elif dataSetName=="google":
        review_number_google = 97658
        item_number_google = 4927
        user_number_google = 3335
        provider_num_google = 4927

        m = user_number_google
        n = item_number_google
        provider_num = provider_num_google


        score_file = '/preference_score.csv'
        item_file = '/item_provider.csv'

        item_provider = pd.read_csv('../datasets/data_' + dataSetName + item_file)
        # item_provider = np.array(item_provider.values)
        w_score = pd.read_csv('../datasets/data_' + dataSetName + score_file,
                              header=None)  # 这里有错误，为什么连文件的socre名还引错，写成result.csv

        # 对分数矩阵进行归一化操作
        score = np.array(w_score.values)
        for index in range(len(score)):
            score[index] = (score[index] / (max(score[
                                                    index]) * 1000))  # this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
            # and the NDCG ,which can be proof strictly!

        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))

            # hyperParameter

        ratio = 0.15

        gap = 1 / 64

        userList = [i for i in range(m)]  # userList的构造
        # save result analyze
        # 命名一个函数名，并且把文件创建好，把title
        # 给写好，给你返回文件的对象
        csvFile = SaveResult_WriteTitle_Offline_Robust(dataSetName, FairType)
        writer = csv.writer(csvFile)
        t = time.time()
        testFairSortRobust_Offline(userList, λ, score, sorted_score, ratio, k, Robust_direc, gap, item_provider
                                   , "provider", FairType, 0.1, dataSetName, writer)

        print(f'Time spent:{time.time() - t:.3f}s')

        csvFile.close()
        print('Finished!')
    elif dataSetName=="ctrip":
        o_num_international = 25190
        u_num_international = 3814
        t_num_international = 6006

        m = u_num_international
        # m = 100
        n = t_num_international
        # n = 50

        dataset_name = 'ctrip'
        score_file = '/score_international.csv'
        item_file = '/ticket_international.csv'
        # ticket_list:订单表：ID airline classes price
        item_provider = pd.read_csv('../datasets/data_' + dataset_name + item_file)
        # 用户和item的贡献矩阵：评分矩阵
        w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file)
        # 评分矩阵score
        w_score = w_score.iloc[:, 3:]
        score = np.array(w_score)
        score = score[:m, :n]
        # 对分数矩阵进行归一化操作
        score = np.array(w_score.values)
        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))
        sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表
        userList = [i for i in range(m)]  # userList的构造
        # hyperParameter

        ratio = 1

        gap = 1 / 64

        # save result analyze

        csvFile = SaveResult_WriteTitle_Offline_Robust(dataset_name, FairType)
        writer = csv.writer(csvFile)
        t = time.time()
        testFairSortRobust_Offline(userList,λ,score,sorted_score,ratio,k,Robust_direc,gap,item_provider
                                   ,"airline",FairType,0.1,dataset_name,writer)

        print(f'Time spent:{time.time() - t:.3f}s')

        csvFile.close()
        print('Finished!')



if __name__ == '__main__':
    Run_TestRobust("ctrip",1,[1,0.95,0.9,0.85])
