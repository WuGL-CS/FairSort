import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def resultAnalysis_Online(BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label,marker):
    Y_dict={}
    X = [x for x in range(2,26)]
    for modelName , path in BestResultFilePath.items():
            csv=pd.read_csv(path,encoding="gbk")
            # if(modelName=="FairSort_Uniform"):
            #     indexName="exposure_var"
            Y_dict[modelName]=np.array(csv[indexName])#this indexName has no extendable(bug)
    paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,marker)
#X_len=5 Y_len=2.7
def paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,marker):
    fig, ax = plt.subplots(figsize=(X_len, Y_len), layout='constrained')
    for modelName, Y in Y_dict.items():
        ax.plot(X, Y, label=modelName ,linestyle=':',marker=marker)  # Plot more data on the axes...
    ax.set_xlabel(x_label)  # Add an x-label to the axes.
    ax.set_ylabel(y_label)  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    ax.legend()  # Add a legend.
    ax.grid(True)
    plt.show()

# # Ctrip:Result_Analysis:
# #     Total recommendation quality
# # pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQualityOff_16_1_0.9.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality","*")

# Ctrip:Result_Analysis:
#     # Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQualityOff_16_1_0.9.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_var",5.8,3.2,"K","Variance of NDCG","x")


#  Ctrip:Result_Analysis:
    # Variance of exposure
# BestResultFilePath={}
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_var",5.8,3.2,"K","Variance of exposure","+")


#  Ctrip:Result_Analysis:
    #Variance of the ratio of exposure and relevance
# BestResultFilePath={}
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQualityOff_16_1_0.9.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_quality_var",5.8,3.2,"K","Variance of the ratio of exposure and relevance","1")


# Amazon:Result_Analysis:
#     Total recommendation quality
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_amazon/FairSortUniformOff8_0.1_0.95.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_amazon/FairSortQualityOff32_0.1_0.91(116+score.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_amazon/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_amazon/TFROM/result_Uniform.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality","*")


# # Amazon:Result_Analysis:
# #    Variance of NDCG
# # pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_amazon/FairSortUniformOff8_0.1_0.95.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_amazon/FairSortQualityOff32_0.1_0.91(116+score.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_amazon/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_amazon/TFROM/result_Uniform.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_var",5.8,3.2,"K","Variance of NDCG","x")

# Amazon:Result_Analysis:
#    Variance of exposure
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_amazon/FairSortUniformOff8_0.1_0.95.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_amazon/TFROM/result_Uniform.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_var",5.8,3.2,"K","Variance of exposure","+")

# Amazon:Result_Analysis:
#     Variance of the ratio of exposure and relevance
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_amazon/FairSortQualityOff32_0.1_0.91(116+score.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_amazon/TFROM/result_quality.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_quality_var",5.8,3.2,"K","Variance of the ratio of exposure and relevance","1")



# # Google:Result_Analysis:
# #     Total recommendation quality
# # pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/google/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_google/FairSortUniformOff8_0.15_0.85.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_google/FairSortQualityOff8_0.15_0.85.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_google/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_google/TFROM/result_Uniform.csv"
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality","*")


# Google:Result_Analysis:
#     Vairance of NDCG
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/google/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_google/FairSortUniformOff8_0.15_0.85.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_google/FairSortQualityOff8_0.15_0.85.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_google/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_google/TFROM/result_Uniform.csv"
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_var",5.8,3.2,"K","Variance of NDCG","x")


# Google:Result_Analysis:
#     Vairance of exposure
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/google/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_google/TFROM/result_Uniform.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_google/FairSortUniformOff8_0.15_0.85.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_var",5.8,3.2,"K","Variance of exposure ","+")


# # Google:Result_Analysis:
#     Variance of the ratio of exposure and relevance
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_google/FairSortQualityOff8_0.15_0.85.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_google/TFROM/result_quality.csv"
# resultAnalysis_Online(BestResultFilePath,"","exposure_quality_var",5.8,3.2,"K","Variance of the ratio of exposure and relevance","1")