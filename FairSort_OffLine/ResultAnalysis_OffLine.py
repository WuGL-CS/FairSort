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
def resultAnalysis_Online(BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label,marker,lw,markersize):
    Y_dict={}
    X = [x for x in range(2,26)]
    for modelName , path in BestResultFilePath.items():
            csv=pd.read_csv(path,encoding="gbk")
            # if(modelName=="FairSort_Uniform"):
            #     indexName="exposure_var"
            Y_dict[modelName]=np.array(csv[indexName])#this indexName has no extendable(bug)
    if(indexName=="exposure_quality_var"):
        for key, value in Y_dict.items():
            Y_dict[key]=value*100

    paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,marker,lw,markersize)
#X_len=5 Y_len=2.7
def paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,marker,linewidth,markersize):
    fig, ax = plt.subplots(figsize=(X_len, Y_len), layout='constrained')
    for modelName, Y in Y_dict.items():
        if (modelName=="Minimum_Exposure"):
            ax.plot(X, Y, label=modelName ,linestyle=':',marker="o", markersize=markersize,color="darkviolet",lw=linewidth)# Plot more data on the axes...
        elif(modelName=="Top-K"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="D", markersize=markersize, color="black",lw=linewidth)  # Plot more data on the axes...
        elif(modelName=="FairSort_offline_Quality_Weighted"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="^", markersize=markersize, color="blue",lw=linewidth)# Plot more data on the axes...
        elif (modelName == "FairSort_offline_Uniform"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="v", markersize=markersize, color="green",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "All_Random"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="*", markersize=markersize,color="chocolate",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "Mixed-k"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="p",  markersize=markersize,color="maroon",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "Fair_Rec"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="s", markersize=markersize,color="olive",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "TFROM_offline_Uniform"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="<", markersize=markersize,color="deeppink",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "TFROM_offline_Quality_Weighted"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker=">", markersize=markersize, color="orange",lw=linewidth)  # Plot more data on the axes...
        elif (modelName=="CP_Fair"):
            ax.plot(X,Y,label=modelName, linestyle=':', marker=marker,markersize=markersize, color="red",lw=linewidth)   # Plot more data on the axes...
    ax.set_xlabel(x_label, fontsize="24")  # Add an x-label to the axes.
    ax.set_ylabel(y_label, fontsize="24")  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    DraggableLegend(ax.legend(fontsize="22")) # Add a legend.
    plt.legend().set_visible(False)
    ax.grid(True)

    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 12,
             }
    # then create a new image
    # adjust the figure size as necessary
    figsize = (3, 3)
    fig_leg = plt.figure(figsize=figsize,layout="tight")
    ax_leg = fig_leg.add_subplot(111)
    # add the legend from the previous axes
    ax_leg.legend(*ax.get_legend_handles_labels(),loc='center', bbox_to_anchor=(0.5, 1),
              fancybox=True, shadow=True, ncol=5, prop=font2)
    # hide the axes frame and the x/y labels
    ax_leg.axis('off')
    plt.show()
    plt.show()


linewidth=4
markersize=18
# Ctrip:Result_Analysis:
#     Total recommendation quality
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/ctrip/CP_Fair_Offline.csv"
# # BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQuality_NewOff16_1_0.9.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
# #
# # # #
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality","*",linewidth,markersize)

# Ctrip:Result_Analysis:
    # Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQualityOff_16_1_0.9.csv"
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/ctrip/CP_Fair_Offline.csv"
#
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_var",5.8,3.2,"K","Variance of NDCG","^",linewidth,markersize)


#  Ctrip:Result_Analysis:
    # Variance of exposure
# BestResultFilePath={}
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFROM_Uniform_Offline.csv"
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv"
# BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/ctrip/CP_Fair_Offline.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_var",5.8,3.2,"K","Variance of exposure","o",linewidth,markersize)


#  Ctrip:Result_Analysis:
    #Variance of the ratio of exposure and relevance
# BestResultFilePath={}
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/ctrip/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/ctrip/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/ctrip/Mixed_k_OffLine.csv"
# # BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/ctrip/minimumExposure_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/ctrip/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortQualityOff_16_1_0.9.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM/result_analyze_TFORM_Quality_Offline.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/ctrip/CP_Fair_Offline.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_quality_var",5.8,3.2,"K","Variance of the ratio of exposure and relevance","D",linewidth,markersize)


