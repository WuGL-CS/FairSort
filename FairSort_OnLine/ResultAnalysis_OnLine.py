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
def resultAnalysis_Online(dataSetName,BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label,linewidth,markersize,markevery,filePath=None):
    Y_dict={}
    if(dataSetName=="ctrip"):
        X = [x for x in range(38140)]
    elif(dataSetName=="amazon"):
        X=[x for x in range(18510)]
    elif(dataSetName=="google"):
        X=[x for x in range(33350)]
    for modelName, path in BestResultFilePath.items():
            csv=pd.read_csv(path,encoding="gbk")
            # if(modelName=="FairSort_Uniform"):
            #     indexName="exposure_var"
            Y_dict[modelName]=np.array(csv[indexName])#this indexName has no extendable(bug)
            if(indexName=="satisfaction_total"):
                 for index in range(len(Y_dict[modelName])):
                    Y_dict[modelName][index]/=(index+1)#compute the average recommendation Quality
    paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,linewidth,markersize,markevery,filePath)
#X_len=5 Y_len=2.7
def paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,linewidth,markersize,markevery,path):
    fig, ax = plt.subplots(figsize=(X_len, Y_len), layout='constrained')
    for modelName, Y in Y_dict.items():
        if (modelName == "Minimum_Exposure"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="o", markevery=markevery,markersize=markersize, color="darkviolet",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "Top-K"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="D", markevery=markevery,markersize=markersize, color="black",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "All_Random"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="*",markevery=markevery, markersize=markersize, color="chocolate",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "Mixed-k"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="p",markevery=markevery, markersize=markersize, color="maroon",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "TFROM_Uniform_Weight"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="<", markevery=markevery,markersize=markersize, color="deeppink",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "TFROM_Quality_Weight"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker=">", markevery=markevery,markersize=markersize, color="orange",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "FairSort_Quality_Weight"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="^", markevery=markevery,markersize=markersize, color="blue",
                    lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "FairSort_Uniform_Weight"):
            ax.plot(X, Y, label=modelName, linestyle='-', marker="v",markevery=markevery, markersize=markersize, color="green",
                    lw=linewidth)  # Plot more data on the axes...

    # mplcyberpunk.make_lines_glow()
    ax.set_xlabel(x_label,fontsize="40")  # Add an x-label to the axes.
    ax.set_ylabel(y_label,fontsize="30")  # Add a y-label to the axes.
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)
    ax.set_title(title)  # Add a title to the axes.
    DraggableLegend(ax.legend(fontsize="25")) # Add a legend.
    plt.legend().set_visible(False)
    ax.grid(True)
    if path != None:
        plt.savefig(path)
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 12,
             }
    # then create a new image
    # adjust the figure size as necessary
    figsize = (3, 3)
    fig_leg = plt.figure(figsize=figsize, layout="tight")
    ax_leg = fig_leg.add_subplot(111)
    # add the legend from the previous axes
    ax_leg.legend(*ax.get_legend_handles_labels(), loc='center', bbox_to_anchor=(0.5, 1),
                  fancybox=True, shadow=True, ncol=5, prop=font2)
    # hide the axes frame and the x/y labels
    ax_leg.axis('off')
    plt.show()


# Ctrip:Result_Analysis:
#
# Ctrip:Result_Analysis:
#     Variance of NDCG

# linewidth = 5
# markersize = 19
# markevery = 1500
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OnLine/ctrip/minimumExposure_OnLine.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OnLine/ctrip/Random_k_Online.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/ctrip/Mixed_k_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/ctrip/Top_K_Online.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortUniformOn8_1_0.85.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_ctrip/FairSortOnLine/FairSortQuality_NewOn8_1_0.9.csv"
#
# resultAnalysis_Online("ctrip",BestResultFilePath,"","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG",linewidth,markersize,markevery)
#
#
# # Amazon:Result_Analysis:
# #    Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_amazon/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OnLine/amazon/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/amazon/Top_K_Online.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OnLine/amazon/Random_k_Online.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/amazon/Mixed_k_OnLine.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_amazon/FairSortOnLine/FairSortQuality_NewOn1_0.1_0.95.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_amazon/FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
# #
# resultAnalysis_Online("amazon",BestResultFilePath,"","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG",linewidth,markersize,markevery)
#
# # Google:Result_Analysis:
# #   Variance of NDCG
# BestResultFilePath={}
# BestResultFilePath["Minimum_Exposure"]="../BaseLine/Results/OnLine/google/minimumExposure_OnLine.csv"
# BestResultFilePath["Top-K"]="../BaseLine/Results/OnLine/google/Top_K_Online.csv"
# # BestResultFilePath["All_Random"]="../BaseLine/Results/OnLine/google/Random_k_Online.csv"
# # BestResultFilePath["Mixed-k"]="../BaseLine/Results/OnLine/google/Mixed_k_OnLine.csv"
# BestResultFilePath["TFROM_online_Quality_Weighted"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Quality.csv"
# BestResultFilePath["TFROM_online_Uniform"]="../datasets/results/result_google/TFROM_Dynamic/dynamic_result_Uniform.csv"
# BestResultFilePath["FairSort_online_Uniform"]="../datasets/results/result_google/FairSortOnLine/FairSortUniformOn8_0.25_0.85.csv"
# BestResultFilePath["FairSort_online_Quality_Weighted"]="../datasets/results/result_google/FairSortOnLine/FairSortQuality_NewOn8_0.2_0.85.csv"
#
# resultAnalysis_Online("google",BestResultFilePath,"","satisfaction_var",5.8,3.2,"customer_request","Variance of NDCG",linewidth,markersize,markevery)

