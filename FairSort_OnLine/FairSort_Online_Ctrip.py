import  numpy as np
import pandas as pd
from FairSort_OffLine import FairSort_Utils as Utils
from FairSort_OnLine import FairSort_Online
import csv as csv
import  time


if __name__ == '__main__':
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
    item_ProducerList = pd.read_csv('../datasets/data_' + dataset_name + item_file)
    # 用户和item的贡献矩阵：评分矩阵
    w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file)
    # 评分矩阵score
    w_score = w_score.iloc[:, 3:]
    score = np.array(w_score)
    score = score[:m, :n]
    # 对分数矩阵进行归一化操作
    score = np.array(w_score.values)
    score_true=np.copy(score)
    for index in range(len(score)):
        score[index] = (score[index] / (max(score[index]) * 10))

    sorted_score = []
    for i in range(len(score)):
        sorted_score.append(np.argsort(-score[i]))
    sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表
    user_Random=Utils.load_variavle("../datasets/data_ctrip/random_user.pkl")
    #hyperParameter
    K=20
    λ=8
    ratio=1
    low_bound=0.9
    gap=1/256
    qualityOrUniform = 0  # 公平诉求：0则为Quality  1 则为Uniform
    # save result analyze
    csvFile=Utils.SaveResult_WriteTitle_Online(dataset_name,qualityOrUniform,λ,ratio,low_bound)
    writer=csv.writer(csvFile)
    t=time.time()
    FairSort_Online.FairSortOnLine(λ,ratio,gap,low_bound,K,score,sorted_score,qualityOrUniform,user_Random,item_ProducerList,"airline",writer,score_truth=score_true)
    print(f'时间差:{time.time() - t:.3f}s')
    csvFile.close()
    print('Finished!')