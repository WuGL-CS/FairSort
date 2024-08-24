import csv
import pickle
import  numpy as  np
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
def resultAnalysis_Offline(X,BestResultFilePath,title,indexName,X_len,Y_len,x_label,y_label,marker,lw,markersize,filePath):
    Y_dict={}

    for modelName , path in BestResultFilePath.items():
            csv=pd.read_csv(path,encoding="gbk")
            # if(modelName=="FairSort_Uniform"):
            #     indexName="exposure_var"
            Y_dict[modelName]=np.array(csv[indexName])#this indexName has no extendable(bug)


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
    if(y_label=="Variance of the ratio of exposure and relevance"):
        ax.set_ylabel(y_label, fontsize="22")  # Add a y-label to the axes.
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
def save_value(value,filePath):
    pic=open(filePath,'wb')
    pickle.dump(value,pic)
    pic.close()


def load_variavle(filename):
    try:
        f = open(filename, 'rb+')
        r = pickle.load(f)
        f.close()
        return r
    except EOFError:
        return ""
def SaveResult_WriteTitle_Offline(dataset_name,qualityOrUniform,λ,ratio,low_bound):
    fairType=""
    if qualityOrUniform==0:fairType="Quality_New"
    elif(qualityOrUniform==1):fairType="Uniform"
    fileName="/FairSort"+fairType+"Off"+str(λ)+"_"+str(ratio)+"_"+str(low_bound)+".csv"
    csvFile = open("../datasets/results/result_" + dataset_name+ fileName
                   , 'w', newline='')
    writer = csv.writer(csvFile)
    title = []
    title.append('k')
    title.append('satisfaction_var')
    title.append('satisfaction_diverse')
    title.append('satisfaction_total')
    if(qualityOrUniform==0):
        title.append('Top-k_qualityVar')
        title.append('exposure_quality_var')
        title.append('exposure_quality_diverse')
    elif(qualityOrUniform==1):
        title.append('Top-k_SizeVar')
        title.append('exposure_var')
        title.append('exposure_diverse')
    title.append('fair_VarAtFirst')
    title.append('fair_Var')  # 公平要求下的方差值：越小越好，说明地整的越平
    title.append("Top-K转化率分布")
    title.append("FairSort转化率分布")
    title.append("公平曝光资源分布")
    title.append("Top-K曝光err")
    title.append("FairSort曝光err")
    title.append("提供商物品数分布")
    title.append("提供商价值量分布")
    writer.writerow(title)
    return csvFile

def SaveResult_WriteTitle_Online(dataset_name,qualityOrUniform,λ,ratio,low_bound):
    fairType=""
    if qualityOrUniform==0:fairType="Quality_New"
    elif(qualityOrUniform==1):fairType="Uniform"
    fileName="/FairSort"+fairType+"On"+str(λ)+"_"+str(ratio)+"_"+str(low_bound)+".csv"
    csvFile = open("../datasets/results/result_" + dataset_name+ "/FairSortOnLine"+fileName
                   , 'w', newline='')
    writer = csv.writer(csvFile)
    title = []
    title.append('round')
    title.append('satisfaction_var')
    title.append('satisfaction_diverse')
    title.append('satisfaction_total')
    if(qualityOrUniform==0):
        # title.append('Top-k_qualityVar')
        title.append('exposure_quality_var')
        title.append('exposure_quality_diverse')
    elif(qualityOrUniform==1):
        # title.append('Top-k_SizeVar')
        title.append('exposure_var')
        title.append('exposure_diverse')
    title.append("NDCG:{[0--0.5],[0.5--0.6],[0.6--0.7],[0.7--0.75],[0.75-0.8],[0.8--0.85],[0.85--0.9],[0.9--0.95],[0.95--1]}")
    if(dataset_name!="google"):
        title.append("转化率分布")
    writer.writerow(title)
    return csvFile

#函数的参数说明：
    #producerExposure:提供商的曝光资源分布向量[l] #fairRegulation:基于价值或者数目计算转化率 (o或者1):0是价值，1是物品数
    #providerSize:提供商拥有的物品数目[l] #provider_quality:提供商侧的价值量分布向量[l]
