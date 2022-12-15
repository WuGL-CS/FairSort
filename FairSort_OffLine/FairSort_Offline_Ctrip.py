import  numpy as np
import pandas as pd
import FairSort_Utils as Utils
import csv as csv
import  time
import  FairSort_Offline as FairSort

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
    # for index in range(len(score)):
    #     score[index] = (score[index] / (max(score[index]) * 1))

    sorted_score = []
    for i in range(len(score)):
        sorted_score.append(np.argsort(-score[i]))
    sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表
    userList=[i for i in range(m)]#userList的构造
    #hyperParameter
    λ=16
    ratio=1
    low_bound=0.85
    gap=1/256
    qualityOrUniform = 1  # 公平诉求：0则为Quality  1 则为Uniform
    # save result analyze
    csvFile=Utils.SaveResult_WriteTitle(dataset_name,qualityOrUniform,λ,ratio,low_bound)
    writer=csv.writer(csvFile)
    t=time.time()
    FairSort.FairSortForTheWhole(userList,λ,score,sorted_score,ratio,25,low_bound,gap,item_ProducerList,"airline",qualityOrUniform,0.1,dataset_name,writer)#（λ=128,ratio=1,K=23, low_bound=0.85，gap=1/256，force=0.1）+left+linearRate1
    print(f'时间差:{time.time() - t:.3f}s')
    csvFile.close()
    print('Finished!')
# 以下为阶段性测试：测试函数  FairSortForUser以及其依赖函数getReSortNDCG
# score=[[1,2,3,4,5,6,7,8,9,10]]
# sorted_score=[[9,8,7,6,5,4,3,2,1,0]]
# item_ProducerNameList=['MeiTuan','MeiTuan','MeiTuan','MeiTuan','MeiTuan','Alibaba','Alibaba','Alibaba','Alibaba','Alibaba']
# index_ProducerNameList=['MeiTuan','Alibaba']
# K=5
# F=[0.6,0]
# λ=20
# user_temp=0
# result=FairSortForUser(user_temp,λ,F,score,sorted_score,0.97,K,0.00000003,1,item_ProducerNameList,index_ProducerNameList)
# print(result[0])
# print(result[1])


#记得思考一个逻辑：公平诉求如果没有的话，我们就不需要调控
# 值得思考一下，如何控制二分查找其最后
# 值得思考一下公平提升策略：我们可以成pair搓揉，使得曝光资源方差min下来，