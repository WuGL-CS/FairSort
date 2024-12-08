import pandas as pd
import numpy as np
import csv
import math
import random
from FairSort_OffLine import FairSort_Utils as FairFunction
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

item_provider = pd.read_csv('datasets/data_' + dataset_name + item_file)
item_provider = np.array(item_provider.values)
w_score = pd.read_csv('datasets/data_' + dataset_name + score_file, header=None)
score = np.array(w_score.values)
sorted_score = []
for i in range(len(score)):
    sorted_score.append(np.argsort(-score[i]))

# save result analyze

csvFile = open('datasets/results/result_' + dataset_name
               + '/TFROM/result_Uniform.csv', 'w', newline='')
writer = csv.writer(csvFile)
title = []
title.append('k')
title.append('satisfaction_var')
title.append('satisfaction_total')
title.append('satisfaction_diverse')
title.append('Top-K_exposure_var')
title.append('exposure_var')
title.append('exposure_diverse')
# title.append('Top-k Conversation Rate')

title.append("Mean Average Envy")
title.append("Inequality in Producer Exposure(UF)")
writer.writerow(title)

for k_temp in range(2, k+1):
    total_exposure = 0
    for i in range(k_temp):
        total_exposure += 1 / math.log((i + 2), 2)
    total_exposure = total_exposure * m

    fair_exposure = []
    providerSize=[]
    for i in range(provider_num):
        item_id = int(np.argwhere(item_provider[:, 1] == i)[0])
        fair_exposure.append(total_exposure / n * item_provider[item_id][2])
        providerSize.append(item_provider[item_id][2])

    ideal_score = [0 for i in range(m)]
    for user_temp in range(m):
        for rank_temp in range(k_temp):
            item_temp = sorted_score[user_temp][rank_temp]
            ideal_score[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)

    user_satisfaction = [0 for i in range(m)]
    user_satisfaction_total = 0
    provider_exposure_score = [0 for i in range(provider_num)]
    rec_result = np.full((m, k_temp), -1)
    rec_flag = []
    for i in range(m):
        rec_flag.append(list(sorted_score[i]))

    for top_k in range(k_temp):
        # sort user according to user_satisfaction
        rank_user_satisfaction = [temp for temp in range(m)]
        random.shuffle(rank_user_satisfaction)
        rank_user_satisfaction.sort(key=lambda x: user_satisfaction[x], reverse=True)
        for i in range(m):
            next_user = rank_user_satisfaction[i]

            # find next item and provider
            for next_item in rec_flag[next_user]:
                next_provider = item_provider[next_item][1]
                if provider_exposure_score[next_provider] + 1 / math.log((top_k + 2), 2) \
                        <= fair_exposure[next_provider]:
                    rec_flag[next_user].remove(next_item)
                    rec_result[next_user][top_k] = next_item
                    user_satisfaction[next_user] += \
                        score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                    user_satisfaction_total += \
                        score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                    provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
                    break
            print('k:%d, rank:%d, i:%d' % (k_temp, top_k, i))

            # 这个的处理逻辑：就是对于没有被安排上的位置的处理逻辑
    for top_k in range(k_temp):
        for next_user in range(m):
            if rec_result[next_user][top_k] == -1:
                min_exposure = 10000000000000000
                # 此处for:映射物品：其提供商的曝光值当前最小，其次是在原列表中排名最前
                for item_temp in rec_flag[next_user]:
                    provider_temp = item_provider[item_temp][1]
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

    # 计算Top-K资源分布情况
    producerExposure_TopK = [0 for i in range(provider_num)]
    for user_temp in range(m):
        for rank_temp in range(k_temp):
            item_temp = sorted_score[user_temp][rank_temp]
            item_producerId = item_provider[item_temp][1]
            producerExposure_TopK[item_producerId] += 1 / math.log((2 + rank_temp), 2)
    avg_provider_exposure_score = []
    for i in range(provider_num):
        item_id = int(np.argwhere(item_provider[:, 1] == i)[0])
        avg_provider_exposure_score.append(provider_exposure_score[i] / item_provider[item_id][2])
    avg_exposure_score = sum(avg_provider_exposure_score) / provider_num

    # result analyze
    avg_satisfaction = user_satisfaction_total / m
    diverse_satisfaction = 0
    for i in range(m):
        diverse_satisfaction = diverse_satisfaction + abs(avg_satisfaction - user_satisfaction[i]) / m

    diverse_exposure_score = 0
    for i in range(provider_num):
        diverse_exposure_score += abs(avg_exposure_score - avg_provider_exposure_score[i]) / provider_num
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    for satisfaction in user_satisfaction:

        if(satisfaction<0.7):
            count1+=1
        elif(satisfaction<=0.75):
            count2+=1
        elif(satisfaction<=0.8):
            count3+=1
        elif(satisfaction<=0.85):
            count4+=1
        elif(satisfaction<=0.9):
            count5+=1
        elif(satisfaction<=0.95):
            count6+=1
    print("0.7以下",count1)
    print("0.7—0.75",count2)
    print("0.75—0.8",count3)
    print("0.8—0.85",count4)
    print("0.85—0.9",count5)
    print("0.9—0.95",count6)
    print("总共:",count6+count5+count4+count3+count2+count1)
    row = []
    row.append(k_temp)
    row.append(np.var(user_satisfaction))
    row.append(user_satisfaction_total)
    row.append(diverse_satisfaction)
    row.append(np.var(FairFunction.getProducerExposurCoversionRate(producerExposure_TopK,1,providerSize,None)))
    row.append(np.var(avg_provider_exposure_score))
    row.append(diverse_exposure_score)
    row.append(FairFunction.calculate_envy(user_satisfaction))
    row.append(FairFunction.calculate_Inequality_Producer_Exposure(avg_provider_exposure_score))
    # row.append(FairFunction.getProducerExposurCoversionRate(producerExposure_TopK,1,providerSize,None))
    # row.append(FairFunction.getProducerExposurCoversionRate(provider_exposure_score,1,providerSize,None))
    writer.writerow(row)
csvFile.close()
print('Finished!')
print('this is for TFROM (UF) google')

