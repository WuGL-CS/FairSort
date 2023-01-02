import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

round=[x for x in range(38140)]
Ctrip_FairSort_quality_csv= pd.read_csv('../datasets/results/result_ctrip/FairSortOnLine/FairSortQualityOn8_1_0.9.csv',encoding="gbk")
Ctrip_TFROM_quality_csv=pd.read_csv('../datasets/results/result_ctrip/TFROM_Dynamic/dynamic_result_Quality.csv',encoding="gbk")
FairSort_exposure_quality_var=np.array(Ctrip_FairSort_quality_csv["exposure_quality_var"])
TFROM_exposure_quality_var=np.array(Ctrip_TFROM_quality_csv["exposure_quality_var"])
# Ctrip的价值方差图

# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.plot(round, FairSort_exposure_quality_var, label='fairsort')  # Plot more data on the axes...
ax.plot(round, TFROM_exposure_quality_var, label='tfrom')  # Plot some data on the axes.
# ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend() # Add a legend.
ax.grid(True)
plt.show()

# title:
#   0: satisfaction_Total
#   1:NDCG_Var
#   2:exposure_var
#   3:
# def resultAnalysis_Online(dataSetName,BestResultFilePath,title):
#     if(dataSetName=="ctrip"):
#         pass
#     elif(dataSetName=="amazon"):
#         X=[x for x in range(18510)]
#         Ctrip_FairSort_quality_csv = pd.read_csv(
#             '../datasets/results/result_ctrip/FairSortOnLine/FairSortQualityOn8_1_0.9.csv', encoding="gbk")
#
#         for modelName , path in BestResultFilePath:

