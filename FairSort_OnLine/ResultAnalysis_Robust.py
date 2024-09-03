import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from FairSort_OffLine.FairSort_Utils import resultAnalysis_Offline


def getModels(dataset,Robust):
    BestResultFilePath = {}
    basePath_BaseLine = f"../results_Robust/{Robust}_Robust/{dataset}"

    # BaseLine Model:
    BestResultFilePath[
            "FairSort_Uniform_Weight"] = basePath_BaseLine + f"/FairSort_Robust({Robust})_UF.csv"
    BestResultFilePath[
            "FairSort_Quality_Weight"] = basePath_BaseLine + f"/FairSort_Robust({Robust})_QF.csv"
    return BestResultFilePath
def getResult(Metric,Dataset,lineWidth,markerSize,filePathBase,X,Robust):
    for metric in Metric:
        for dataset in Dataset:
            datasetTitle=dataset.title()
            Models=getModels(dataset,Robust)
            path = filePathBase + f"/{datasetTitle}_Online_" + metric+".png"
            if metric =="satisfaction_average":
                resultAnalysis_Offline(X,Models,"","satisfaction_average",19.2,10.8,Robust,
                                  metric,"*",lineWidth,markerSize,path)
            elif metric=="satisfaction_var_average":
                resultAnalysis_Offline(X,Models, "", "satisfaction_var_average", 19.2, 10.8, Robust, metric,
                                      "^", lineWidth, markerSize,path)
            elif metric=="exposure_var_average":
                Models.pop("FairSort_Quality_Weight")
                resultAnalysis_Offline(X,Models, "", metric, 19.2, 10.8, Robust,metric,
                                      "o", lineWidth, markerSize,path)
            elif metric == "exposure_quality_var_average":
                Models.pop("FairSort_Uniform_Weight")
                resultAnalysis_Offline(X,Models, "", metric, 19.2, 10.8, Robust,
                                      metric, "D", lineWidth, markerSize,path)


if __name__ == '__main__':
    lineWidth=5
    markerSize=19
    metrix=["satisfaction_average","satisfaction_var_average","exposure_var_average", "exposure_quality_var_average"]
    datasets=["ctrip","amazon","google"]
    filePathBase="..\\FairSortFigure\\OnLine_Pig_Robust"
    X=[10,20,30,40,50,60,70,80,90,100]
    getResult(metrix,datasets,lineWidth,markerSize,filePathBase,X,"user_Random_Seeds")