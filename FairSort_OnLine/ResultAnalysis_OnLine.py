import csv
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
class DraggableLegend:
    def __init__(self, legend):
        self.legend = legend
        self.gotLegend = False
        legend.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        legend.figure.canvas.mpl_connect('pick_event', self.on_pick)
        legend.figure.canvas.mpl_connect('button_release_event', self.on_release)
        legend.set_picker(self.my_legend_picker)
    def on_motion(self, evt):
        if self.gotLegend:
            dx = evt.x - self.mouse_x
            dy = evt.y - self.mouse_y
            loc_in_canvas = self.legend_x + dx, self.legend_y + dy
            loc_in_norm_axes = self.legend.parent.transAxes.inverted().transform_point(loc_in_canvas)
            self.legend._loc = tuple(loc_in_norm_axes)
            self.legend.figure.canvas.draw()
    def my_legend_picker(self, legend, evt):
        return self.legend.legendPatch.contains(evt)
    def on_pick(self, evt):
        if evt.artist == self.legend:
            bBox = self.legend.get_window_extent()
            self.mouse_x = evt.mouseevent.x
            self.mouse_y = evt.mouseevent.y
            self.legend_x = bBox.xmin
            self.legend_y = bBox.ymin
            self.gotLegend = 1
    def on_release(self, event):
        if self.gotLegend:
            self.gotLegend = False

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
    elif(dataSetName=="google"):
        X=[x for x in range(33350)]
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
        if (modelName == "minimum_exposure"):
            ax.plot(X, Y, label=modelName,  color="darkviolet")  # Plot more data on the axes...
        elif (modelName == "Top-K"):
            ax.plot(X, Y, label=modelName,  color="black")  # Plot more data on the axes...
        elif (modelName == "FairSort_online_Quality_Weighted"):
            ax.plot(X, Y, label=modelName,  color="blue")  # Plot more data on the axes...
        elif (modelName == "FairSort_online_Uniform"):
            ax.plot(X, Y, label=modelName,  color="green")  # Plot more data on the axes...
        elif (modelName == "all_random"):
            ax.plot(X, Y, label=modelName, color="purple")  # Plot more data on the axes...
        elif (modelName == "Mixed-k"):
            ax.plot(X, Y, label=modelName, color="maroon")  # Plot more data on the axes...
        elif (modelName == "TFROM_online_Uniform"):
            ax.plot(X, Y, label=modelName, color="deeppink")  # Plot more data on the axes...
        elif (modelName == "TFROM_online_Quality_Weighted"):
            ax.plot(X, Y, label=modelName, color="orange")  # Plot more data on the axes...

    ax.set_xlabel(x_label,fontsize="24")  # Add an x-label to the axes.
    ax.set_ylabel(y_label,fontsize="24")  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    DraggableLegend(ax.legend(fontsize="25")) # Add a legend.
    ax.grid(True)
    plt.show()



# Ctrip:Result_Analysis:
#     Total recommendation quality
#
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortUniformOn8_1_0.85.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortQualityOn8_1_0.9.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/ctrip/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/ctrip/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/ctrip/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/ctrip/Mixed_k_OnLine.csv"
#
# resultAnalysis_Online("ctrip",BestResultFilePath,"","satisfaction_total",5.8,3.2,"customer_request","Total recommendation quality")

#Ctrip:Result_Analysis:
    # Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/ctrip/minimumExposure_OnLine.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/ctrip/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/ctrip/Mixed_k_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/ctrip/Top_K_Online.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortUniformOn8_1_0.85.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortQualityOn8_1_0.9.csv"
#
# resultAnalysis_Online("ctrip",BestResultFilePath,"","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG")

# #Ctrip:Result_Analysis:
#     # Variance of exposure
# BestResultFilePath = {}
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/ctrip/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/ctrip/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/ctrip/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/ctrip/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortUniformOn8_1_0.85.csv"
# resultAnalysis_Online("ctrip",BestResultFilePath,"","exposure_var",5.8,3.2,"customer_request","variance of provider exposure")

#Ctrip:Result_Analysis:
    # Variance of the ratio of exposure and relevance
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/ctrip/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/ctrip/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/ctrip/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortQualityOn8_1_0.9.csv"
#
# resultAnalysis_Online("ctrip",BestResultFilePath,"","exposure_quality_var",5.8,3.2,"customer_request","Variance of the ratio of exposure and relevance")


#Amazon:Result_Analysis:
#   Total recommendation quality
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQualityOn1_0.1_0.95.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/amazon/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/amazon/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/amazon/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/amazon/Mixed_k_OnLine.csv"
# resultAnalysis_Online("amazon",BestResultFilePath,"","satisfaction_total",5.8,3.2,"customer_request","Total recommendation quality")

#Amazon:Result_Analysis:
#    Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/amazon/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/amazon/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/amazon/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/amazon/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQualityOn1_0.1_0.95.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
# #
# resultAnalysis_Online("amazon",BestResultFilePath,"","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG")

#Amazon:Result_Analysis:
#    Variance of exposure
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/amazon/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/amazon/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/amazon/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/amazon/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
# resultAnalysis_Online("amazon",BestResultFilePath,"","exposure_var",5.8,3.2,"customer_request","Variance of exposure")

#Amazon:Result_Analysis:
#    Variance of the ratio of exposure and relevance
#
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/amazon/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/amazon/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/amazon/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQualityOn1_0.1_0.95.csv"
# resultAnalysis_Online("amazon",BestResultFilePath,"","exposure_quality_var",5.8,3.2,"customer_request","Variance of the ratio of exposure and relevance")

#Google:Result_Analysis:
#   Total recommendation quality
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_google/FairSortOnLine/FairSortUniformOn8_0.25_0.85.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_google/FairSortOnLine/FairSortQualityOn8_0.2_0.85.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/google/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/google/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/google/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/google/Mixed_k_OnLine.csv"
# resultAnalysis_Online("google",BestResultFilePath,"","satisfaction_total",5.8,3.2,"customer_request","Total recommendation quality")

#Google:Result_Analysis:
  # Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/google/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/google/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/google/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/google/Mixed_k_OnLine.csv"
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_google/FairSortOnLine/FairSortUniformOn8_0.25_0.85.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_google/FairSortOnLine/FairSortQualityOn8_0.2_0.85.csv"
#
# resultAnalysis_Online("google",BestResultFilePath,"","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG")

# Google:Result_Analysis:
#   Variance of exposure
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["minimum_exposure"]="../BaseLine/Results/OnLine/google/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/google/Top_K_Online.csv"
# BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/google/Random_k_Online.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/google/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_google/FairSortOnLine/FairSortUniformOn8_0.25_0.85.csv"
# resultAnalysis_Online("google",BestResultFilePath,"","exposure_var",5.8,3.2,"customer_request","Variance of exposure")

#Google:Result_Analysis:
  # Variance of the ratio of exposure and relevance
BestResultFilePath={}
BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Quality.csv"
BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/google/Top_K_Online.csv"
BestResultFilePath["all_random"]="../BaseLine/Results/OnLine/google/Random_k_Online.csv"
BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/google/Mixed_k_OnLine.csv"
BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_google/FairSortOnLine/FairSortQualityOn8_0.2_0.85.csv"
resultAnalysis_Online("google",BestResultFilePath,"","exposure_quality_var",5.8,3.2,"customer_request","Variance of the ratio of exposure and relevance")