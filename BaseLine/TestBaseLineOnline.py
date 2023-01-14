import csv
import math

import BaseLineFunction as BaseLineFunction
from FairSort_OffLine import FairSort_Utils as Utils
import BaseLineUtils as baseLineUtils
import numpy as np

def writeCsvTitleOnLine(DataSetName,BaseLineName):
    csvFile = open('Results/OnLine/' + DataSetName +
                   "/" + BaseLineName + ".csv", 'w', newline='')
    writer = csv.writer(csvFile)
    title = []
    title.append('round')
    title.append('satisfaction_var')
    title.append('satisfaction_total')
    title.append('satisfaction_diverse')
    title.append('exposure_var')
    title.append('exposure_diverse')
    title.append('exposure_quality_var')
    title.append('exposure_quality_diverse')
    title.append(
        "NDCG:{[0--0.5],[0.5--0.6],[0.6--0.7],[0.7--0.75],[0.75-0.8],[0.8--0.85],[0.85--0.9],[0.9--0.95],[0.95--1]}")
    writer.writerow(title)
    return writer

#compute:satisfaction_var,satisfaction_total,exposure_var,exposure_quality_var
def getRecomendationList(userId, BaseLineName,sorted_score,K,itemExposureList):
    recommendationList=None
    if (BaseLineName == "Top_K_Online"):
        recommendationList=BaseLineFunction.Top_K_Online(userId,sorted_score,K)
    elif (BaseLineName == "Random_k_Online"):
        recommendationList=BaseLineFunction.Random_k_Online(userId,sorted_score,K)
    elif (BaseLineName == "minimumExposure_OnLine"):
        recommendationList=BaseLineFunction.minimumExposure_OnLine(itemExposureList,K)
    elif (BaseLineName == "Mixed_k_OnLine"):
        recommendationList=BaseLineFunction.Mixed_k_OnLine(userId,sorted_score,K)
    return recommendationList


def AllocateExposureOnline(providerExposureList, recommendationList, providerNameList,item_ProducerNameList):
    for rankTemp in range(len(recommendationList)):
        item=recommendationList[rankTemp]
        providerName=item_ProducerNameList[item]
        providerIndex=providerNameList.index(providerName)
        providerExposureList[providerIndex]+=1/math.log(2+rankTemp,2)

def testBaseLineOnLine(DataSetName,BaseLineName,K,writer):
    Data=baseLineUtils.getData(DataSetName,K)
    providerSizeList=Data["providerSizeList"]
    providerQualityList=Data["providerQualityList"]
    providerNameList=Data["providerNameList"]
    userRandom=Data["userRandom"]
    score=Data["score"]
    sorted_score=Data["sortedScore"]
    ideal_score=Data["idealScore"]
    item_ProducerNameList=Data["item_ProducerNameList"]
    m=Data["m"]
    n=Data["n"]
    providerNum=Data["providerNum"]
#Global Value:
    userAvgSatisfactionList = [0 for x in range(m)]
    userAvgSatisfactionTotal = 0
    userRecomendTimeList = [0 for x in range(m)]
    satisfactionTotal = 0  # 推荐列表的满意度总和
    satisDistributeList = [0 for x in range(9)]

    providerExposureList = [0 for i in range(providerNum)]
    itemExposureList=[0 for x in range(n)]
    for roundTime in range(len(userRandom)):
        print("当前第"+str(roundTime)+"个user")
        userId=userRandom[roundTime]
        recommendationList=getRecomendationList(userId,BaseLineName,sorted_score,K,itemExposureList)
        satisfactionTemp=baseLineUtils.getSatisfaction(userId,score,recommendationList,ideal_score)
        AllocateExposureOnline(providerExposureList,recommendationList,providerNameList,item_ProducerNameList)

        Utils.getSatisfactionDistribution2(satisfactionTemp, satisDistributeList)
        userAvgSatisfactionTotal -= userAvgSatisfactionList[userId]
        userAvgSatisfactionList[userId] = (userAvgSatisfactionList[userId] * userRecomendTimeList[
            userId] + satisfactionTemp) / (userRecomendTimeList[userId] + 1)
        userAvgSatisfactionTotal += userAvgSatisfactionList[userId]
        satisfactionTotal += satisfactionTemp
        userRecomendTimeList[userId] += 1
        provider_exposure_num_rate = Utils.getProducerExposurCoversionRate(providerExposureList, 1,
                                                                            providerSizeList, providerQualityList)
        diverse_exposure_score = Utils.getStandardDeviation(provider_exposure_num_rate)

        provider_exposure_quality_rate = Utils.getProducerExposurCoversionRate(providerExposureList, 0,
                                                                                   providerSizeList,
                                                                                   providerQualityList)
        divers_exposure_quality = Utils.getStandardDeviation(provider_exposure_quality_rate)

        diverse_satisfaction = Utils.getStandardDeviation(userAvgSatisfactionList)

        row = []
        row.append(roundTime)
        row.append(np.var(userAvgSatisfactionList))
        row.append(satisfactionTotal)
        row.append(diverse_satisfaction)
        temp = np.var(provider_exposure_num_rate)
        row.append(temp)
        print("******数量公平性指标******：", temp)
        row.append(diverse_exposure_score)
        temp = np.var(provider_exposure_quality_rate)
        row.append(temp)
        print("******价值公平性指标******：", temp)
        row.append(divers_exposure_quality)
        row.append(satisDistributeList)
        print("NDCG分布:", satisDistributeList)
        print("提供商当前拥有的曝光资源:", providerExposureList)
        if (roundTime == len(userRandom) - 1):
            print("算法结束了：")
            print("提供商最终的曝光资源分配值为：", providerExposureList)
            print("数量转化率分布为:",
                  Utils.getProducerExposurCoversionRate(providerExposureList, 1, providerSizeList,
                                                        providerQualityList))
            print("价值转化率分布为:",
                  Utils.getProducerExposurCoversionRate(providerExposureList, 0, providerSizeList,
                                                        providerQualityList))
        writer.writerow(row)


if __name__ == '__main__':
    writer=writeCsvTitleOnLine("google","minimumExposure_OnLine")
    testBaseLineOnLine("google","minimumExposure_OnLine",20,writer)
