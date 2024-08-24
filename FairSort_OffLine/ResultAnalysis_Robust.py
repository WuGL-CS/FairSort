import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from FairSort_Utils import resultAnalysis_Offline


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
            path = filePathBase + f"/{datasetTitle}_Offline_" + metric+".pdf"
            if metric =="Total recommendation quality":
                resultAnalysis_Offline(X,Models,"","satisfaction_total",19.2,10.8,Robust,
                                  metric,"*",lineWidth,markerSize,path)
            elif metric=="Variance of NDCG":
                resultAnalysis_Offline(X,Models, "", "satisfaction_var", 19.2, 10.8, Robust, metric,
                                      "^", lineWidth, markerSize,path)
            elif metric=="Variance of exposure":
                Models.pop("FairSort_Quality_Weight")
                resultAnalysis_Offline(X,Models, "", "exposure_var", 19.2, 10.8, Robust,metric,
                                      "o", lineWidth, markerSize,path)
            elif metric == "Exposure_quality_var":
                Models.pop("FairSort_Uniform_Weight")
                resultAnalysis_Offline(X,Models, "", "exposure_quality_var", 19.2, 10.8, Robust,
                                      "Variance of the ratio of exposure and relevance", "D", lineWidth, markerSize,path)


if __name__ == '__main__':
    lineWidth=5
    markerSize=19
    metrix=["Total recommendation quality","Variance of NDCG","Variance of exposure", "Exposure_quality_var"]
    datasets=["ctrip","amazon","google"]
    filePathBase="..\\FairSortFigure\\OffLine_Pig_Robust"
    X=[1,0.95,0.9,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5]
    getResult(metrix,datasets,lineWidth,markerSize,filePathBase,X,"threadhold")