import math
import random

import numpy
import numpy as np
#userId:current services user
#sortedScore:recommendationList
#执行逻辑：
#     获取当前最需要扶贫的
# minimumExposure_OnLine
def minimumExposure_OnLine(itemExposureList,K):
    result=np.argsort(itemExposureList) #get the list which item ranking by the exposure gained by them(min——>large)
    recommendationList=result[0:K]
    #update itemExposure
    for index in range(K):
        item=recommendationList[index]
        itemExposureList[item]+=1/math.log(2+index,2)
    return recommendationList
# minimumExposure_OffLine()
def minimumExposure_OffLine(userList,K,itemExposureList):
    recommdationList= {}
    for user_Temp in userList:
        recommdationList[user_Temp]=[-1 for x in range(K)]
    for k_temp in range(K):
        for user_Temp in userList:
            result = np.argsort(itemExposureList)  # get the list which item ranking by the exposure gained by them(min——>large)
            for itemTemp in result:
                if(itemTemp not in recommdationList[user_Temp]):
                    recommdationList[user_Temp][k_temp] = itemTemp
                    itemExposureList[itemTemp] += 1 / math.log(2 + k_temp, 2)
                    break
    return recommdationList

#Mixed_k :OnLine Version
def Mixed_k_OnLine(userId,sorted_Score,K):
    halfLength=int(math.ceil((K+0.0)/2))
    half=list(sorted_Score[userId][0:halfLength])
    randomHalf=random.sample(list(sorted_Score[userId][halfLength:]),int(K-halfLength))
    return half+randomHalf
#Mixed_k :OffLine Version
def Mixed_k_Offline(userList,sorted_Score,K):
    A={}
    for userTemp in userList:
        A[userTemp]=Mixed_k_OnLine(userTemp,sorted_Score,K)
    return A


#Top-K OnLine Version
def Top_K_Online(userId,sorted_Score,K):
    return sorted_Score[userId][0:K]

#Top-K OffLine Version
def Top_K_Offline(userList,sorted_Score,K):
    A={}
    for userTemp in userList:
        A[userTemp]=Top_K_Online(userTemp,sorted_Score,K)
    return A

#Random_k :OnLine Version
def Random_k_Online(userId,sorted_Score,K):
   return random.sample(list(sorted_Score[userId]),K)
#Random_k :OffLine Version
def Random_k_Offline(userList,sorted_Score,K):
    A={}
    for userTemp in userList:
        A[userTemp]=Random_k_Online(userTemp,sorted_Score,K)
    return A

#FairRec:which is the offLine Version and just have this Version
def greedy_round_robin(m, n, R, l, T, V, U, F):
    # greedy round robin allocation based on a specific ordering of customers (assuming the ordering is done in the relevance scoring matrix before passing it here)

    # creating empty allocations
    B = {}
    for u in U:
        B[u] = []

    # available number of copies of each producer
    Z = {}  # total availability
    P = range(n)  # set of producers
    for p in P:
        Z[p] = l

    # allocating the producers to customers
    for t in range(1, R + 1):
        print("GRR round number==============================", t)
        for i in range(m):
            if T == 0:
                return B, F
            u = U[i]
            # choosing the p_ which is available and also in feasible set for the user
            possible = [(Z[p] > 0) * (p in F[u]) * V[u, p] for p in range(n)]
            p_ = np.argmax(possible)

            if (Z[p_] > 0) and (p_ in F[u]) and len(F[u]) > 0:
                B[u].append(p_)
                F[u].remove(p_)
                Z[p_] = Z[p_] - 1
                T = T - 1
            else:
                return B, F
    # returning the allocation
    return B, F;


def FairRecOffLine(U, P, k, V, alpha):
    # Allocation set for each customer, initially it is set to empty set
    m=len(U)
    n=len(P)
    A = {}
    for u in U:
        A[u] = []

    # feasible set for each customer, initially it is set to P
    F = {}
    for u in U:
        F[u] = P[:]
    # print(sum([len(F[u]) for u in U]))

    # number of copies of each producer
    l = int(alpha * m * k / (n + 0.0))

    # R= number of rounds of allocation to be done in first GRR
    R = int(math.ceil((l * n) / (m + 0.0)))

    # total number of copies to be allocated
    T = l * n

    # first greedy round-robin allocation
    [B, F1] = greedy_round_robin(m, n, R, l, T, V, U[:], F.copy())
    F = {}
    F = F1.copy()
    print("GRR done")
    # adding the allocation
    for u in U:
        A[u] = A[u][:] + B[u][:]

    # second phase
    u_less = []  # customers allocated with <k products till now
    for u in A:
        if len(A[u]) < k:
            u_less.append(u)

    # allocating every customer till k products
    for u in u_less:
        scores = V[u, :]
        new = scores.argsort()[-(k + k):][::-1]
        for p in new:
            if p not in A[u]:
                A[u].append(p)
            if len(A[u]) == k:
                break

    return A


