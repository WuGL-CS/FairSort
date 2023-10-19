# arr=[-38.91743638022126, -0.31145238351474447, -2.035566188607662, 8.020714077113553, 11.961869528229727, -1.3230697739958686, -1.7190862855017457, -0.29569623050168303, 20.67785462007305, -0.4149497350213771, -0.6257191524534083, -15.527941215177634, -2.4343566834550785, 7.431860795266402, 4.472267874220336, 11.040703993833631]
# print(sum(arr))
#
# #asdasd
# import  random
# import numpy as np
# #Test Function
# def getValue(score,totalUsers,totalItems,topK,top_k):
#     # totalUsers—————>UFlag：
#
#     UFlag=np.zeros((totalUsers,2))
#     for index in range(totalUsers): UFlag[index][1]=1 # [1]:inactive   [0]:active
#     user=[i  for i in range(totalUsers)]
#     random.seed(10)
#     random.shuffle(user)
#     active_User=user[0:int(totalUsers*0.2)]
#     for index in active_User:
#         UFlag[index][0]=1
#         UFlag[index][1]=0
#
#     # score：—————>itemFlag：
#     itemFlag=np.zeros((totalItems,topK,2))
#     itemFlag[:,:,1]=1  # inactive item
#     itemScore=[0 for index in range(totalItems)]
#     for index in range(totalItems):
#         itemScore[index]=np.mean(score[:,index])
#     activeItem=list(reversed(np.array(itemScore).argsort()))[0:int(totalItems*0.05)]
#     P = np.ndarray((totalUsers, topK))#P 会自己提供，不需要造
#
#     item=[item for item in range(totalItems)]
#     for user in range(totalUsers):
#         random.shuffle(item)
#         P[user,:] = item[0:topK]
#         for topK_index in range(topK):
#             if P[user][topK_index] in activeItem:
#                 itemFlag[user][topK_index][0]=1
#                 itemFlag[user][topK_index][1] = 0
#
# #—————>Ahelp：这个逻辑是：平等性破坏active和inactive的推荐列表质量的逻辑
#     # Ahelp=np.zeros((totalUsers,topK))
#     # for user in range(totalUsers):
#     #         if user in active_User:
#     #             Ahelp[user,top_k:2*top_k]=1
#     #         else:
#     #             Ahelp[user,0:top_k]=1
# #这个逻辑是：破坏 active 推荐质量，提高inactive 的推荐质量
#     Ahelp = np.zeros((totalUsers, topK))
#     Ahelp[:, top_k: ] = 1
#
# print("sad")
# score=np.random.randint(1, 6, size=(100, 100))
# getValue(score,100,100,8,4)
#
#
#
#         #score：—————>itemFlag：
#
#
import  numpy as np
score = np.array([[1.0,1.0],[1.0,1.0]])
score_true=np.copy(score)
for index in range(len(score)):
    score[index] = (score[index] / (max(score[index]) * 1000))
print(score)
print(score_true)