import math
# import random
# import numpy as np
# arr=[0 for x in range(3000)]
# sum=30000
# count=0
# for index in range(3000):
#     if (index == 2999 or sum<100):
#         arr[index]=sum
#         sum-=sum
#         break
#     else:
#         arr[index]=random.randint(0,40)
#         sum-=arr[index]
#
# for index in range(3000):
#     if(arr[index]==0):
#         count+=1
# arr2=[0 for x in range(3000)]
# l=0
# for k in range(3000):
#     if(k%2==0):
#         arr2[k]=20
#         l+=arr2[k]
# j=0
# for index in range(3000):
#     if(arr2[index]==0):
#         j+=1
# print(l)
# print("arr1 0 个数：",count)
# print("arr2 0 个数：",j)
# print(arr)
# print(arr2)
# print(np.var(arr))
# print(np.var(arr2))

import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

plt.plot(x, y)
plt.show()


