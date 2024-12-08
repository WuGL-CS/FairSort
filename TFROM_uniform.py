import pandas as pd
import numpy as np
import csv
import math
import random
from FairSort_OffLine import FairSort_Utils as Utils
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

ticket_list = pd.read_csv('datasets/data_' + dataset_name + item_file)
w_score = pd.read_csv('datasets/data_' + dataset_name + score_file)
score = w_score.iloc[:, 3:]
score = np.array(score)
score = score[:m, :n]
sorted_score = []
for i in range(len(score)):
    sorted_score.append(np.argsort(-score[i]))
sorted_score = np.array(sorted_score)

provider = []
provider_size = []
grouped_ticket = ticket_list.groupby((["airline"]))
for group_name,group_list in grouped_ticket:
    provider.append(group_name[0])#this line have a bug: it sometimes should be group_name[0] or group_name
    provider_size.append(len(group_list))
provider_size_total = sum(provider_size)

# save result analyze
csvFile = open('datasets/results/result_' + dataset_name
               + '/TFROM/result_Uniform.csv', 'w', newline='')
writer = csv.writer(csvFile)
title = []
title.append('k')
title.append('satisfaction_var')
title.append('satisfaction_total')
title.append('satisfaction_diverse')
title.append('exposure_var')
title.append('exposure_diverse')
title.append("Mean Average Envy")
title.append("Inequality in Producer Exposure(UF)")
writer.writerow(title)

for k_temp in range(2, k+1):
    total_exposure = 0
    for i in range(k_temp):
        total_exposure += 1 / math.log((i + 2), 2)
    total_exposure = total_exposure * m

    fair_exposure = []
    for i in range(len(provider)):
        fair_exposure.append(total_exposure / provider_size_total * provider_size[i])

    ideal_score = [0 for i in range(m)]
    for user_temp in range(m):
        for rank_temp in range(k_temp):
            item_temp = sorted_score[user_temp][rank_temp]
            ideal_score[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)

    user_satisfaction = [0 for i in range(m)]
    user_satisfaction_total = 0
    provider_exposure_score = [0 for i in range(len(provider))]
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
                next_provider_name = ticket_list['airline'][next_item]
                next_provider = provider.index(next_provider_name)
                if provider_exposure_score[next_provider] + 1 / math.log((top_k + 2), 2) <= fair_exposure[
                    next_provider]:
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
    avg_provider_exposure_score = []
    for i in range(len(provider)):
        avg_provider_exposure_score.append(provider_exposure_score[i] / provider_size[i])
    avg_exposure_score = sum(avg_provider_exposure_score) / len(provider)

    # result analyze
    avg_satisfaction = user_satisfaction_total / m
    diverse_satisfaction = 0
    for i in range(m):
        diverse_satisfaction = diverse_satisfaction + abs(avg_satisfaction - user_satisfaction[i]) / m

    diverse_exposure_score = 0
    for i in range(len(provider)):
        diverse_exposure_score += abs(avg_exposure_score - avg_provider_exposure_score[i]) / len(provider)

    row = []
    row.append(k_temp)
    row.append(np.var(user_satisfaction))
    row.append(user_satisfaction_total)
    row.append(diverse_satisfaction)
    row.append(np.var(avg_provider_exposure_score))
    row.append(diverse_exposure_score)
    row.append(Utils.calculate_envy(user_satisfaction))
    row.append(Utils.calculate_Inequality_Producer_Exposure(avg_provider_exposure_score))
    writer.writerow(row)

csvFile.close()
print('Finished!')
print("this is for ctrip Tfrom(UF)")
