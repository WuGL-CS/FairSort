import random
arr=[1,2,35,12,13,43,123,45]
half=arr[0:2]
randomHalf=random.sample(list(arr[2:]),int(4-2))
print(half+randomHalf)