import pandas as pd
import numpy as np
import csv
import math
import random
import pickle
from FairSort_OffLine import FairSort_Utils as FairFunction
def getFairAndCurrentErr(producerExposure,fair_exposure):
    err=[]
    for index in range(len(fair_exposure)):
        err.append(fair_exposure[index]-producerExposure[index])
    return  err

#论文作者的Bug：（Amazon）数据集
    #连喜好分数矩阵的csv导入名称都搞错，写成result.csv  实际应该是：item_provider.csv
    #fair_exposure计算逻辑惊人啊！！！   （居然这么算）
        # fair_exposure = []
        # for i in range(provider_num):
        #     fair_exposure.append(total_exposure / n * provider_quality[i])
    #正常应该是：
        # fair_exposure = []
        # for i in range(len(provider)):
        #     fair_exposure.append(total_exposure / sum(provider_quality) * provider_quality[i])
    #min值又是忘记更新啊！！！！
def save_value(value, filePath):
    pic = open(filePath, 'wb')
    pickle.dump(value, pic)
    pic.close()


def load_variavle(filename):
    try:
        f = open(filename, 'rb+')
        r = pickle.load(f)
        f.close()
        return r
    except EOFError:
        return ""
if __name__ == '__main__':

    review_number_amazon = 24658
    item_number_amazon = 7538
    user_number_amazon = 1851
    provider_num_amazon = 161

    review_number_google = 97658
    item_number_google = 4927
    user_number_google = 3335
    provider_num_google = 4927

    m = user_number_amazon
    n = item_number_amazon
    provider_num = provider_num_amazon

    k = 25
    dataset_name = 'amazon'
    score_file = '/preference_score.csv'
    item_file = '/item_provider.csv'

    item_provider = pd.read_csv('datasets/data_' + dataset_name + item_file)
    item_provider = np.array(item_provider.values)
    w_score = pd.read_csv('datasets/data_' + dataset_name + score_file, header=None)#这里有错误，为什么连文件的socre名还引错，写成result.csv

    score = np.array(w_score.values)
    sorted_score = []
    for i in range(len(score)):
        sorted_score.append(np.argsort(-score[i]))

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
    title.append('Top-K_exposure_quality_var')
    title.append('exposure_quality_var')
    title.append('exposure_quality_diverse')
    title.append("fair_VarAtFirst")
    title.append("fair_Var")
    # title.append('Top-k Conversation Rate')
    # title.append('TFROM-Conversation Rate')
    writer.writerow(title)

    provider_quality = [0 for i in range(provider_num)]
    # for user_temp in range(m):
    #     for rank_temp in range(n):
    #         item_temp = sorted_score[user_temp][rank_temp]
    #         provider_temp = item_provider[item_temp][1]
    #         provider_quality[provider_temp] += score[user_temp][item_temp]
    #     print('provider_quality: %d' % (user_temp))
    # save_value(provider_quality,"datasets/Temp_Value/TFROM_amazon_provider_quality.pkl")
    provider_quality=load_variavle(f"datasets/Temp_Value/TFROM_{dataset_name}_provider_quality.pkl")
    for k_temp in range(2, k+1):
        ideal_score = [0 for i in range(m)]

        for user_temp in range(m):
            for rank_temp in range(k_temp):
                item_temp = sorted_score[user_temp][rank_temp]
                ideal_score[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)

        total_exposure = 0
        for i in range(k_temp):
            total_exposure += 1 / math.log((i + 2), 2)
        total_exposure = total_exposure * m
        # 下面这个函数有BUG呀！！！！！
            #正常逻辑如下:
                # fair_exposure = []
                # for i in range(len(provider)):
                #     fair_exposure.append(total_exposure / sum(provider_quality) * provider_quality[i])

        # fair_exposure = []
        # for i in range(provider_num):
        #     fair_exposure.append(total_exposure / n * provider_quality[i])

        fair_exposure = []
        for i in range(provider_num):
            fair_exposure.append(total_exposure / sum(provider_quality) * provider_quality[i])


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
                    if provider_quality[next_provider] > 0 and \
                            provider_exposure_score[next_provider] + 1 / math.log((top_k + 2), 2) \
                            <= fair_exposure[next_provider]:
                        rec_result[next_user][top_k] = next_item
                        user_satisfaction[next_user] += \
                            score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                        user_satisfaction_total += \
                            score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                        provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
                        rec_flag[next_user].remove(next_item)
                        break
                print('k:%d, rank:%d, i:%d' % (k_temp, top_k, i))

        for top_k in range(k_temp):
            for next_user in range(m):
                if rec_result[next_user][top_k] == -1:
                    min_exposure = 10000000000000000
                    for item_temp in rec_flag[next_user]:
                        provider_temp = next_provider = item_provider[item_temp][1]
                        if provider_exposure_score[provider_temp] < min_exposure:
                            next_item = item_temp
                            next_provider = provider_temp
                            #原有作者  对min值依旧忘记更新啊！！！！！
                            min_exposure = provider_exposure_score[provider_temp]  # 作者这有一处错误：没有更新min_exposure的值
                    rec_result[next_user][top_k] = next_item
                    user_satisfaction[next_user] += \
                        score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                    user_satisfaction_total += \
                        score[next_user][next_item] / math.log((top_k + 2), 2) / ideal_score[next_user]
                    provider_exposure_score[next_provider] += 1 / math.log((top_k + 2), 2)
                    rec_flag[next_user].remove(next_item)

        #计算Top-K资源分布情况
        producerExposure_TopK = [0 for i in range(len(provider_quality))]
        for user_temp in range(m):
            for rank_temp in range(k_temp):
                item_temp = sorted_score[user_temp][rank_temp]
                item_producerId = item_provider[item_temp][1]
                producerExposure_TopK[item_producerId] += 1 / math.log((2 + rank_temp), 2)


        avg_provider_exposure_score = []
        provider_exposure_quality = []
        for i in range(provider_num):
            item_id = int(np.argwhere(item_provider[:, 1] == i)[0])
            avg_provider_exposure_score.append(provider_exposure_score[i] / item_provider[item_id][2])
            provider_exposure_quality.append((provider_exposure_score[i]  / provider_quality[i])*1000 )
        avg_exposure_score = sum(avg_provider_exposure_score) / provider_num
        avg_provider_exposure_quality = sum(provider_exposure_quality) / provider_num

        # result analyze
        avg_satisfaction = user_satisfaction_total / m
        diverse_satisfaction = 0
        for i in range(m):
            diverse_satisfaction = diverse_satisfaction + abs(avg_satisfaction - user_satisfaction[i]) / m
            print('k: %d diverse_satisfaction i: %d' % (k_temp, i))

        diverse_exposure_score = 0
        for i in range(provider_num):
            diverse_exposure_score += abs(avg_exposure_score - avg_provider_exposure_score[i]) / provider_num

        divers_exposure_quality = 0
        for i in range(len(provider_exposure_quality)):
            divers_exposure_quality += abs(avg_provider_exposure_quality - provider_exposure_quality[i]) / provider_num

        #result
        print("算法结束了：")
        print("最终提供商侧的最终曝光资源分布为", provider_exposure_score)
        print("公平分配应该为：", fair_exposure)
        print("提供商一开始top-k价值转化率为：",
              FairFunction.getProducerExposurCoversionRate(producerExposure_TopK, 0, None, provider_quality))
        print("提供商侧的价值最终转化率分布为：",
              FairFunction.getProducerExposurCoversionRate(provider_exposure_score, 0, None, provider_quality))
        print("一开始的Top-K的差额值:", FairFunction.getFairAndCurrentErr(producerExposure_TopK, fair_exposure))
        print("FairSort的差额值:", FairFunction.getFairAndCurrentErr(provider_exposure_score, fair_exposure))



        TopK_ExposureConversationRate=FairFunction.getProducerExposurCoversionRate(producerExposure_TopK,0,None,provider_quality)
        row = []
        row.append(k_temp)
        row.append(np.var(user_satisfaction))
        row.append(user_satisfaction_total)
        row.append(diverse_satisfaction)
        row.append(np.var(avg_provider_exposure_score))
        row.append(diverse_exposure_score)
        row.append(FairFunction.getVar(TopK_ExposureConversationRate))
        row.append(np.var(provider_exposure_quality))
        row.append(divers_exposure_quality)
        row.append(np.var(getFairAndCurrentErr(producerExposure_TopK,fair_exposure)))
        row.append(np.var(getFairAndCurrentErr(provider_exposure_score,fair_exposure)))
        # row.append(TopK_ExposureConversationRate)
        # row.append(provider_exposure_quality)
        writer.writerow(row)

csvFile.close()
print('Finished!')