# Amazon:Result_Analysis:
#     Total recommendation quality
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_amazon/FairSortUniformOff8_0.1_0.95.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_amazon/FairSortQualityOff32_0.1_0.91(116+score.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_amazon/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_amazon/TFROM/result_Uniform.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/amazon/CP_Fair_Offline.csv"
#
# #
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality","*",linewidth,markersize)


# # Amazon:Result_Analysis:
# #    Variance of NDCG
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
#
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_amazon/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_amazon/TFROM/result_Uniform.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/amazon/CP_Fair_Offline.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_amazon/FairSortUniformOff8_0.1_0.95.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_amazon/FairSortQualityOff32_0.1_0.91(116+score.csv"
#
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_var",5.8,3.2,"K","Variance of NDCG","^",linewidth,markersize)

# Amazon:Result_Analysis:
#    Variance of exposure
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/amazon/CP_Fair_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_amazon/TFROM/result_Uniform.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_amazon/FairSortUniformOff8_0.1_0.95.csv"
#
# #
# #
# resultAnalysis_Online(BestResultFilePath,"","exposure_var",5.8,3.2,"K","Variance of exposure","o",linewidth,markersize)

# Amazon:Result_Analysis:
#     Variance of the ratio of exposure and relevance
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/amazon/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/amazon/Random_k_Offline.csv"
# # BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/amazon/minimumExposure_OffLine.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/amazon/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/amazon/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_amazon/TFROM/result_quality.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/amazon/CP_Fair_Offline.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_amazon/FairSortQualityOff32_0.1_0.91(116+score.csv"
#
# #
# #
# resultAnalysis_Online(BestResultFilePath,"","exposure_quality_var",5.8,3.2,"K","Variance of the ratio of exposure and relevance","D",linewidth,markersize)
# # #


# # Google:Result_Analysis:
# #     Total recommendation quality
# # pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/google/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_google/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_google/TFROM/result_Uniform.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_google/FairSortUniformOff8_0.15_0.85.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_google/FairSortQualityOff8_0.15_0.85.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/google/CP_Fair_Offline.csv"
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_total",5.8,3.2,"K","total recommendation quality","*",linewidth,markersize)


# Google:Result_Analysis:
#     Vairance of NDCG
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/google/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
# BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_google/TFROM/result_quality.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_google/TFROM/result_Uniform.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/google/CP_Fair_Offline.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_google/FairSortUniformOff8_0.15_0.85.csv"
# BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_google/FairSortQualityOff8_0.15_0.85.csv"
#
# resultAnalysis_Online(BestResultFilePath,"","satisfaction_var",5.8,3.2,"K","Variance of NDCG","^",linewidth,markersize)


# Google:Result_Analysis:
#     Vairance of exposure
# pd.read_csv("../datasets/results/result_ctrip/FairSortUniformOff_16_1_0.85.csv")
# BestResultFilePath={}
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OffLine/google/minimumExposure_OffLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# BestResultFilePath["TFROM_offline_Uniform"]="../datasets/results/result_google/TFROM/result_Uniform.csv"
# BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
# BestResultFilePath["FairSort_offline_Uniform"]="../datasets/results/result_google/FairSortUniformOff8_0.15_0.85.csv"
# BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/google/CP_Fair_Offline.csv"
#
#
# resultAnalysis_Online(BestResultFilePath,"","exposure_var",5.8,3.2,"K","Variance of exposure ","o",linewidth,markersize)


# # Google:Result_Analysis:
#     Variance of the ratio of exposure and relevance
# pd.read_csv("../datasets/results/result_google/FairSortQuality_NewOff8_0.15_0.85.csv")
BestResultFilePath={}
BestResultFilePath["Top-K"]="../BaseLine/Results/OffLine/google/Top_K_Offline.csv"
# BestResultFilePath["All_Random"]="../BaseLine/Results/OffLine/google/Random_k_Offline.csv"
# BestResultFilePath["Mixed-k"]="../BaseLine/Results/OffLine/google/Mixed_k_OffLine.csv"
# BestResultFilePath["Fair_Rec"]="../BaseLine/Results/OffLine/google/FairRecOffLine.csv"
BestResultFilePath["TFROM_offline_Quality_Weighted"]="../datasets/results/result_google/TFROM/result_quality.csv"
BestResultFilePath["FairSort_offline_Quality_Weighted"]="../datasets/results/result_google/FairSortQuality_NewOff8_0.15_0.85.csv"
BestResultFilePath["CP_Fair"]="../BaseLine/Results/OffLine/google/CP_Fair_Offline.csv"

resultAnalysis_Online(BestResultFilePath,"","exposure_quality_var",5.8,3.2,"K","Variance of the ratio of exposure and relevance","D",linewidth,markersize)