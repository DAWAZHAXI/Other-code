#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Created the fpar/rastercalculation.py in PyCharm on 九月 07 09:32:24 2017
@author:wangyc
计算时间序列栅格相关系数、偏相关系数和复相关系数
R_为相关系数
PR_为偏相关
CR_为复相关
"""
import os
import arcpy
from arcpy.sa import *
import glob
if __name__ == '__main__':
    FvcPath = ur''
    LaiPath = ur''
    GppPath = ur''
    TempPath = ur''
    PrePath = ur""
    outpath = ur""
    ##List files
    tempfilelist = [[f,arcpy.Raster(f)] for f in glob.glob(os.path.join(TempPath,'*.tif'))]
    prefilelist = [[f,arcpy.Raster(f)] for f in glob.glob(os.path.join(PrePath,'*.tif'))]
    Fvcfilelist = [[f,arcpy.Raster(f)] for f in glob.glob(os.path.join(FvcPath,'*.tif'))]
    #Laifilelist = [[f,arcpy.Raster(f)] for f in glob.glob(os.path.join(LaiPath,"*.tif"))]
    #Gppfilelist = [[f,arcpy.Raster(f)] for f in glob.glob(os.path.join(GppPath,"*.tif"))]
    ## Calculate mean
    temp_mean = CellStatistics([tempfilelist[i][1] for i in range(len(tempfilelist))], "MEAN", "DATA")
    pre_mean = CellStatistics([prefilelist[i][1] for i in range(len(prefilelist))],"MEAN","DATA")
    Fvc_mean = CellStatistics([Fvcfilelist[i][1] for i in range(len(Fvcfilelist))],"MEAN","DATA")
    #Lai_mean = CellStatistics([Laifilelist[i][1] for i in range(len(Fvcfilelist))],"MEAN","DATA")
    #Gpp_mean = CellStatistics([Laifilelist[i][1] for i in range(len(Laifilelist))],"MEAN","DATA")
    ####plus
    temp_mean_plus = [tempfilelist[i][1] - temp_mean for i in range(len(tempfilelist))]
    pre_mean_plus = [prefilelist[i][1] - pre_mean for i in range(len(prefilelist))]
    Fvc_mean_plus = [Fvcfilelist[i][1] - Fvc_mean for i in range(len(Fvcfilelist))]
    #Lai_mean_plus = [Laifilelist[i][1] - Lai_mean for i in range(len(Laifilelist))]
    #Gpp_mean_plus = [Gppfilelist[i][1] - Gpp_mean for i in range(len(Gppfilelist))]
    ####plus sum
    temp_pre_sum = sum([temp_mean_plus[i] * pre_mean_plus[i] for i in range(len(temp_mean_plus))])
    temp_Fvc_sum = sum([temp_mean_plus[i] * Fvc_mean_plus[i] for i in range(len(Fvc_mean_plus))])
    pre_Fvc_sum = sum([pre_mean_plus[i] * Fvc_mean_plus[i] for i in range(len(Fvc_mean_plus))])
    #temp_Lai_sum = sum([temp_mean_plus[i] * Lai_mean_plus[i] for i in range(len(Lai_mean_plus))])
    #pre_Lai_sum = sum([pre_mean_plus[i] * Lai_mean_plus[i] for i in range(len(Lai_mean_plus))])
    #temp_Gpp_sum = sum([temp_mean_plus[i] * Gpp_mean_plus[i] for i in range(len(Gpp_mean_plus))])
    #pre_Gpp_sum = sum([pre_mean_plus[i] * Gpp_mean_plus[i] for i in range(len(Gpp_mean_plus))])
    #Fvc_Lai_sum = sum([Fvc_mean_plus[i] * Lai_mean_plus[i] for i in range(len(Lai_mean_plus))])
    #Fvc_Gpp_sum = sum([Fvc_mean_plus[i] * Gpp_mean_plus[i] for i in range(len(Gpp_mean_plus))])
    #Lai_Gpp_sum = sum([Lai_mean_plus[i] * Gpp_mean_plus[i] for i in range(len(Gpp_mean_plus))])

    #pow sum
    temp_pre_pow_sum = sum([Power(i,2) for i in temp_mean_plus]) * sum([Power(i,2) for i in pre_mean_plus])
    temp_Fvc_pow_sum = sum([Power(i,2) for i in temp_mean_plus]) * sum([Power(i,2) for i in Fvc_mean_plus])
    pre_Fvc_pow_sum = sum([Power(i,2) for i in pre_mean_plus]) * sum([Power(i,2) for i in Fvc_mean_plus])
    #temp_Lai_pow_sum = sum([Power(i,2) for i in temp_mean_plus]) * sum([Power(i,2) for i in Lai_mean_plus])
    #pre_Lai_pow_sum = sum([Power(i,2) for i in pre_mean_plus]) * sum([Power(i,2) for i in Lai_mean_plus])
    #temp_Gpp_pow_sum = sum([Power(i,2) for i in temp_mean_plus]) * sum([Power(i,2) for i in Gpp_mean_plus])
    #pre_Gpp_pow_sum = sum([Power(i,2) for i in pre_mean_plus]) * sum([Power(i,2) for i in Gpp_mean_plus])
    #Fvc_Lai_pow_sum = sum([Power(i,2) for i in Fvc_mean_plus]) * sum([Power(i,2) for i in Lai_mean_plus])
    #Fvc_Gpp_pow_sum = sum([Power(i,2) for i in Fvc_mean_plus]) * sum([Power(i,2) for i in Gpp_mean_plus])
    #Lai_Gpp_pow_sum = sum([Power(i,2) for i in Lai_mean_plus]) * sum([Power(i,2) for i in Gpp_mean_plus])

    R_temp_pre = temp_pre_sum / SquareRoot(temp_pre_pow_sum)
    R_temp_Fvc = temp_Fvc_sum / SquareRoot(temp_Fvc_pow_sum)
    R_pre_Fvc = pre_Fvc_sum / SquareRoot(pre_Fvc_pow_sum)
    #R_temp_Lai = temp_Lai_sum / SquareRoot(temp_Lai_pow_sum)
    #R_pre_Lai = pre_Lai_sum / SquareRoot(pre_Lai_pow_sum)
    #R_temp_Gpp = temp_Gpp_sum / SquareRoot(temp_Gpp_pow_sum)
    #R_pre_Gpp = pre_Gpp_sum / SquareRoot(pre_Gpp_pow_sum)
    #R_Fvc_Lai = Fvc_Lai_sum / SquareRoot(Fvc_Lai_pow_sum)
    #R_Fvc_Gpp = Fvc_Gpp_sum / SquareRoot(Fvc_Gpp_pow_sum)
    #R_Lai_Gpp = Lai_Gpp_sum / SquareRoot(Lai_Gpp_pow_sum)

    del tempfilelist,prefilelist,Fvcfilelist,temp_mean,pre_mean,Fvc_mean,temp_mean_plus,pre_mean_plus,Fvc_mean_plus,\
        temp_pre_sum,temp_Fvc_sum,pre_Fvc_sum,temp_pre_pow_sum,temp_Fvc_pow_sum,pre_Fvc_pow_sum

    '''
    PR_tf_p = (R_temp_fpar - R_temp_pre * R_pre_fpar) / SquareRoot((1 - Power(R_temp_pre,2))*(1 - Power(R_pre_fpar,2)))
    PR_pf_t = (R_pre_fpar - R_temp_pre * R_temp_fpar) / SquareRoot((1 - Power(R_temp_pre,2))*(1 - Power(R_temp_fpar,2)))
    T_tf_p = PR_tf_p*14 / SquareRoot(1 - Power(PR_tf_p,2))
    T_pf_t = PR_pf_t*14 / SquareRoot(1- Power(PR_pf_t,2))
    CR_tp_f = SquareRoot(1 - (1 - Power(R_temp_fpar,2))*(1 - Power(PR_pf_t,2)))
    CR_pt_f = SquareRoot(1 - (1 - Power(R_pre_fpar,2))*(1 - Power(PR_tf_p,2)))
    F_tp_f = Power(CR_tp_f,2) / (1 - Power(CR_tp_f,2)) * 6.5
    F_pt_f = Power(CR_pt_f,2) / (1 - Power(CR_pt_f,2)) * 6.5
    arcpy.CopyRaster_management(R_temp_pre,'R_temp_pre.tif')
    R_temp_pre.save(os.path.join(outpath,'R_temp_pre.tif'))
    '''
    R_temp_pre.save(os.path.join(outpath,'R_temp_pre.tif'))
    R_temp_Fvc.save(os.path.join(outpath,'R_temp_Fvc.tif'))
    R_pre_Fvc.save(os.path.join(outpath,'R_pre_Fvc.tif'))
    #R_temp_Lai.save(os.path.join(outpath,'R_temp_Lai.tif'))
    #R_pre_Lai.save(os.path.join(outpath, 'R_pre_Lai.tif'))
    #R_temp_Gpp.save(os.path.join(outpath,'R_temp_Gpp.tif'))
    #R_pre_Gpp.save(os.path.join(outpath, 'R_pre_Gpp.tif'))
    #R_Fvc_Lai.save(os.path.join(outpath, 'R_Fvc_Lai.tif'))
    #R_Fvc_Gpp.save(os.path.join(outpath, 'R_Fvc_Gpp.tif'))
    #R_Lai_Gpp.save(os.path.join(outpath, 'R_Lai_Gpp.tif'))


    #PR_tf_p.save('PR_tf_p.tif')
    #PR_pf_t.save('PR_pf_t.tif')
    #CR_tp_f.save('CR_tp_f.tif')
    #CR_pt_f.save('CR_pt_f.tif')
    #F_tp_f.save('F_tp_f.tif')
    #F_pt_f.save('F_pt_f.tif')