#CP-FairModel：Offline Version

#进行参数的简约：
    #P的计算放入内部：
def CP_Fair_Offline(score,sorted_Score,top_k,topK,groupNum,totalUsers,totalItems,fair_mode,λ1=0,λ2=0):
    A={}
    P=numpy.ndarray((totalUsers,topK),dtype=int)
    for user in range(totalUsers):
        P[user]=sorted_Score[user][0:topK]
    print(f"Runing fairness optimisation on '{fair_mode}', {format(λ1, 'f')}, {format(λ2, 'f')}")
    #获取itemFactor
    W=np.zeros((totalUsers,topK))#线性规划的系数矩阵
    W_result=np.zeros((totalUsers,topK))#规划后的结果矩阵
    item_groups=np.zeros(groupNum)
    # totalUsers—————>UFlag：

    UFlag = np.zeros((totalUsers, groupNum))
    for index in range(totalUsers): UFlag[index][1] = 1  # [1]:inactive   [0]:active
    user = [i for i in range(totalUsers)]
    random.seed(10)
    random.shuffle(user)
    active_User = user[0:int(totalUsers * 0.2)]
    for index in active_User:
        UFlag[index][0] = 1
        UFlag[index][1] = 0

    # score：—————>itemFlag：
    itemFlag = np.zeros((totalItems, topK, groupNum))
    itemFlag[:, :, 1] = 1  # inactive item
    itemScore = [0 for index in range(totalItems)]
    for index in range(totalItems):
        itemScore[index] = np.mean(score[:, index])
    activeItem = list(reversed(np.array(itemScore).argsort()))[0:int(totalItems * 0.05)]

    for user in range(totalUsers):
        for topK_index in range(topK):
            if P[user][topK_index] in activeItem:
                itemFlag[user][topK_index][0] = 1
                itemFlag[user][topK_index][1] = 0

    # —————>Ahelp：这个逻辑是：平等性破坏active和inactive的推荐列表质量的逻辑
    # Ahelp=np.zeros((totalUsers,topK))
    # for user in range(totalUsers):
    #         if user in active_User:
    #             Ahelp[user,top_k:2*top_k]=1
    #         else:
    #             Ahelp[user,0:top_k]=1
    # 这个逻辑是：破坏 active 推荐质量，提高inactive 的推荐质量
    Ahelp = np.zeros((totalUsers, topK))
    Ahelp[:, top_k:] = 1

    for i in range(totalUsers):
        if UFlag[i][0] == 1:
           u_λ= λ1
        else:
           u_λ = -λ1
        for j in range(topK):
            userFair = u_λ * Ahelp[i][j]

            if itemFlag[i][j][0] == 1:
                itemFair=-λ2
            else:
                itemFair= λ2
            if fair_mode == "N":
                W[i][j]+=score[i][int(P[i][j])] #线性综合指标
            elif fair_mode == 'C':
                W[i][j]+=score[i][int(P[i][j])] + userFair #线性综合指标
            elif fair_mode == "P":
                W[i][j] += score[i][int(P[i][j])] + itemFair  # 线性综合指标
            elif fair_mode=='CP':
                W[i][j] += score[i][int(P[i][j])] + userFair +itemFair # 线性综合指标

    for i in range(totalUsers):
        for item_topK_index in list(reversed(W[i].argsort()))[:top_k]:
            W_result[i][item_topK_index ]=1 #悠哉悠哉地挑物品
            itemgroup= 0 if itemFlag[i][item_topK_index][0]==1 else 1 #计算该物品对应的组
            item_groups[itemgroup]+=1 #挑上物品，累积对应组的曝光获得量
    for user in range(totalUsers):
        selectedItemList=P[user][W_result[user]==1]
        A[user]=selectedItemList
    return A


