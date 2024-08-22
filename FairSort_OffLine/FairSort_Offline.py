import csv
import FairSort_Utils as Utils
import math
import  numpy as  np

#返回重排后的较优NDCG值以及排序列表
#K:排序列表>=0 #gap:拉姆达查找的精确度 #user_temp:用户id  #λ:响应公平诉求的力度 #F:各个提供商遭遇不公平的力度
#score:推荐算法计算给到的用户喜好分数矩阵 #sorted_score：全体排序列表  #NDCG_low_bound:NDCG值的下界约束
#gap:λ搜索精度要求:>0  #item_List:物品集（记录各个物品的属性） #提供商的名称信息和ID映射表 #ratio:基于多大的列表比例重排[0,1]
#函数计算逻辑:
    #这个函数的功能是，给到一个待重排序的物品集，然后相应计算信息给到，
    #其动作逻辑便是：每调用一次，就是对待排序物品重新排了一下，并返回Top K NDCG值
def getReSortNDCG(score, λ_temp, F,IDCG,user_temp,ReRankList,item_num,K,
                  item_ProducerNameList,index_ProducerNameList):
    ReRankList_score=dict()#用于计算重排物品的分数数据
    for item in ReRankList :
        producer_index=index_ProducerNameList.index(item_ProducerNameList[item])
        ReRankList_score[item]=score[user_temp][item]+λ_temp*F[producer_index]
    # print("ReRankList_score")
    # print(ReRankList_score)
    # print("ReRankList")
    #检查是否从小到大排序
    ReRankList.sort(key=lambda x: ReRankList_score[x], reverse=True)
    # print(ReRankList)
    #开始计算重排序后的NDCG值
    DCG=0
    for index in range(K):
        DCG+=score[user_temp][ReRankList[index]]*1/math.log(2+index,2)
    NDCG=DCG/IDCG
    return NDCG

#该函数的参数说明：
    #produceExposure:[1*l]:当前各个提供商的曝光资源分配情况,#ReRankList_userTemp:当前用户的重排列表
    #sorted_score:这个可以映射其原有的Top_K列表 #K：不必多说，就是Top-K的个数
#该函数的计算逻辑：
    #为每个提供商的曝光资源重新刷新,因为重排序了，所以基于新的排序结果进行曝光资源的更新
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

#上面做法指标不治本，现在考虑转化率:有差别地前后跑,归一化
def getFairliftFactorAndVar_Rate1(producerExposure_TopK, fair_exposure,fairRegulation,producer_quality,producerSize):
    err = []
    up_Sum = 0#
    down_Sum = 0
    rateErr = []
    for index in range(len(fair_exposure)):
        temp = fair_exposure[index] - producerExposure_TopK[index]
        err.append(temp)
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
    err = np.array(err)
    err_var = np.var(err)
    # print("当前的曝光资源差额值" + str(err) + "当前曝光资源相对于公平分配的方差：" + str(err_var))
    for index in range(len(rateErr)):
        if (rateErr[index] > 0):
            rateErr[index] /= up_Sum
        elif (rateErr[index] < 0):
            rateErr[index] /= abs(down_Sum)
    FairliftFactor = rateErr
    return (FairliftFactor, err_var)

#治本！！且有差别前后跑，但是 不归一化
def getFairliftFactorAndVar_Rate2(producerExposure_TopK, fair_exposure,fairRegulation,producer_quality,producerSize):
    err = []
    up_Sum = 0#
    down_Sum = 0
    rateErr = []
    for index in range(len(fair_exposure)):
        temp = fair_exposure[index] - producerExposure_TopK[index]
        err.append(temp)
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
    err = np.array(err)
    err_var = np.var(err)
    # print("当前的曝光资源差额值" + str(err) + "当前曝光资源相对于公平分配的方差：" + str(err_var))
    FairliftFactor = rateErr
    return (FairliftFactor, err_var)