def getAllModels(dataset):
    BestResultFilePath = {}
    basePath_BaseLine = f"../BaseLine/Results/OnLine/{dataset}/"
    sotaPath = f"../datasets/results/result_{dataset}/"
    # BaseLine Model:
    BestResultFilePath["Top-K"] = basePath_BaseLine + "Top_K_Online.csv"
    BestResultFilePath["Minimum_Exposure"] = basePath_BaseLine + "minimumExposure_OnLine.csv"
    BestResultFilePath["All_Random"] = basePath_BaseLine + "Random_k_Online.csv"
    BestResultFilePath["Mixed-k"] = basePath_BaseLine + "Mixed_k_OnLine.csv"
    # SOTA Model:
    BestResultFilePath["TFROM_Quality_Weight"] = sotaPath + "TFROM_Dynamic/dynamic_result_Quality.csv"
    BestResultFilePath["TFROM_Uniform_Weight"] = sotaPath + "TFROM_Dynamic/dynamic_result_Uniform.csv"
    if dataset == "ctrip":
        BestResultFilePath[
            "FairSort_Uniform_Weight"] = sotaPath + "FairSortOnLine/FairSortUniformOn8_1_0.85.csv"
        BestResultFilePath[
            "FairSort_Quality_Weight"] = sotaPath + "FairSortOnLine/FairSortQuality_NewOn8_1_0.9.csv"
    elif dataset == "amazon":
        BestResultFilePath[
            "FairSort_Quality_Weight"] = sotaPath + "FairSortOnLine/FairSortQuality_NewOn1_0.1_0.95.csv"
        BestResultFilePath[
            "FairSort_Uniform_Weight"] = sotaPath + "FairSortOnLine/FairSortUniformOn1_0.1_0.95.csv"
    elif dataset == "google":
        BestResultFilePath[
            "FairSort_Uniform_Weight"] = sotaPath + "FairSortOnLine/FairSortUniformOn8_0.25_0.85.csv"
        BestResultFilePath[
            "FairSort_Quality_Weight"] = sotaPath + "FairSortOnLine/FairSortQuality_NewOn8_0.2_0.85.csv"
    return BestResultFilePath
def getModels(metric,dataset):
    BestResultFilePath = getAllModels(dataset)#Get the 10 models, according to the data set
    if metric =="Average recommendation quality":
        return BestResultFilePath
    elif metric=="Variance of NDCG":
        #they loss quite much recommendation Quality,so we do not compare them
        BestResultFilePath.pop("All_Random")
        BestResultFilePath.pop("Mixed-k")
        return BestResultFilePath
    elif metric=="Variance of exposure":
        BestResultFilePath.pop("FairSort_Quality_Weight")
        BestResultFilePath.pop("TFROM_Quality_Weight")
        return BestResultFilePath
    elif metric=="Exposure_quality_var":
        BestResultFilePath.pop("TFROM_Uniform_Weight")
        BestResultFilePath.pop("FairSort_Uniform_Weight")
        return BestResultFilePath


def getResult(Metric,Dataset,lineWidth,markerSize,markevery,filePathBase):
    for metric in Metric:
        for dataset in Dataset:
            datasetTitle=dataset.title()
            Models=getModels(metric,dataset)
            path = filePathBase + f"/{datasetTitle}_Online_" + metric+".pdf"
            if metric =="Average recommendation quality":
                resultAnalysis_Online(dataset,Models,"","satisfaction_total",19.2,10.8,"customer_request",metric,lineWidth,markerSize,markevery,path)
            elif metric=="Variance of NDCG":
                resultAnalysis_Online(dataset,Models,"","satisfaction_var",19.2,10.8,"customer_request",metric,lineWidth,markerSize,markevery,path)
            elif metric=="Variance of exposure":
                resultAnalysis_Online(dataset,Models,"","exposure_var",19.2,10.8,"customer_request",metric,lineWidth,markerSize,markevery,path)
            elif metric == "Exposure_quality_var":
                resultAnalysis_Online(dataset,Models,"","exposure_quality_var",19.2,10.8,"customer_request","Variance of the ratio of exposure and relevance",lineWidth,markerSize,markevery,path)
if __name__ == '__main__':
    lineWidth = 5
    markerSize = 25
    markevery = 1500
    metrix = ["Average recommendation quality", "Variance of NDCG", "Variance of exposure", "Exposure_quality_var"]
    datasets = ["ctrip", "amazon", "google"]
    filePathBase = "..\\FairSortFigure\\OnLine_Pig"
    getResult(metrix, datasets, lineWidth, markerSize,markevery,filePathBase)