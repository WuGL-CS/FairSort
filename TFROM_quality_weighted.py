import time as time
import numpy
import pandas as pd
import numpy as np
import csv
import math
from FairSort_OffLine import FairSort_Utils as Utils
import random
import pickle
def getProducerExposurCoversionRate(producerExposure,fairRegulation,providerSize,provider_quality):
    convertRate = []
    if (fairRegulation == 0):  # 这个是基于价值效益
        for index in range(len(producerExposure)):
            convertRate.append(producerExposure[index] / provider_quality[index]*1000)
        return convertRate
    elif (fairRegulation == 1):  # 这个是基于数量效益的
        for index in range(len(producerExposure)):
            convertRate.append(producerExposure[index] / providerSize[index])
        return convertRate
def getFairAndCurrentErr(producerExposure,fair_exposure):
    err=[]
    for index in range(len(fair_exposure)):
        err.append(fair_exposure[index]-producerExposure[index])
    return  err
def offlineFunction(k_temp,score,ticket_list,sorted_score,result_writer,provider,provider_size,provider_quality):

        ideal_score = [0 for i in range(m)]  # 每一趟初始化一个空的列表，存放各个用户的IDCG（最大值），当前K

        # 下面这个for循环：就是在K确定下，为每个用户计算出理想的IDCG值
        for user_temp in range(m):
            for rank_temp in range(k_temp):
                item_temp = sorted_score[user_temp][rank_temp]
                ideal_score[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)
            print('k: %d ideal_score: %d' % (k_temp, ideal_score[user_temp]))
        # 计算当前K下，总曝光资源
        total_exposure = 0
        for i in range(k_temp):
            total_exposure += 1 / math.log((i + 2), 2)
        total_exposure = total_exposure * m

        # 计算每个提供商的曝光公平阈值——基于价值量
        fair_exposure = []
        for i in range(len(provider)):
            fair_exposure.append(total_exposure / sum(provider_quality) * provider_quality[i])
        # 进行相关依赖变量的初始化
        user_satisfaction = [0 for i in range(m)]
        user_satisfaction_total = 0
        provider_exposure_score = [0 for i in range(len(provider))]
        rec_result = np.full((m, k_temp), -1)
        rec_flag = []
        for i in range(m):
            rec_flag.append(list(sorted_score[i]))

        # 以下这行是老子给他改造的，麻蛋，逻辑必须得这样才是严谨的，算法执行起来快的多
        # rec_flag = [rec_flag[i][0:k_temp] for i in range(len(rec_flag))]

        # 开始制作重排推荐列表：
        for top_k in range(k_temp):
            # sort user according to user_satisfaction
            rank_user_satisfaction = [temp for temp in range(m)]
            random.shuffle(rank_user_satisfaction)
            # 下面这个排序个人认为比较有问题，用户满意度应该低的优先服务，应该升序，reverse要等于=False
            rank_user_satisfaction.sort(key=lambda x: user_satisfaction[x], reverse=True)
            for i in range(m):
                next_user = rank_user_satisfaction[i]  # 依次为每个用户开始服务

                # find next item and provider
                for next_item in rec_flag[next_user]:  # 从每个用户的推荐列表中取出从高到低取物品
                    next_provider_name = ticket_list['airline'][next_item]  # 先获取提供商名
                    next_provider = provider.index(next_provider_name)  # 再获取提供商下标
                    if provider_exposure_score[next_provider] + 1 / math.log((top_k + 2), 2) \
                            <= fair_exposure[next_provider]:  # 不超出公平阈值
                        rec_result[next_user][top_k] = next_item  # 放入物品
                        # 放入物品后更新推荐质量+曝光分配值+总NDCG值,还有移除物品
                        user_satisfaction[next_user] += \
                            score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                        user_satisfaction_total += \
                            score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                        provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
                        rec_flag[next_user].remove(next_item)
                        break
                print('当前的超参数k:%d, 当前超参数K下，安排的第rank（从0开始）:%d, 第i位用户（从0开始）:%d' % (k_temp, top_k, i))

        # 这个的处理逻辑：就是对于没有被安排上的位置的处理逻辑
        for top_k in range(k_temp):
            for next_user in range(m):
                if rec_result[next_user][top_k] == -1:
                    min_exposure = 10000000000000000
                    # 此处for:映射物品：其提供商的曝光值当前最小，其次是在原列表中排名最前
                    for item_temp in rec_flag[next_user]:
                        provider_name_temp = ticket_list['airline'][item_temp]
                        provider_temp = provider.index(provider_name_temp)
                        if provider_exposure_score[provider_temp] < min_exposure:
                            next_item = item_temp
                            next_provider = provider_temp
                            min_exposure = provider_exposure_score[provider_temp]  # 这有一处错误：没有更新min_exposure的值
                    # for结束后，将其得到的物品放入推荐列表中，更新必要信息
                    rec_result[next_user][top_k] = next_item
                    user_satisfaction[next_user] += \
                        score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                    user_satisfaction_total += \
                        score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                    provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
                    rec_flag[next_user].remove(next_item)  # 记得移除物品
        avg_provider_exposure_score = []  # 提供商关于曝光资源和物品数目的平均
        provider_exposure_quality = []  # 提供商关于曝光资源和价值量的平均*分子分母都有一个归一化系数
        for i in range(len(provider)):
            avg_provider_exposure_score.append(provider_exposure_score[i] / provider_size[i])
            provider_exposure_quality.append((provider_exposure_score[i] / max(provider_exposure_score))
                                             / (provider_quality[i] / max(provider_quality)))
        # 上面就是核心函数：solve（k_temp）,返回推荐结果，
        #               里面有一个bug，最小值没有更新
        #               其次就是我认为从大到小排是不合理的，应该让NDCG小的，
        avg_exposure_score = sum(avg_provider_exposure_score) / len(provider)
        avg_provider_exposure_quality = sum(provider_exposure_quality) / len(provider)
        print(getFairAndCurrentErr(provider_exposure_score,fair_exposure))
        # result analyze
        avg_satisfaction = user_satisfaction_total / m
        diverse_satisfaction = 0
        for i in range(m):
            diverse_satisfaction = diverse_satisfaction + abs(avg_satisfaction - user_satisfaction[i]) / m

        diverse_exposure_score = 0
        for i in range(len(provider)):
            diverse_exposure_score += abs(avg_exposure_score - avg_provider_exposure_score[i]) / len(provider)

        divers_exposure_quality = 0
        for i in range(len(provider_exposure_quality)):
            divers_exposure_quality += abs(avg_provider_exposure_quality - provider_exposure_quality[i]) / len(provider)
        print("公平曝光：",fair_exposure)
        print("最终曝光:",provider_exposure_score)
        print("转化率：",getProducerExposurCoversionRate(provider_exposure_score,0,provider_size,provider_quality))
        print("价值分布：",provider_quality)
        row = []
        row.append(k_temp)#K超参数
        row.append(np.var(user_satisfaction))#用户满意度向量的方差
        row.append(user_satisfaction_total)#用户总满意度
        row.append(diverse_satisfaction)#满意度的绝对值偏移量
        row.append(np.var(avg_provider_exposure_score))#曝光基于物品数转化率的方差
        row.append(diverse_exposure_score)#曝光基于物品数转化率的绝对值偏移
        row.append(np.var(provider_exposure_quality))#曝光基于价值的转化率方差
        row.append(divers_exposure_quality)##曝光基于价值的绝对值转化率偏移
        row.append(np.var(getFairAndCurrentErr(provider_exposure_score,fair_exposure)))
        row.append(Utils.calculate_envy(user_satisfaction))
        row.append(Utils.calculate_Inequality_Producer_Exposure(provider_exposure_quality))
        result_writer.writerow(row)
