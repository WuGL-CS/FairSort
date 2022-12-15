import pandas as pd
import numpy as np
import csv
import math

o_num_international = 25190
u_num_international = 3814
t_num_international = 6006

m = u_num_international
#m = 50
n = t_num_international
#n = 20

k = 20
total_round = 10 * m
dataset_name = 'ctrip'
score_file = '/score_international.csv'
item_file = '/ticket_international.csv'

random_user_temp = pd.read_csv('datasets/data_' + dataset_name + '/random_user.csv', header=None)
random_user_temp = random_user_temp.values
random_user = list(random_user_temp[0])

ticket_list = pd.read_csv('datasets/data_' + dataset_name + item_file)
w_score = pd.read_csv('datasets/data_' + dataset_name + score_file)
score = w_score.iloc[:, 3:]
score = np.array(score)
score = score[:m, :n]
sorted_score = []
for i in range(len(score)):
    sorted_score.append(np.argsort(-score[i]))

provider = []
provider_size = []
grouped_ticket = ticket_list.groupby((["airline"]))
for group_name,group_list in grouped_ticket:
    provider.append(group_name)
    provider_size.append(len(group_list))


#save result analyze
csvFile = open('datasets/results/result_' + dataset_name +
               '/dynamic/dynamic_result_analyze_TFROM.csv', 'w', newline='')
writer = csv.writer(csvFile)
title = []
title.append('round')
title.append('satisfaction_var')
title.append('satisfaction_total')
title.append('satisfaction_diverse')
title.append('exposure_var')
title.append('exposure_diverse')
writer.writerow(title)

user_satisfaction = [0 for i in range(m)]
user_rec_time = [0 for i in range(m)]
user_satisfaction_total = 0
satisfaction_total = 0
provider_exposure_score = [0 for i in range(len(provider))]

ideal_score = [0 for i in range(m)]
for user_temp in range(m):
    for rank_temp in range(k):
        item_temp = sorted_score[user_temp][rank_temp]
        ideal_score[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)

for round_temp in range(total_round):
    total_exposure = 0
    for i in range(k):
        total_exposure += 1 / math.log((i + 2), 2)
    total_exposure = total_exposure * (round_temp + 1)

    fair_exposure = []
    for i in range(len(provider)):
        fair_exposure.append(total_exposure / n * provider_size[i])

    next_user = random_user[round_temp]
    rec_flag = list(sorted_score[next_user])
    user_satisfaction_temp = 0
    rec_result = [-1 for i in range(k)]

    # find next item and provider
    for top_k in range(k):
        for next_item in rec_flag:
            next_provider_name = ticket_list['airline'][next_item]
            next_provider = provider.index(next_provider_name)
            if provider_exposure_score[next_provider] + 1 / math.log((top_k + 2), 2) <= fair_exposure[next_provider]:
                rec_result[top_k] = next_item
                user_satisfaction_temp += score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[
                    next_user]
                provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
                rec_flag.remove(next_item)
                break
        print('round:%d, rank:%d' % (round_temp, top_k))

    for top_k in range(k):
        if rec_result[top_k] == -1:
            next_item = rec_flag[0]
            next_provider_name = ticket_list['airline'][next_item]
            next_provider = provider.index(next_provider_name)
            rec_result[top_k] = next_item
            user_satisfaction_temp += score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[
                next_user]
            provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
            del rec_flag[0]

    user_satisfaction_total -= user_satisfaction[next_user]
    user_satisfaction[next_user] = (user_satisfaction[next_user] * user_rec_time[next_user] + user_satisfaction_temp) \
                                   / (user_rec_time[next_user] + 1)
    user_satisfaction_total += user_satisfaction[next_user]
    satisfaction_total += user_satisfaction_temp
    user_rec_time[next_user] += 1

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

    # save result analyze
    row = []
    row.append(round_temp)
    row.append(np.var(user_satisfaction))
    row.append(satisfaction_total)
    row.append(diverse_satisfaction)
    row.append(np.var(avg_provider_exposure_score))
    row.append(diverse_exposure_score)
    writer.writerow(row)

print('Finished!')