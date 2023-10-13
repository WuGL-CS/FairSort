import csv
import math
from FairSort_OffLine import FairSort_Utils as FairSortUtils
import BaseLineUtils as baseLineUtils
import BaseLineFunction as functions
#compute:satisfaction_var,satisfaction_total,exposure_var,exposure_quality_var
def getRecomendationListOffLine(userList, BaseLineName,sorted_score,K,itemExposureList,score):
    recommendationList=None
    if (BaseLineName == "Top_K_Offline"):
        recommendationList=functions.Top_K_Offline(userList,sorted_score,K)
    elif (BaseLineName == "minimumExposure_OffLine"):
        recommendationList=functions.minimumExposure_OffLine(userList,K,itemExposureList)
    elif (BaseLineName == "FairRecOffLine"):
        recommendationList=functions.FairRecOffLine(userList,[x for x in range(len(sorted_score[0]))],K,score,1)
    elif (BaseLineName == "Mixed_k_Offline"):
        recommendationList=functions.Mixed_k_Offline(userList,sorted_score,K)
    elif(BaseLineName=="Random_k_Offline"):
        recommendationList=functions.Random_k_Offline(userList,sorted_score,K)
    elif(BaseLineName=="CP_Fair_Offline"):
        recommendationList=functions.CP_Fair_Offline(score,sorted_score,K,50,2,len(userList),len(score[0]),"CP",0.5,0.5)
    return recommendationList
def writeCsvTitleOffLine(DataSetName,BaseLineName):
    csvFile = open('Results/OffLine/' + DataSetName +
                   "/" + BaseLineName + ".csv", 'w', newline='')
    writer = csv.writer(csvFile)
    title = []
    title.append('k')
    title.append('satisfaction_var')
    title.append('satisfaction_diverse')
    title.append('satisfaction_total')
    title.append('exposure_quality_var')
    title.append('exposure_quality_diverse')
    title.append('exposure_var')
    title.append('exposure_diverse')
    writer.writerow(title)
    return writer


def computeExposureAndSatis(recomResults, providerExposureList, userSatisfactionList,ideal_score,score,providerNameList,item_ProducerNameList):
    for userId,RecoList in recomResults.items():
        DCG=0
        for K_temp in (range(len(RecoList))):
            item=RecoList[K_temp]
            DCG+=(score[userId][item]/math.log(2+K_temp,2))
            producerName=item_ProducerNameList[item]
            producerIndex=providerNameList.index(producerName)
            providerExposureList[producerIndex]+=1/math.log(2+K_temp,2)
        userSatisfactionList[userId]=DCG/ideal_score[userId]



def testBaseLineOffLine(DataSetName,BaseLineName,K,writer):
    Data = baseLineUtils.getData(DataSetName,K)
    providerSizeList = Data["providerSizeList"]
    providerQualityList = Data["providerQualityList"]
    providerNameList = Data["providerNameList"]
    userRandom = Data["userRandom"]
    score = Data["score"]
    sorted_score = Data["sortedScore"]
    ideal_score = Data["idealScore"]
    item_ProducerNameList = Data["item_ProducerNameList"]
    m = Data["m"]
    n = Data["n"]
    providerNum = Data["providerNum"]
#global value
    itemExposureList=[0 for x in range(n)]
    userList=[x for x in range(m)]
    userSatisfactionList=[0 for x in range(m)]
    providerExposureList=[0 for x in range(providerNum)]
    recomResults=getRecomendationListOffLine(userList,BaseLineName,sorted_score,K,itemExposureList,score)
    computeExposureAndSatis(recomResults,providerExposureList,userSatisfactionList,ideal_score,score,providerNameList,item_ProducerNameList)
    row = []
    row.append(K)
    row.append(FairSortUtils.getVar(userSatisfactionList))
    row.append(FairSortUtils.getDiverse(userSatisfactionList))
    row.append(sum(userSatisfactionList))
    rateQualityList=FairSortUtils.getProducerExposurCoversionRate(providerExposureList,0,providerSizeList,providerQualityList)
    rateSizeList=FairSortUtils.getProducerExposurCoversionRate(providerExposureList,1,providerSizeList,providerQualityList)
    qualityFairIndex=FairSortUtils.getVar(rateQualityList)
    UniformFairIndex=FairSortUtils.getVar(rateSizeList)
    row.append(qualityFairIndex)
    print("******qualityFairIndex:******：", qualityFairIndex)
    row.append(FairSortUtils.getDiverse(rateQualityList))
    row.append(UniformFairIndex)
    print("******UniformFairIndex:******：", UniformFairIndex)
    row.append(FairSortUtils.getDiverse(rateSizeList))
    writer.writerow(row)

    print("Current K:")
    print("providerExposureList：", providerExposureList)
    print("rateSizeList:",
          FairSortUtils.getProducerExposurCoversionRate(providerExposureList, 1, providerSizeList,
                                                providerQualityList))
    print("rateQualityList:",
          FairSortUtils.getProducerExposurCoversionRate(providerExposureList, 0, providerSizeList,
                                                providerQualityList))
    print("userSatisfaction:",userSatisfactionList)

if __name__ == '__main__':
    writer = writeCsvTitleOffLine("google", "CP_Fair_Offline")
    for K in range(2,26):
        testBaseLineOffLine("google","CP_Fair_Offline",K,writer)