def save_variable(v,filename):
  f=open(filename,'wb')          #打开或创建名叫filename的文档。
  pickle.dump(v,f)               #在文件filename中写入v
  f.close()                      #关闭文件，释放内存。
  return filename


def load_variavle(filename):
    try:
        f = open(filename, 'rb+')
        r = pickle.load(f)
        f.close()
        return r

    except EOFError:
        return ""

o_num_international = 25190
u_num_international = 3814
t_num_international = 6006

m = u_num_international
#m = 100
n = t_num_international
#n = 50
k = 25
dataset_name = 'ctrip'
score_file = '/score_international.csv'
item_file = '/ticket_international.csv'
#ticket_list:订单表：ID airline classes price
ticket_list = pd.read_csv('datasets/data_' + dataset_name + item_file)
#用户和item的贡献矩阵：评分矩阵
w_score = pd.read_csv('datasets/data_' + dataset_name + score_file)
#评分矩阵score
score = w_score.iloc[:, 3:]
score = np.array(score)
score = score[:m, :n]
sorted_score = []
for i in range(len(score)):
    sorted_score.append(np.argsort(-score[i]))
sorted_score = np.array(sorted_score)#这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表

provider = []
provider_size = []
grouped_ticket = ticket_list.groupby((["airline"]))
for group_name,group_list in grouped_ticket:
    provider.append(group_name[0])
    provider_size.append(len(group_list))