###以下函数的执行逻辑：FairSortForUser()
#   (user_temp, λ, F,score, sorted_score, NDCG_low_bound, k,gap,ratio)
#           告诉我哪个用户user_temp,公平重视力度因子λ最大值,以及计算信息（score喜好信息，F公平信息，sorted_score最初排序列表)
#           计算逻辑为：给一个用户，拿到其最原始推荐列表sorted_List，取ratio个重排物品，基于F公平提升因子
#                     迭代出当前的最佳λ：公平注意力力度，从而获得靠近NDCG_low_bound的NDCG列表，gap为λ精确值
def FairSortForUser(user_temp, λ, F,score, sorted_score, NDCG_low_bound, K,gap,ratio,item_ProducerNameList,index_ProducerNameList):
    item_num=len(score[user_temp])
    ReRankList=[]#重新排序列表
    ReRankList_length=math.floor(len(sorted_score[user_temp])*ratio)
    for index in range(ReRankList_length):
        ReRankList.append(sorted_score[user_temp][index])#获取了重排列表
    IDCG =0
    #计算当前用户的IDCG值
    for index in range(K):
        item_temp=sorted_score[user_temp][index]
        IDCG+=score[user_temp][item_temp]*1/math.log(index+2,2)
    target_λ = -1
    left = 0
    right = λ
    count=0
    equalBoolean=False#也就是说,下面的二分查找没有找到相等的目标NDCG值
    #值得思考一下，如何控制二分查找其最后输出的NDCG，不但逼近其阈值（要求值），也不小于其阈值（要求值）
    count=0
    while (right-left>gap):
        count+=1
        λ_temp = (left + right) / 2
        # print("当前力度：" + str(λ_temp))
        ReSort_NDCG = getReSortNDCG(score, λ_temp, F,IDCG,user_temp,ReRankList,item_num,K,
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
    # print("当前：" + str(user_temp) + "二分查找了" + str(count) + "次")
    if( not equalBoolean ):
        # target_λ=(left+right)/2
        target_λ=left
        # target_λ=right
    #再将搜到的target_λ进行重新排序，并返回NDCG值
    ReSort_NDCG = getReSortNDCG(score, target_λ, F,IDCG,user_temp,ReRankList,item_num,K,item_ProducerNameList,index_ProducerNameList)
    print("当前用户："+str(user_temp)+"确定的λ大小为："+str(target_λ)+" Recommendation Quality:" +str(ReSort_NDCG))
    return (ReSort_NDCG,ReRankList[:K])


# 函数参数说明：FairSortForTheWhole()
#              userList, λ,score, sorted_score,ratio, K, NDCG_low_bound,gap,
#              item_ProducerNameList,index_ProducerNameList,
#              providerSize,provider_quality
#              force=[1,+∞]:也就是公平诉求的差异化力度

#              producerClassName:所有提供商类型名，用于映射：item_ProducerNameList=[]

# 函数参数规约:
#           userList, λ,score, sorted_score,ratio, K, NDCG_low_bound,gap,
#              [item_ProducerNameList,index_ProducerNameList,
#              providerSize,provider_quality]=======>归越为item_ProducerList
#              producerClassName:所有提供商类型名，用于映射：item_ProducerNameList=[]
#              fairRegulation:公平规则：0:表示采取价值规则，1:表示采取提供商物品量的规则
#              result_writer:算法结果分析的输出流
# 返回值:应当是：各个用户的Top K排序列表，以及整个过程的信息统计量（公平指标，推荐总满意度，等等)
def FairSortForTheWhole(userList, λ,score, sorted_score,ratio, K, NDCG_low_bound,gap,
             item_ProducerList,producerClassName,fairRegulation,force,dataSetName):
    m=len(userList)#用户的个数信息
#BY  item_ProducerList  ===>d  [item_ProducerNameList,index_ProducerNameList,
#       providerSize,provider_quality]
    index_ProducerNameList=[]
    providerSize=[]
    #计算index_ProducerNameList[] & providerSize[]
    grouped_ticket = item_ProducerList.groupby(([producerClassName]))
    for group_name, group_list in grouped_ticket:
        index_ProducerNameList.append(group_name[0])#BUG:sometimes you should use the group_name[0] or group_name
        providerSize.append(len(group_list))

    provider_size_total = sum(providerSize)
    item_ProducerNameList=item_ProducerList[producerClassName] #计算item_ProducerNameList=[]
    provider_quality = [0 for i in range(len(index_ProducerNameList))]#计算provider_quality[]
    # 下面这个函数负值映射提供商的价值量
    #     遍历user维度和item维度，也就是遍历完所有的评分信息
    # for user_temp in range(m):
    #     for rank_temp in range(len(score[user_temp])):
    #         item_temp = sorted_score[user_temp][rank_temp]#推荐列表里的物品编号
    #         provider_name_temp = item_ProducerList[producerClassName][item_temp]#映射该物品的生产商名字
    #         provider_temp = index_ProducerNameList.index(provider_name_temp)#得到生产商对应的索引
    #         provider_quality[provider_temp] += score[user_temp][item_temp]#加入到生产商的价值矢量里
    #     print('collecting provider_quality ing Now turn user_temp: %d' % (user_temp))
    # 保存变量到文件中：
    # save_value(provider_quality,filePath="../datasets/Temp_Value/TFROM_google_provider_quality.pkl")
    provider_quality = Utils.load_variavle(filename="../datasets/Temp_Value/TFROM_"+dataSetName+"_provider_quality.pkl")
#以上完成了item_ProducerList  ===>d  [item_ProducerNameList,index_ProducerNameList,providerSize,provider_quality]
    #接下来要统计一下当前所有用户的Top-K曝光资源分布情况:
    producerExposure_TopK=[0 for i in range(len(index_ProducerNameList))]
    for user_temp in range(m):
        for rank_temp in range(K):
            item_temp=sorted_score[user_temp][rank_temp]
            item_producerName=item_ProducerNameList[item_temp]
            producer_Index=index_ProducerNameList.index(item_producerName)
            producerExposure_TopK[producer_Index]+=1/math.log((2+rank_temp),2)
    #将这个值赋值给提供商曝光资源分配情况（这个是动态变化的）
    producerExposure = [producerExposure_TopK[i] for i in range(len(index_ProducerNameList))]
    # print("当前系统提供商top-k下的曝光值",producerExposure)
#接下来计算各个提供商曝光资源公平分配值应该是多少！！！！！
    # 计算当前K下，总曝光资源
    total_exposure = 0
    for i in range(K):
        total_exposure += 1 / math.log((i + 2), 2)
    total_exposure = total_exposure * m

    # 计算每个提供商的曝光公平阈值——基于价值量
    fair_exposure = []
    if(fairRegulation==0):
        provider_quality_sum=sum(provider_quality)
        for i in range(len(index_ProducerNameList)):
            fair_exposure.append(total_exposure /provider_quality_sum  * provider_quality[i])
    elif(fairRegulation==1):
        providerSize_sum=sum(providerSize)
        for i in range(len(index_ProducerNameList)):
            fair_exposure.append(total_exposure /providerSize_sum  * providerSize[i])
    # print("当前系统提供商如果公平，应得到的曝光值：",fair_exposure)
    userSatisfaction=[0 for i in range(len(userList))]#同于记录用户的满意度值
    #似乎忘记给producerFairExposure赋值
#上面的所有数据结构准备完毕，下面FairSort算法开始服务:(待思考问题：)
        #这里可以思考一下服务的顺序:不同用户的优先服务顺序！（随机，或者怎么个服务顺序）
#算法执行过程，相应的信息统计量:如下
        #我们统计一下:每5个用户其公平信息熵是否会稳步提升，公平性指标，是否在稳步提升，再确立信息熵阈值
        #用户的满意度总和值user_satisfactionTotal
    user_satisfactionTotal=0
    count=0#当前服务了多少个用户了：当前服务的用户数统计量
    for user_temp in userList:
        count+=1
    #进行公平性启发：
        result=getFairliftFactorAndVar_Rate1(producerExposure,fair_exposure,fairRegulation,provider_quality,providerSize)#这里可以选择其他函数
        FairLiftFactor=result[0]
        # if(result[1]<=10):throw Exception
        #计算当前的提升因子信息熵值，如果达到一定阈值，我们统计其变化规律，是否在递增，值域[0,1]
        # FairLiftFactorInfoEntropy=getFairLiftFactorInfoEntropy(FairLiftFactor)
    #有了公平性启发后的提升因子,进行二分搜索
        #有了提升因子，其实应该看其公平性怎样，再做计划的，但是我们先进行
        RecResult=FairSortForUser(user_temp,λ,FairLiftFactor,score,sorted_score,NDCG_low_bound,K,gap,ratio,item_ProducerNameList,index_ProducerNameList)
        # print("Current exposure error variance: "+str(result[1])+"  Provider_Fair_Index "+str(Utils.getVar(Utils.getProducerExposurCoversionRate(producerExposure,fairRegulation,providerSize,provider_quality)))+"  Recommended_List_Quality:"+str(RecResult[0]))
        userSatisfaction[user_temp]=RecResult[0]
        # print("Current User: " + str(user_temp) +"  The Lift Factor List: " +str(FairLiftFactor))
        user_satisfactionTotal+=RecResult[0]
        ReRankList_userTemp = RecResult[1]
        #对曝光资源进行更新操作！将原有Top-k列表的曝光资源分配情况进行重新调整，牺牲一定的推荐质量，换取提供商公平
        refreshExposureAlloaction(producerExposure, ReRankList_userTemp, sorted_score,K,
                                  user_temp,item_ProducerNameList,index_ProducerNameList)
        # print("Finished Service user："+str(user_temp)+" later,Error between producerExposure and fair_Exposure :",Utils.getFairAndCurrentErr(producerExposure,fair_exposure))
        print("Finished Service user："+str(user_temp)+" later : provider_Fair_Index :"+str(Utils.getVar(
            Utils.getProducerExposurCoversionRate(producerExposure,fairRegulation,providerSize,provider_quality))))

        if(count%10==0):
            print("Total service "+str(count)+" Users"+"  provider_Fair_Index :"+str(Utils.getVar(
            Utils.getProducerExposurCoversionRate(producerExposure,fairRegulation,providerSize,provider_quality))))
            # print("The final exposure resource distribution on the  provider_side is", producerExposure)
            # print("Fair distribution should be(Exposure For Every Provider)：", fair_exposure)
            # print("Error：",Utils.getFairAndCurrentErr(producerExposure,fair_exposure))
#我们要对本轮算法进行结果分析:
    print("The algorithm is over：")
    # print("Tok-K exposure resource distribution is：", producerExposure_TopK)
    # print("The final exposure resource distribution on the  provider_side is",producerExposure)
    # print("Fair distribution should be(Exposure For Every Provider)：",fair_exposure)
    print("The provider's initial top-k Exposure_Quality conversion Rate is:：",Utils.getProducerExposurCoversionRate(producerExposure_TopK,fairRegulation,providerSize,provider_quality))
    print("The final conversion Rate distribution on the provider side is：",Utils.getProducerExposurCoversionRate(producerExposure,fairRegulation,providerSize,provider_quality))
    print("Error between producerExposure_TopK and fair_exposure",Utils.getFairAndCurrentErr(producerExposure_TopK,fair_exposure))
    print("FairSort's error between producerExposure and fair_exposure :",Utils.getFairAndCurrentErr(producerExposure,fair_exposure))
    Utils.getSatisfactionDistribution(userSatisfaction)
    userSatisfaction_var=Utils.getVar(userSatisfaction)
    userSatisfaction_diverse=Utils.getDiverse(userSatisfaction)
    CoversionRate_quality=Utils.getProducerExposurCoversionRate(producerExposure,0,providerSize,provider_quality)
    producer_exposure_quality_var=Utils.getVar(CoversionRate_quality)
    producer_exposure_quality_diverse=Utils.getDiverse(CoversionRate_quality)
    CoversionRate_Size = Utils.getProducerExposurCoversionRate(producerExposure, 1, providerSize, provider_quality)
    producer_exposure_Size_var = Utils.getVar(CoversionRate_Size)
    producer_exposure_Size_diverse = Utils.getDiverse(CoversionRate_Size)
    row = []
    row.append(K)  # K超参数
    row.append(userSatisfaction_var)  # 用户满意度向量的方差
    row.append(userSatisfaction_diverse)  # 满意度的绝对值平均偏移量
    row.append(user_satisfactionTotal)  # 用户总满意度
    if(fairRegulation==1):
        row.append(Utils.getVar(
            Utils.getProducerExposurCoversionRate(producerExposure_TopK, 1, providerSize, provider_quality)))  # 'Top-k_SizeVar'
        row.append(producer_exposure_Size_var)  # 曝光基于物品数转化率的方差
        row.append(producer_exposure_Size_diverse)  # 曝光基于物品数转化率的绝对值偏移
    elif(fairRegulation==0):
        row.append(Utils.getVar(
            Utils.getProducerExposurCoversionRate(producerExposure_TopK, 0, providerSize,
                                            provider_quality)))  # 'Top-k_qualityVar'
        row.append(producer_exposure_quality_var)  # 曝光基于价值的转化率方差
        row.append(producer_exposure_quality_diverse)  ##曝光基于价值的绝对值转化率偏移
    row.append(Utils.getVar(Utils.getFairAndCurrentErr(producerExposure_TopK, fair_exposure)))  # 期初的方差：
    row.append(Utils.getVar(Utils.getFairAndCurrentErr(producerExposure, fair_exposure)))  # 方差力度
    if(dataSetName!='google'):
        row.append(Utils.getProducerExposurCoversionRate(producerExposure_TopK, fairRegulation, providerSize,
                                               provider_quality))  # "Top-K转化率分布"
        row.append(Utils.getProducerExposurCoversionRate(producerExposure, fairRegulation, providerSize,
                                                   provider_quality))  # "FairSort转化率分布"
        row.append(fair_exposure)  # "公平曝光资源分布"
        row.append(Utils.getFairAndCurrentErr(producerExposure_TopK, fair_exposure))  # "Top-K曝光err"
        row.append(Utils.getFairAndCurrentErr(producerExposure, fair_exposure))  # "FairSort曝光err"
        row.append(providerSize)  # "提供商物品数分布"
        row.append(provider_quality)  # "提供商价值量分布"
    return row