import math
import random
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





