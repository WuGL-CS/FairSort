import  numpy as np
import pandas as pd
from FairSort_OffLine import FairSort_Utils as Utils
from FairSort_OnLine import FairSort_Online
import csv as csv
import  time
def SaveResult_WriteTitle_Online(dataset_name,qualityOrUniform):
    fairType=""
    if qualityOrUniform==0:fairType="QF"
    elif(qualityOrUniform==1):fairType="UF"
    fileName="/FairSort_Robust(userRandom)_"+fairType+".csv"
    csvFile = open("../results_Robust/user_random_Robust/" + dataset_name+fileName
                   , 'w', newline='')
    writer = csv.writer(csvFile)
    title = []
    title.append('seed')
    title.append('satisfaction_average')
    title.append('satisfaction_var_average')
    if(qualityOrUniform==0):
        # title.append('Top-k_qualityVar')
        title.append('exposure_quality_var_average')
    elif(qualityOrUniform==1):
        # title.append('Top-k_SizeVar')
        title.append('exposure_var_everage')
    writer.writerow(title)
    return csvFile
#input：
#output:every dataset have a cvs:quality,fairness(bothside)
def FairSort_Online_Robust(DataSet,radomSeeds):
    if DataSet=="ctrip":
        u_num_international = 3814
        t_num_international = 6006

        m = u_num_international
        # m = 100
        n = t_num_international
        # n = 50

        dataset_name = 'ctrip'
        score_file = '/score_international.csv'
        item_file = '/ticket_international.csv'
        # ticket_list:订单表：ID airline classes price
        item_ProducerList = pd.read_csv('../datasets/data_' + dataset_name + item_file)
        # 用户和item的贡献矩阵：评分矩阵
        w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file)
        # 评分矩阵score
        w_score = w_score.iloc[:, 3:]
        score = np.array(w_score)
        score = score[:m, :n]
        # 对分数矩阵进行归一化操作
        score = np.array(w_score.values)
        # score_true=np.copy(score)
        for index in range(len(score)):
            score[index] = (score[index] / (max(score[
                                                    index]) * 10))  # this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
            # and the NDCG ,which can be proof strictly!

        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))
        sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表

        # hyperParameter
        K = 20
        λ = 8
        ratio = 1
        low_bound = 0.9
        gap = 1 / 256
        qualityOrUniform = 0  # Fair appeal: 0 is Quality and 1 is Uniform
        # save result analyze
        csvFile = SaveResult_WriteTitle_Online(dataset_name,qualityOrUniform)
        writer = csv.writer(csvFile)
        t = time.time()
        user_Random = []
        for j in range(10):
            user_Random.extend([user for user in range(m)])
        for seed in radomSeeds:
            # 原始列表
            np.random.seed(seed)
            # 随机打乱列表
            np.random.shuffle(user_Random)
            results_Robust=FairSort_Online.FairSortOnLine(λ, ratio, gap, low_bound, K, score, sorted_score, qualityOrUniform, user_Random,
                                       item_ProducerList, "airline", None, dataset_name)
            results_Robust = [sum(column) / len(column) for column in zip(*results_Robust)]
            writer.writerow([seed]+results_Robust)
        print(f'Time spent:{time.time() - t:.3f}s')
        csvFile.close()
        print('Finished!')
    elif DataSet=="amazon":
        review_number_amazon = 24658
        item_number_amazon = 7538
        user_number_amazon = 1851
        provider_num_amazon = 161

        m = user_number_amazon
        # m = 100
        n = item_number_amazon
        # n = 50

        dataset_name = 'amazon'
        score_file = '/preference_score.csv'
        item_file = '/item_provider.csv'
        # ticket_list:订单表：ID airline classes price
        item_ProducerList = pd.read_csv('../datasets/data_' + dataset_name + item_file)
        # 用户和item的贡献矩阵：评分矩阵
        w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file, header=None)
        # 评分矩阵score
        score = np.array(w_score)
        score = score[:m, :n]
        # 对分数矩阵进行归一化操作
        score = np.array(w_score.values)
        # score_true=np.copy(score)
        for index in range(len(score)):
            score[index] = (score[index] / (max(score[
                                                    index]) * 100))  # this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
            # and the NDCG ,which can be proof strictly!

        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))
        sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表
        user_Random = Utils.load_variavle("../datasets/data_amazon/random_user.pkl")
        # hyperParameter
        K = 20
        λ = 1
        ratio = 0.1
        low_bound = 0.95
        gap = 1 / 256
        qualityOrUniform = 1  # Fair appeal: 0 is Quality and 1 is Uniform
        # save result analyze
        csvFile = SaveResult_WriteTitle_Online(dataset_name, qualityOrUniform)
        writer = csv.writer(csvFile)
        t = time.time()
        user_Random = []
        for j in range(10):
            user_Random.extend([user for user in range(m)])
        for seed in radomSeeds:
            # 原始列表
            np.random.seed(seed)
            # 随机打乱列表
            np.random.shuffle(user_Random)
            results_Robust = FairSort_Online.FairSortOnLine(λ, ratio, gap, low_bound, K, score, sorted_score,
                                                            qualityOrUniform, user_Random,
                                                            item_ProducerList, "provider", None, dataset_name)
            results_Robust = [sum(column) / len(column) for column in zip(*results_Robust)]
            writer.writerow([seed]+results_Robust)
        print(f'Time spent:{time.time() - t:.3f}s')
        csvFile.close()
        print('Finished!')
    elif DataSet=="google":
        review_number_google = 97658
        item_number_google = 4927
        user_number_google = 3335
        provider_num_google = 4927

        m = user_number_google
        # m = 100
        n = item_number_google
        # n = 50

        dataset_name = 'google'
        score_file = '/preference_score.csv'
        item_file = '/item_provider.csv'
        # ticket_list:订单表：ID airline classes price
        item_ProducerList = pd.read_csv('../datasets/data_' + dataset_name + item_file)
        # 用户和item的贡献矩阵：评分矩阵
        w_score = pd.read_csv('../datasets/data_' + dataset_name + score_file, header=None)
        # 评分矩阵score
        score = np.array(w_score)
        score = score[:m, :n]
        # 对分数矩阵进行归一化操作
        # score = np.array(w_score.values)
        score_true = np.copy(score)
        for index in range(len(score)):
            score[index] = (score[index] / (max(score[
                                                    index]) * 1000))  # this can accelerate the search of λ，and will not infulence any other Index ,such as the relative rank between any item，
            # and the NDCG ,which can be proof strictly!

        sorted_score = []
        for i in range(len(score)):
            sorted_score.append(np.argsort(-score[i]))
        sorted_score = np.array(sorted_score)  # 这个其实就是对score分数进行一个物品排序，然后获得每个用户的推荐列表
        user_Random = Utils.load_variavle("../datasets/data_google/random_user.pkl")
        # hyperParameter
        K = 20
        λ = 8
        ratio = 0.2
        low_bound = 0.85
        gap = 1 / 64
        qualityOrUniform = 0  # Fair appeal: 0 is Quality and 1 is Uniform
        # save result analyze
        csvFile = SaveResult_WriteTitle_Online(dataset_name, qualityOrUniform)
        writer = csv.writer(csvFile)
        t = time.time()
        user_Random = []
        for j in range(10):
            user_Random.extend([user for user in range(m)])
        for seed in radomSeeds:
            # 原始列表
            np.random.seed(seed)
            # 随机打乱列表
            np.random.shuffle(user_Random)
            results_Robust = FairSort_Online.FairSortOnLine(λ, ratio, gap, low_bound, K, score, sorted_score,
                                                            qualityOrUniform, user_Random,
                                                            item_ProducerList, "provider", None, dataset_name)
            results_Robust = [sum(column) / len(column) for column in zip(*results_Robust)]
            writer.writerow([seed] + results_Robust)
        print(f'Time spent:{time.time() - t:.3f}s')
        csvFile.close()
        print('Finished!')

if __name__ == '__main__':
    DataSets=["ctrip","amazon","google"]
    randomSeeds=[10,20,30,40,50,60,70,80,90,100]
    for dataset in DataSets:
        FairSort_Online_Robust(dataset, randomSeeds)