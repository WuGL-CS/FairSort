import csv

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# round=[x for x in range(38140)]
# Ctrip_FairSort_quality_csv= pd.read_csv('../datasets/results/result_ctrip/FairSortOnLine/FairSortQualityOn8_1_0.9.csv',encoding="gbk")
# Ctrip_TFROM_quality_csv=pd.read_csv('../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Quality.csv',encoding="gbk")
# FairSort_exposure_quality_var=np.array(Ctrip_FairSort_quality_csv["exposure_quality_var"])
# TFROM_exposure_quality_var=np.array(Ctrip_TFROM_quality_csv["exposure_quality_var"])
# Ctrip的价值方差图

# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.


# title:
#   0: satisfaction_Total
#   1:NDCG_Var
#   2:exposure_var
#   3:Variance of the ratio of exposure and relevance
def resultAnalysis_Online(dataSetName,BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label):
    Y_dict={}
    if(dataSetName=="ctrip"):
        X = [x for x in range(38140)]
    elif(dataSetName=="amazon"):
        X=[x for x in range(18510)]
    for modelName , path in BestResultFilePath.items():
            csv=pd.read_csv(path,encoding="gbk")
            # if(modelName=="FairSort_Uniform"):
            #     indexName="exposure_var"
            Y_dict[modelName]=np.array(csv[indexName])#this indexName has no extendable(bug)
    paint(X,Y_dict,title,X_len,Y_len,x_label,y_label)
#X_len=5 Y_len=2.7
def paint(X,Y_dict,title,X_len,Y_len,x_label,y_label):
    fig, ax = plt.subplots(figsize=(X_len, Y_len), layout='constrained')
    for modelName, Y in Y_dict.items():
        ax.plot(X, Y, label=modelName)  # Plot more data on the axes...
    ax.set_xlabel(x_label)  # Add an x-label to the axes.
    ax.set_ylabel(y_label)  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    ax.legend()  # Add a legend.
    ax.grid(True)
    plt.show()
#Variance of the ratio of exposure and relevance
# BestResultFilePath={}
# BestResultFilePath["FairSort_quality"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQualityOn1_0.1_0.95.csv"
# BestResultFilePath["TFROM_quality"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["FairSort_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
#
# resultAnalysis_Online("amazon",BestResultFilePath,"Variance of the ratio of exposure and relevance","exposure_quality_var",5.8,3.2,"customer_request","Variance of the ratio of exposure and relevance")

# Variance of NDCG
# csv = pd.read_csv("../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv", encoding="gbk")
BestResultFilePath={}
BestResultFilePath["TFROM_quality"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
BestResultFilePath["TFROM_uniform"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Uniform.csv"
BestResultFilePath["FairSort_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
BestResultFilePath["FairSort_quality"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQualityOn1_0.1_0.95.csv"

resultAnalysis_Online("amazon",BestResultFilePath,"Variance of NDCG","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG")

#Total recommendation quality
# csv = pd.read_csv("../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv", encoding="gbk")
# BestResultFilePath={}
# BestResultFilePath["TFROM_quality"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_uniform"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["FairSort_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
# BestResultFilePath["FairSort_quality"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQualityOn1_0.1_0.95.csv"
#
# resultAnalysis_Online("amazon",BestResultFilePath,"Total recommendation quality","satisfaction_total",5.8,3.2,"customer_request","total recommendation quality")