#计算逻辑:计算当前资源分布情况（分发给提供商的情况）基于某个价值维度考量下的转化率
def getProducerExposurCoversionRate(producerExposure,fairRegulation,providerSize,provider_quality):
    convertRate = []
    if (fairRegulation == 0):  # 这个是基于价值效益
        for index in range(len(producerExposure)):
            convertRate.append(producerExposure[index]/provider_quality[index] *1000)
        return convertRate
    elif (fairRegulation == 1):  # 这个是基于数量效益的
        for index in range(len(producerExposure)):
            convertRate.append(producerExposure[index] / providerSize[index])
        return convertRate
#函数的参数说明：
    #producerExposure:提供商的曝光资源分布向量[l] #fairRegulation:基于价值或者数目计算转化率 (o或者1)
    #providerSize:提供商拥有的物品数目[l] #provider_quality:提供商侧的价值量分布向量[l]
#计算逻辑:计算当前资源分布情况（分发给提供商的情况），其转化率的方差值大小：越小越好
def getVar(convertRate):
    return np.var(convertRate)
def getDiverse(convertRate):
    avg=sum(convertRate)/len(convertRate)
    diverse=0
    for index in range(len(convertRate)):
        diverse+=abs(convertRate[index]-avg)/len(convertRate)
    return diverse


def getFairAndCurrentErr(producerExposure,fair_exposure):
    err=[]
    for index in range(len(fair_exposure)):
        err.append(fair_exposure[index]-producerExposure[index])
    return  err


def getSatisfactionDistribution(user_satisfaction):
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    count8 = 0
    count9 = 0
    for satisfaction in user_satisfaction:

        if (satisfaction < 0.5):
            count1 += 1
        elif (satisfaction <= 0.6):
            count2 += 1
        elif (satisfaction <= 0.7):
            count3 += 1
        elif (satisfaction <= 0.75):
            count4 += 1
        elif (satisfaction <= 0.8):
            count5 += 1
        elif (satisfaction <= 0.85):
            count6 += 1
        elif (satisfaction <= 0.9):
            count7 += 1
        elif (satisfaction <= 0.95):
            count8 += 1
        elif (satisfaction <= 1):
            count9 += 1
    print("0.5以下", count1)
    print("0.5—0.6", count2)
    print("0.6—0.7", count3)
    print("0.7—0.75", count4)
    print("0.75—0.8", count5)
    print("0.8—0.85", count6)
    print("0.85—0.9", count7)
    print("0.9—0.95", count8)
    print("0.95—1", count9)
    print("总共:", count9+count8+count7+count6 + count5 + count4 + count3 + count2 + count1)

def getSatisfactionDistribution2(user_satisfaction,user_satisDistributList):
        if (user_satisfaction <= 0.5):
            user_satisDistributList[0] += 1
        elif (user_satisfaction <= 0.6):
            user_satisDistributList[1] += 1
        elif (user_satisfaction <= 0.7):
            user_satisDistributList[2] += 1
        elif (user_satisfaction <= 0.75):
            user_satisDistributList[3] += 1
        elif (user_satisfaction <= 0.8):
            user_satisDistributList[4] += 1
        elif (user_satisfaction <= 0.85):
            user_satisDistributList[5] += 1
        elif (user_satisfaction <= 0.9):
            user_satisDistributList[6] += 1
        elif (user_satisfaction <= 0.95):
            user_satisDistributList[7] += 1
        elif (user_satisfaction <= 1.0000005):
            user_satisDistributList[8] += 1

def getStandardDeviation(List):
    avg=sum(List)/len(List)
    StandardDeviation=0
    for index in range(len(List)):
        StandardDeviation+=abs(List[index]-avg)/len(List)
    return StandardDeviation
if __name__ == '__main__':
    satisDistribute=[0 for x in range(9)]
    print(satisDistribute)
    getSatisfactionDistribution2(1,satisDistribute)
    getSatisfactionDistribution2(0,satisDistribute)
    getSatisfactionDistribution2(0.7,satisDistribute)
    getSatisfactionDistribution2(0.92,satisDistribute)
    getSatisfactionDistribution2(0.77,satisDistribute)
    print(satisDistribute)