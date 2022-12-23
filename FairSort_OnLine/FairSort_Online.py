import math
from FairSort_OffLine import FairSort_Utils as Utils
import numpy as np
def refreshExposureAlloaction(produceExposure, ReRankList_userTemp, sorted_score,K,
        user_temp,item_ProducerNameList,index_ProducerNameList):
    for index in range(K):
        #撤回原有Top_K列表的曝光资源
        item_Original=sorted_score[user_temp][index]
        item_ProduceName=item_ProducerNameList[item_Original]
        item_Producer_index=index_ProducerNameList.index(item_ProduceName)
        produceExposure[item_Producer_index]-=1/math.log(2+index,2)
        #重新分配给重排序后所在位置的物品
        item_Rerank=ReRankList_userTemp[index]
        item_ProduceName=item_ProducerNameList[item_Rerank]
        item_Producer_index = index_ProducerNameList.index(item_ProduceName)
        produceExposure[item_Producer_index] += 1 / math.log(2 + index, 2)

def getReSortNDCG(score, λ_temp, F,IDCG,user_temp,ReRankList,item_num,K,
                  item_ProducerNameList,index_ProducerNameList):
    ReRankList_score=dict()#用于计算重排物品的分数数据
    for item in ReRankList :
        producer_index=index_ProducerNameList.index(item_ProducerNameList[item])
        ReRankList_score[item]=score[user_temp][item]+λ_temp*F[producer_index]
    #检查是否从小到大排序
    ReRankList.sort(key=lambda x: ReRankList_score[x], reverse=True)
    #开始计算重排序后的NDCG值
    DCG=0
    for index in range(K):
        DCG+=score[user_temp][ReRankList[index]]*1/math.log(2+index,2)
    NDCG=DCG/IDCG
    return NDCG

def FairSortForUser(user_temp, λ,userIDCG, F,score, sorted_score, NDCG_low_bound, K,gap,ratio,item_ProducerNameList,index_ProducerNameList):
    item_num=len(score[user_temp])
    ReRankList=[]#重新排序列表
    ReRankList_length=math.floor(len(sorted_score[user_temp])*ratio)
    for index in range(ReRankList_length):
        ReRankList.append(sorted_score[user_temp][index])#获取了重排列表
    # IDCG =0
    # #计算当前用户的IDCG值
    # for index in range(K):
    #     item_temp=sorted_score[user_temp][index]
    #     IDCG+=score[user_temp][item_temp]*1/math.log(index+2,2)
    target_λ = -1
    left = 0
    right = λ
    equalBoolean=False#也就是说,下面的二分查找没有找到相等的目标NDCG值
    #值得思考一下，如何控制二分查找其最后输出的NDCG，不但逼近其阈值（要求值），也不小于其阈值（要求值）
    count=0
    while (right-left>gap):
        count+=1
        λ_temp = (left + right) / 2
        # print("当前力度：" + str(λ_temp))
        ReSort_NDCG = getReSortNDCG(score, λ_temp, F,userIDCG,user_temp,ReRankList,item_num,K,
                                    item_ProducerNameList,index_ProducerNameList)
        # print("作用后NDCG" + str(ReSort_NDCG))
        if (ReSort_NDCG == NDCG_low_bound):
            target_λ=λ_temp
            equalBoolean=True
            break
        elif (ReSort_NDCG < NDCG_low_bound):
            right = λ_temp
        else:
            left = λ_temp
    print("当前：" + str(user_temp) + "二分查找了" + str(count) + "次")
    if( not equalBoolean ):
        # target_λ=(left+right)/2
        target_λ=left
        # target_λ=right
    #再将搜到的target_λ进行重新排序，并返回NDCG值
    print("当前用户："+str(user_temp)+"确定的λ大小为："+str(target_λ))
    ReSort_NDCG = getReSortNDCG(score, target_λ, F,userIDCG,user_temp,ReRankList,item_num,K,item_ProducerNameList,index_ProducerNameList)
    return (ReSort_NDCG,ReRankList[:K])

