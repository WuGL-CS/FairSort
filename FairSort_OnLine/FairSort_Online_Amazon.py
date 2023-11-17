import  numpy as np
import pandas as pd
from FairSort_OffLine import FairSort_Utils as Utils
from FairSort_OnLine import FairSort_Online
import csv as csv
import  time


if __name__ == '__main__':
    review_number_amazon = 24658
    item_number_amazon = 7538
    user_number_amazon = 1851
    provider_num_amazon = 161

    m = user_number_amazon
    # m = 100
    n = item_number_amazon
    # n = 50

    dataset_name = 'amazon'
    score_file = '/preference_score.csv'
    item_file = '/item_provider.csv'
    # ticket_list:订单表：ID airline classes price
    item_ProducerList = pd.read_csv('../datasets/data_' + dataset_name + item_file)
    # 用户和item的贡献矩阵：评分矩阵
    w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file,header=None)
    # 评分矩阵score
    score = np.array(w_score)
    score = score[:m, :n]
    # 对分数矩阵进行归一化操作
    score = np.array(w_score.values)
    # score_true=np.copy(score)
    for index in range(len(score)):
        score[index] = (score[index] / (max(score[index]) * 100))#this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
        #and the NDCG ,which can be proof strictly!

    sorted_score = []
    for i in range(len(score)):
        sorted_score.append(np.argsort(-score[i]))
    sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表
    user_Random=Utils.load_variavle("../datasets/data_amazon/random_user.pkl")
    #hyperParameter
    K=20
    λ=1
    ratio=0.1
    low_bound=0.95
    gap=1/256
    qualityOrUniform = 0  # Fair appeal: 0 is Quality and 1 is Uniform
    # save result analyze
    csvFile=Utils.SaveResult_WriteTitle_Online(dataset_name,qualityOrUniform,λ,ratio,low_bound)
    writer=csv.writer(csvFile)
    t=time.time()
    FairSort_Online.FairSortOnLine(λ,ratio,gap,low_bound,K,score,sorted_score,qualityOrUniform,user_Random,item_ProducerList,"provider",writer,dataset_name)
    print(f'Time spent:{time.time() - t:.3f}s')
    csvFile.close()
    print('Finished!')