provider_size_total = sum(provider_size)

# save result analyze
csvFile = open('datasets/results/result_' + dataset_name
               + '/TFROM/result_quality.csv', 'w', newline='')
writer = csv.writer(csvFile)
title = []
title.append('k')
title.append('satisfaction_var')
title.append('satisfaction_total')
title.append('satisfaction_diverse')
title.append('exposure_var')
title.append('exposure_diverse')
title.append('exposure_quality_var')
title.append('exposure_quality_diverse')
title.append('方差力度')
title.append('Mean Average Envy')
title.append('Inequality in Producer Exposure(QF)')
writer.writerow(title)

provider_quality = [0 for i in range(len(provider))]
#下面这个函数负值映射提供商的价值量
#     遍历user维度和item维度，也就是遍历完所有的评分信息
# for user_temp in range(m):
#     for rank_temp in range(n):
#         item_temp = sorted_score[user_temp][rank_temp]#推荐列表里的物品编号
#         provider_name_temp = ticket_list['airline'][item_temp]#映射该物品的生产商名字
#         provider_temp = provider.index(provider_name_temp)#得到生产商对应的索引
#         provider_quality[provider_temp] += score[user_temp][item_temp]#加入到生产商的价值矢量里
#     print('collecting provider_quality ing Now turn user_temp: %d' % (user_temp))
#保存变量到文件中：
    # save_variable(provider_quality,filename="datasets/Temp_Value/TFROM_ctrip_provider_quality.pkl")
provider_quality=load_variavle(filename="datasets/Temp_Value/TFROM_ctrip_provider_quality.pkl")
print(provider_quality)
#上面所有的代码其实就是获得算法执行所依赖的所有数据信息
# csv表格：ticket信息表（可以知道生成商有哪些，以及对应生产商下有哪些物品），score表（物品和用户索引，以及交互分数）
#1-需要一个score：评分矩阵：这个是直接获取的，（user——item）的评分矩阵——>再计算出相应的score-socked排序列表
#2-计算出provider向量和对应的provider_size向量，还有获得provider_quality
# 有了score——有了score——socked（排序列表），有了生成商（item——producer关系），producer（价值和尺寸信息）
# 超参数K；
# 输出排序列表：
#需要中间变量：被安排的排序列表的质量在变化，producer的曝光值变量
#


#下面的映射逻辑：
#   K_temp∈[2,K]
#       每当K确定：
#                 映射--->每个用户的IDCG:ideal_score
#                 映射--->总曝光资源，映射--->公平曝光阈值：fair_exposure
#                 初始化：user_satisfaction：用户满意度 user_satisfaction_total
#                        provider_exposure_score
#                        rec_result = np.full((m, k_temp), -1)
#                        rec_flag：每个用户的原推荐列表
#
t=time.time()
for k_temp in range(2,26):
    offlineFunction(k_temp,score,ticket_list,sorted_score,writer,provider,provider_size,provider_quality)
print(f'时间差:{time.time() - t:.3f}s')
csvFile.close()
print('Finished!')
print('this is for TFROM ctrip (QF)')
   