import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import ast
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






def resultAnalysis_Offline(BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label,marker,lw,markersize,filePath):
    Y_dict={}
    X = [x for x in range(2,26)]
    for modelName , path in BestResultFilePath.items():
            Y_list = []
            # 打开CSV文件并读取
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                # 假设要处理的列索引是 'NDCG_distribution'
                for row in reader:
                    # 读取到的是字符串，需要转换为数组
                    ndcg_str = row[indexName]  # 这是一个字符串，比如 "[0.75, 0.85, 0.92]"

                    # 使用 ast.literal_eval 将字符串转换为数组
                    try:
                        Y_list.append(ast.literal_eval(ndcg_str))

                    except (ValueError, SyntaxError):
                        print(f"无法将字符串 '{ndcg_str}' 转换为数组")


            Y_dict[modelName] =Y_list

    paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,marker,lw,markersize,filePath)
#X_len=5 Y_len=2.7
def paint(X,Y_dict,title,X_len,Y_len,x_label,y_label,marker,linewidth,markersize,filePath):
    fig, ax = plt.subplots(figsize=(X_len, Y_len), layout='constrained')
    for modelName, Y in Y_dict.items():
        if (modelName=="Minimum_Exposure"):
            ax.plot(X, Y, label=modelName ,linestyle=':',marker="o", markersize=markersize,color="darkviolet",lw=linewidth)# Plot more data on the axes...
        elif(modelName=="Top-K"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="D", markersize=markersize, color="black",lw=linewidth)  # Plot more data on the axes...
        elif(modelName=="FairSort_Quality_Weight"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="^", markersize=markersize, color="blue",lw=linewidth)# Plot more data on the axes...
        elif (modelName == "FairSort_Uniform_Weight"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="v", markersize=markersize, color="green",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "All_Random"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="*", markersize=markersize,color="chocolate",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "Mixed-k"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="p",  markersize=markersize,color="maroon",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "Fair_Rec"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="s", markersize=markersize,color="olive",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "TFROM_Uniform_Weight"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker="<", markersize=markersize,color="deeppink",lw=linewidth)  # Plot more data on the axes...
        elif (modelName == "TFROM_Quality_Weight"):
            ax.plot(X, Y, label=modelName, linestyle=':', marker=">", markersize=markersize, color="orange",lw=linewidth)  # Plot more data on the axes...
        elif (modelName=="CP_Fair"):
            ax.plot(X,Y,label=modelName, linestyle=':', marker="X",markersize=markersize, color="red",lw=linewidth)   # Plot more data on the axes...
    ax.set_xlabel(x_label, fontsize="40")  # Add an x-label to the axes.
    ax.set_ylabel(y_label, fontsize="30")  # Add a y-label to the axes.
    ax.set_title(title)  # Add a title to the axes.
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)
    DraggableLegend(ax.legend(fontsize="22")) # Add a legend.
    plt.legend().set_visible(False)
    ax.grid(True)
    plt.savefig(filePath)
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

def getAllModels(dataset):
    BestResultFilePath = {}
    basePath_BaseLine = f"../BaseLine/Results/OffLine/{dataset}/"
    sotaPath = f"../datasets/results/result_{dataset}/"
    # BaseLine Model:
    BestResultFilePath["Top-K"] = basePath_BaseLine + "Top_K_Offline.csv"
    BestResultFilePath["Minimum_Exposure"] = basePath_BaseLine + "minimumExposure_OffLine.csv"
    BestResultFilePath["CP_Fair"] = basePath_BaseLine + "CP_Fair_Offline.csv"
    BestResultFilePath["Fair_Rec"] = basePath_BaseLine + "FairRecOffLine.csv"
    BestResultFilePath["All_Random"] = basePath_BaseLine + "Random_k_Offline.csv"
    BestResultFilePath["Mixed-k"] = basePath_BaseLine + "Mixed_k_OffLine.csv"
    # SOTA Model:
    BestResultFilePath["TFROM_Quality_Weight"] = sotaPath + "TFROM/result_quality.csv"
    BestResultFilePath["TFROM_Uniform_Weight"] = sotaPath + "TFROM/result_Uniform.csv"
    if dataset == "ctrip":
        BestResultFilePath[
            "FairSort_Uniform_Weight"] = sotaPath + "FairSortUniformOff16_1_0.85.csv"
        BestResultFilePath[
            "FairSort_Quality_Weight"] = sotaPath + "FairSortQuality_NewOff16_1_0.9.csv"
    elif dataset == "amazon":
        BestResultFilePath[
            "FairSort_Quality_Weight"] = sotaPath + "/FairSortQuality_NewOff32_0.1_0.9.csv"
        BestResultFilePath[
            "FairSort_Uniform_Weight"] = sotaPath + "/FairSortUniformOff8_0.1_0.95.csv"
    elif dataset == "google":
        BestResultFilePath[
            "FairSort_Uniform_Weight"] = sotaPath + "/FairSortUniformOff8_0.15_0.85.csv"
        BestResultFilePath[
            "FairSort_Quality_Weight"] = sotaPath + "/FairSortQuality_NewOff8_0.15_0.85.csv"
    return BestResultFilePath
def getModels(metric,dataset):
    BestResultFilePath = getAllModels(dataset)#Get the 10 models, according to the data set
    BestResultFilePath.pop("All_Random")
    BestResultFilePath.pop("Mixed-k")
    BestResultFilePath.pop("Minimum_Exposure")

    if metric =="Mean Average Envy":
        return BestResultFilePath
    elif metric=="Inequality in Producer Exposure(QF)":
        BestResultFilePath.pop("FairSort_Uniform_Weight")
        BestResultFilePath.pop("TFROM_Uniform_Weight")
        return BestResultFilePath
    elif metric=="Inequality in Producer Exposure(UF)":
        BestResultFilePath.pop("FairSort_Quality_Weight")
        BestResultFilePath.pop("TFROM_Quality_Weight")
        return BestResultFilePath



def getResult(Metric,Dataset,lineWidth,markerSize,filePathBase):
    for metric in Metric:
        for dataset in Dataset:
            datasetTitle=dataset.title()
            Models=getModels(metric,dataset)
            path = filePathBase + f"/{datasetTitle}_Offline_" + metric+".pdf"
            if metric =="Mean Average Envy":
                resultAnalysis_Offline(Models,"","Mean Average Envy",19.2,10.8,"K",
                                  metric,"*",lineWidth,markerSize,path)
            elif metric=="Inequality in Producer Exposure(QF)":
                resultAnalysis_Offline(Models, "", "Inequality in Producer Exposure(QF)", 19.2, 10.8, "K", metric,
                                      "^", lineWidth, markerSize,path)
            elif metric=="Inequality in Producer Exposure(UF)":
                resultAnalysis_Offline(Models, "", "Inequality in Producer Exposure(UF)", 19.2, 10.8, "K", metric,
                                      "o", lineWidth, markerSize,path)

if __name__ == '__main__':
    lineWidth=5
    markerSize=19
    metrix=["Mean Average Envy","Inequality in Producer Exposure(QF)","Inequality in Producer Exposure(UF)"]
    datasets=["ctrip","amazon","google"]
    filePathBase="..\\FairSortFigure\\OffLine_Pig"
    getResult(metrix,datasets,lineWidth,markerSize,filePathBase)