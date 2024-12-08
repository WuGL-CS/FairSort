'''
Author: 13543024276 13543024276@163.com
Date: 2024-08-17 13:46:18
LastEditors: 13543024276 13543024276@163.com
LastEditTime: 2024-11-17 19:12:38
FilePath: \FairSort\FairSort_OffLine\Test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import math
import random
import numpy as np
# # arr=[0 for x in range(4927)]
# # sum=4927
# # count=0
# # for index in range(3000):
# #     if (index == 2999 or sum<100):
# #         arr[index]=sum
# #         sum-=sum
# #         break
# #     else:
# #         arr[index]=random.randint(0,40)
# #         sum-=arr[index]
# #
# # for index in range(3000):
# #     if(arr[index]==0):
# #         count+=1
# # arr2=[0 for x in range(3000)]
# # l=0
# # for k in range(3000):
# #     if(k%2==0):
# #         arr2[k]=20
# #         l+=arr2[k]
# # j=0
# # for index in range(3000):
# #     if(arr2[index]==0):
# #         j+=1
# # print(l)
# # print("arr1 0 个数：",count)
# # print("arr2 0 个数：",j)
# # print(arr)
# # print(arr2)
# # print(np.var(arr))
# # print(np.var(arr2))
#
# import matplotlib.pyplot as plt
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# # 定义函数 f(x)
# def f(x):
#     return 1 - np.exp(1 - x)
#
# # 定义函数 f'(x) - 导数
# def df(x):
#     return np.exp(1 - x)
#
# # 生成 x 值
# x = np.linspace(0, 1, 100)
#
# # 计算对应的 y 值
# y = f(x)
# dy = df(x)
#
# # 绘制函数 f(x) 和其导数 f'(x) 的图像
# plt.figure(figsize=(10, 5))
# plt.subplot(1, 2, 1)
# plt.plot(x, y, label='f(x) = 1 - e^{1-x}', color='blue')
# plt.title('f(x)')
# plt.xlabel('x')
# plt.ylabel('f(x)')
# plt.grid(True)
# plt.legend()
#
# plt.subplot(1, 2, 2)
# plt.plot(x, dy, label="f'(x) = e^{1-x}", color='red')
# plt.title("f'(x)")
# plt.xlabel('x')
# plt.ylabel("f'(x)")
# plt.grid(True)
# plt.legend()
#
# plt.show()
# import numpy as np
#

for i in range(5):
    # 原始列表
    np.random.seed(i)
    my_list = [1, 2, 3, 4, 5]

    # 随机打乱列表
    np.random.shuffle(my_list)

    print(my_list)
