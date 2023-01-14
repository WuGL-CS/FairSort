import math

import numpy as np
import pandas as pd
from FairSort_OffLine import FairSort_Utils as Utils

def getSatisfaction(userId,score, recommendationList,ideal_score):
    DCG=0
    for rank_temp in range(len(recommendationList)):
        item_score = score[userId][recommendationList[rank_temp]]
        DCG += item_score/ math.log((rank_temp + 2), 2)
    return DCG/ideal_score[userId]


#will get the needed Data By the DataSetName
    # 1-providerSizeList
    # 2-providerQualityList
    # 3-providerNameList
    # 4-userRandom
    # 5-score
    # 6-sortedScore
    # 7-idealScore
    # 8-item_ProducerNameList
    # 9-m
    # 10-n
    #11-providerNum
def getData(DataSetName,K):
    Data={}
    # amazon
    review_number_amazon = 24658
    item_number_amazon = 7538
    user_number_amazon = 1851
    provider_num_amazon = 161

    # google
    review_number_google = 97658
    item_number_google = 4927
    user_number_google = 3335
    provider_num_google = 4927

    # ctrip
    o_num_international = 25190
    u_num_international = 3814
    t_num_international = 6006


    if (DataSetName == "google" or DataSetName == "amazon"):
        score_file = '/preference_score.csv'
        item_file = '/item_provider.csv'
        # random_user_temp = pd.read_csv('datasets/data_' + dataset_name + '/random_user.csv', header=None)
        # random_user_temp = random_user_temp.values
        # random_user = list(random_user_temp[0])
    elif (DataSetName == "ctrip"):
        score_file = '/score_international.csv'
        item_file = '/ticket_international.csv'
    userRandom = Utils.load_variavle("../datasets/data_"+DataSetName+"/random_user.pkl")

    item_provider = pd.read_csv('../datasets/data_' + DataSetName + item_file)
    # item_provider = np.array(item_provider.values)
    w_score = pd.read_csv('../datasets/data_' + DataSetName + score_file, header=None)
    if(DataSetName=="google" or DataSetName=="amazon"):
        score = np.array(w_score.values)
        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))
    else:
        score = w_score.iloc[:, 3:]
        score = np.array(score)
        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))

    if (DataSetName == "amazon" or DataSetName == "google"):
        producerClassName = "provider"
    else:
        producerClassName = "airline"
    providerNameList=[]
    providerSizeList=[]
    # compute ProducerNameList[] & providerSize[]
    grouped_ticket = item_provider.groupby(([producerClassName]))
    for group_name, group_list in grouped_ticket:
        providerNameList.append(group_name)
        providerSizeList.append(len(group_list))
    if (DataSetName == "google"):
        m = user_number_google
        n = item_number_google
        provider_num = provider_num_google
    elif (DataSetName == "ctrip"):
        m = u_num_international
        n = t_num_international
        provider_num=len(providerNameList)
    elif (DataSetName == "amazon"):
        m = user_number_amazon
        n = item_number_amazon
        provider_num = provider_num_amazon
    ideal_score = [0 for i in range(m)]
    for user_temp in range(m):
        for rank_temp in range(K):
            item_temp = sorted_score[user_temp][rank_temp]
            ideal_score[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)

    provider_size_total = sum(providerSizeList)
    item_ProducerNameList = item_provider[producerClassName]  # compute item_ProducerNameList=[]
    providerQualityList = Utils.load_variavle(
        filename="../datasets/Temp_Value/TFROM_" + DataSetName + "_provider_quality.pkl")
    # 1-providerSizeList
    # 2-providerQualityList
    # 3-providerNameList
    # 4-userRandom
    # 5-score
    # 6-sortedScore
    # 7-idealScore
    # 8-item_ProducerNameList
    # 9-m
    #10-n
    Data["providerSizeList"]=providerSizeList
    Data["providerQualityList"]=providerQualityList
    Data["providerNameList"]=providerNameList
    Data["userRandom"]=userRandom
    Data["score"]=score
    Data["sortedScore"]=sorted_score
    Data["idealScore"]=ideal_score
    Data["item_ProducerNameList"]=item_ProducerNameList
    Data["m"]=m
    Data["n"]=n
    Data["providerNum"]=provider_num
    return Data

