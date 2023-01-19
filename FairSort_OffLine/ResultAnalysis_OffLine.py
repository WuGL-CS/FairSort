import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def resultAnalysis_Online(BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label):
    Y_dict={}
    X = [x for x in range(2,26)]
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
        ax.plot(X, Y, label=modelName ,linestyle=':',marker='*')  # Plot more data on the axes...
    ax.set_xlabel(x_label)  # Add an x-label to the axes.
    ax.set_ylabel(y_label)  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    ax.legend()  # Add a legend.
    ax.grid(True)
    plt.show()

# Ctrip:Result_Analysis:
#     Total recommendation quality
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
BestResultFilePath={}
BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQualityOff_16_1_0.9.csv"
BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
BestResultFilePath["all_random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"

resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality")
