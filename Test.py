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
# import  numpy as np
# score = np.array([[1.0,1.0],[1.0,1.0]])
# score_true=np.copy(score)
# for index in range(len(score)):
#     score[index] = (score[index] / (max(score[index]) * 1000))
# print(score)
# print(score_true)

#asda

# import random
#
# # 原始列表
# original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
# # 设置随机数种子
# seeds = [42, 100, 1234, 2024, 5555]
#
# # 用不同的随机数种子打乱列表
# shuffled_lists = []
#
# for seed in seeds:
#     random.seed(seed)  # 设置随机种子
#     shuffled_list = original_list[:]  # 复制列表
#     random.shuffle(shuffled_list)  # 打乱列表
#     shuffled_lists.append(shuffled_list)  # 将打乱后的列表添加到结果列表中
#
# # 打印结果
# for i, shuffled_list in enumerate(shuffled_lists):
#     print(f"Seed {seeds[i]}: {shuffled_list}")
import numpy as np

import ast
import pandas as pd
from FairSort_OffLine import  FairSort_Utils as Utils
# 1. 读取 CSV 文件
df = pd.read_csv('BaseLine\\Results\\OffLine\\amazon\\FairRecOffLine.csv')

# 2. 删除指定列并保存该列数据
# column_data1 = df.pop('Rate_QF')
# print(np.var(ast.literal_eval(column_data1[3])))
# column_data2 = df.pop('Rate_UF')
# print(np.var(ast.literal_eval(column_data2[3])))
# column_data3= df.pop("NDCG_distribution")
# print(column_data3)
# 3. 对列数据进行运算 (这里是示例，可以换成你的实际运算)
# results=[]
# for data in column_data1:
#     try:
#         results.append(Utils.calculate_Inequality_Producer_Exposure(ast.literal_eval(data)))  # 假设进行乘以2的运算
#
#     except (ValueError, SyntaxError):
#         print(f"无法将字符串 '{data}' 转换为数组")
#
#
# # 4. 重新插入计算后的列
# df['Inequality in Producer Exposure(QF)'] = results
# results=[]
# for data in column_data2:
#     try:
#         results.append(Utils.calculate_Inequality_Producer_Exposure(ast.literal_eval(data)))  # 假设进行乘以2的运算
#
#     except (ValueError, SyntaxError):
#         print(f"无法将字符串 '{data}' 转换为数组")
#
#
# # 4. 重新插入计算后的列
# df['Inequality in Producer Exposure(UF)'] = results
# results=[]
# for data in column_data3:
#     try:
#         results.append(Utils.calculate_envy(ast.literal_eval(data)))  # 假设进行乘以2的运算
#
#     except (ValueError, SyntaxError):
#         print(f"无法将字符串 '{data}' 转换为数组")
#
#
# # 4. 重新插入计算后的列
# df['Mean Average Envy'] = results
# # 5. 保存修改后的 CSV 文件
df.to_csv('BaseLine\\Results\\OffLine\\google\\FairRecOffLine_new_new_me.csv', index=False)