def getFairliftFactorAndVar_Rate1(producerExposure_TopK, fair_exposure,fairRegulation,producer_quality,producerSize):
    up_Sum = 0#
    down_Sum = 0
    rateErr = []
    for index in range(len(fair_exposure)):
        temp = fair_exposure[index] - producerExposure_TopK[index]
        if (temp < 0):
            if(fairRegulation==0):
                rateErr_temp=temp / producer_quality[index]
                down_Sum += rateErr_temp
                rateErr.append(rateErr_temp)
            elif(fairRegulation==1):
                rateErr_temp = temp / producerSize[index]
                down_Sum += rateErr_temp
                rateErr.append(rateErr_temp)
        else:
            if (fairRegulation == 0):
                rateErr_temp = temp / producer_quality[index]
                up_Sum += rateErr_temp
                rateErr.append(rateErr_temp)
            elif (fairRegulation == 1):
                rateErr_temp = temp / producerSize[index]
                up_Sum += rateErr_temp
                rateErr.append(rateErr_temp)
    # print("当前的曝光资源差额值" + str(err) + "当前曝光资源相对于公平分配的方差：" + str(err_var))
    for index in range(len(rateErr)):
        if (rateErr[index] > 0):
            rateErr[index] /= up_Sum
        elif (rateErr[index] < 0):
            rateErr[index] /= abs(down_Sum)
    FairliftFactor = rateErr
    return FairliftFactor

def FairSortOnLine (λ,ratio,gap,NDCG_LowBound,K,score,sorted_score,qualityOrUniform,\
                    user_Random,item_ProducerList,producerClassName,writer):
    m=len(score) #user_Num
    n=len(score[0])#item_Num
    UserIDCGList=[0 for x in range(m)]#计算用户的IDCG值
    for user_temp in range(m):
        for rank_temp in range(K):
            item_temp = sorted_score[user_temp][rank_temp]
            UserIDCGList[user_temp] += score[user_temp][item_temp] / math.log((rank_temp + 2), 2)
    item_ProducerNameList=item_ProducerList[producerClassName]

    Exposure_Single_Time=0#计算每次用户请求带来的曝光资源量
    for rank_temp in range(K):
        Exposure_Single_Time+=1/ math.log((rank_temp + 2), 2)

    index_ProducerNameList = []
    provider_SizeList = []
    # 计算index_ProducerNameList[] & providerSize[]
    grouped_ticket = item_ProducerList.groupby(([producerClassName]))
    for group_name, group_list in grouped_ticket:
        index_ProducerNameList.append(group_name)
        provider_SizeList.append(len(group_list))
    #初始化satisDistributeList
    satisDistributeList=[0 for x in range(9)]

    #初始化producer_qualityList:
    producer_qualityList=[0 for x in range(len(index_ProducerNameList))]

    #初始化Fair_ExposureList and producerExposureList
    Fair_ExposureList=[0 for x in range(len(index_ProducerNameList))]
    producerExposureList=[0 for x in range(len(index_ProducerNameList))]

    userAvgSatisfactionList=[0 for x in range(m)]#用户的平均满意度列表
    userAvgSatisfactionTotal=0 #用户的平均满意度列表总和
    userRecomendTimeList=[0 for x in range(m)]#用户被推荐次数列表
    satisfactionTotal=0 #推荐列表的满意度总和

    producerQualitySum=0
    #算法开始：
    for round_temp in range(len(user_Random)):
        print("当前第"+str(round_temp)+"个用户请求到达:")
        userTemp=user_Random[round_temp]
        userIDCG=UserIDCGList[userTemp]
        if(qualityOrUniform==0):#价值
            for rank_temp in range(n):
                item_temp = sorted_score[userTemp][rank_temp]
                provider_name_temp = item_ProducerList[producerClassName][item_temp]
                provider_temp = index_ProducerNameList.index(provider_name_temp)
                producer_qualityList[provider_temp] += score[userTemp][item_temp]
                producerQualitySum+=score[userTemp][item_temp]

                #Equals+<===>
                # itemScore=score[userTemp][rank_temp]
                # provider_name_temp = item_ProducerList[producerClassName][item_temp]
                # provider_temp = index_ProducerNameList.index(provider_name_temp)
                # producer_qualityList[provider_temp] += itemScore
        #开始更新Fair_ExposureList:
        if(qualityOrUniform==0):
            for index in range(len(Fair_ExposureList)):
                Fair_ExposureList[index]=((Exposure_Single_Time*(round_temp+1))/producerQualitySum)*producer_qualityList[index]
        elif(qualityOrUniform==1):
            for index in range(len(Fair_ExposureList)):
                Fair_ExposureList[index]=((Exposure_Single_Time*(round_temp+1))/n)*provider_SizeList[index]
        #更新producer_Exposure:(Top-K分配):
        for rank in range(K):
            item_temp=sorted_score[userTemp][rank]#这里曾经有个致命的BUG
            producerName=item_ProducerList[producerClassName][item_temp]
            producerIndex=index_ProducerNameList.index(producerName)
            producerExposureList[producerIndex]+=1/math.log((rank+2),2)
        #调用启发函数获取启发因子！
        liftFactor=getFairliftFactorAndVar_Rate1(producerExposureList,Fair_ExposureList,qualityOrUniform,producer_qualityList,provider_SizeList)
        #寻找自适应的λ牺牲推荐质量重排序并
        result=FairSortForUser(userTemp,λ,userIDCG,liftFactor,score,sorted_score,NDCG_LowBound,K,gap,ratio,item_ProducerNameList,index_ProducerNameList)
        userSatisTemp=result[0] #用户获得的推荐列表质量
        reRankList=result[1]#重新排序的列表
        print("当前用户："+str(userTemp)+",获得推荐列表NDCG：=========>"+str(result[0]))
        #重新分配资源：
        refreshExposureAlloaction(producerExposureList,reRankList,sorted_score,K,userTemp,item_ProducerNameList,index_ProducerNameList)
        Utils.getSatisfactionDistribution2(userSatisTemp, satisDistributeList)
        userAvgSatisfactionTotal -= userAvgSatisfactionList[userTemp]
        userAvgSatisfactionList[userTemp] = (userAvgSatisfactionList[userTemp] * userRecomendTimeList[
            userTemp] + userSatisTemp) / (userRecomendTimeList[userTemp] + 1)
        userAvgSatisfactionTotal += userAvgSatisfactionList[userTemp]
        satisfactionTotal += userSatisTemp
        userRecomendTimeList[userTemp] += 1

        provider_exposure_num_rate = Utils.getProducerExposurCoversionRate(producerExposureList,1,provider_SizeList,producer_qualityList)
        provider_exposure_quality_rate = Utils.getProducerExposurCoversionRate(producerExposureList,0,provider_SizeList,producer_qualityList)


        diverse_satisfaction=Utils.getStandardDeviation(userAvgSatisfactionList)
        diverse_exposure_score=Utils.getStandardDeviation(provider_exposure_num_rate)
        divers_exposure_quality=Utils.getStandardDeviation(provider_exposure_quality_rate)

        # save result analyze
        row = []
        row.append(round_temp)
        row.append(np.var(userAvgSatisfactionList))
        row.append(diverse_satisfaction)
        row.append(satisfactionTotal)
        if (qualityOrUniform == 1):
            row.append(np.var(provider_exposure_num_rate))
            print("******公平性指标******：", np.var(provider_exposure_num_rate))
            row.append(diverse_exposure_score)
        if(qualityOrUniform == 0):
            row.append(np.var(provider_exposure_quality_rate))
            print("******公平性指标******：", np.var(provider_exposure_quality_rate))
            row.append(divers_exposure_quality)
        row.append(satisDistributeList)
        print("NDCG分布:",satisDistributeList)
        print("提升因子:",liftFactor)
        print("曝光资源公平分配值:",Fair_ExposureList)
        print("提供商当前拥有的曝光资源:",producerExposureList)
        print("曝光分配差额值:",Utils.getFairAndCurrentErr(producerExposureList,Fair_ExposureList))
        if(qualityOrUniform==1):
            if(len(provider_exposure_num_rate)<1000):
                row.append(provider_exposure_num_rate)
        elif(qualityOrUniform==0):
            if(len(provider_exposure_quality_rate)<1000):
                row.append(provider_exposure_quality_rate)
        if(round_temp==len(user_Random)-1):
            print("算法结束了：")
            print("提供商的最终公平曝光值应为：",Fair_ExposureList)
            print("提供商最终的曝光资源分配值为：",producerExposureList)
            print("曝光资源差额值为:",Utils.getFairAndCurrentErr(producerExposureList,Fair_ExposureList))
            print("转化率分布为:",Utils.getProducerExposurCoversionRate(producerExposureList,qualityOrUniform,provider_SizeList,producer_qualityList))
        writer.writerow(row)
if __name__ == '__main__':
    pass