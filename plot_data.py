# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:34:41 2023

Python script containing all functions to plot data 
"""
import os

import pandas as pd

import datetime as dt

import numpy as np

# from astral import Astral #Daily sunrise and sunset info

#import pytz # For the timezone (UTC->Europe/MAdrid)


import matplotlib.pyplot as plt


import math

varnames = ['G001901.RADS01#10MN.AVG', 'G001901.RADS02#10MN.AVG',
       'G001901.RADL01#10MN.AVG', 'G001901.RADL02#10MN.AVG',
       'G001901.SHFX01#10MN.AVG', 'G001901.WVFX01#10MN.AVG',
       'G001901.HFXS01#10MN.AVG', 'G001901.TMPA01#10MN.AVG',
       'G001901.TMPA02#10MN.AVG', 'G001901.TMPA03#10MN.AVG',
       'G001901.WSPD01#10MN.AVG', 'G001901.WSPD02#10MN.AVG',
       'G001901.WSPD03#10MN.AVG', 'G001901.WDIR01#10MN.AVG',
       'G001901.CDCN01#10MN.AVG', 'G001901.WVCN01#10MN.AVG',
       'G001901.RHMA01#10MN.AVG', 'G001901.SPWV01#10MN.AVG',
       'G001901.UXWS01#10MN.STD', 'G001901.UYWS01#10MN.STD',
       'G001901.UZWS01#10MN.STD', 'G001901.CXCZ01#10MN.SMP',
       'G001901.CYCZ01#10MN.SMP', 'G001901.CDCZ01#10MN.SMP',
       'G001901.CDCZ02#10MN.AVG', 'G001901.CDFX01#10MN.AVG',
       'G001901.FRVL01#10MN.SMP', 'G001901.VTCZ01#10MN.SMP',
       'G001901.PCTR01#10MN.SMP', 'G001901.PRES01#10MN.AVG',
       'G001901.DNSA02#10MN.AVG', 'G001901.VGCC02#10MN.MIN',
       'G001901.TMPS01#10MN.SMP', 'G001901.TMPS02#10MN.SMP',
       'G001901.TMPS03#10MN.SMP', 'G001901.TMPS04#10MN.SMP',
       'G001901.TMPS05#10MN.SMP', 'G001901.TMPB16#10MN.SMP',
       'G001901.TMPB15#10MN.SMP', 'G001901.TMPB14#10MN.SMP',
       'G00101.TMPB13#10MN.SMP', 'G001901.TMPB12#10MN.SMP',
       'G001901.TMPB11#10MN.SMP', 'G001901.TMPB10#10MN.SMP',
       'G001901.TMPB09#10MN.SMP', 'G001901.TMPB08#10MN.SMP',
       'G001901.TMPB07#10MN.SMP', 'G001901.TMPB06#10MN.SMP',
       'G001901.TMPB05#10MN.SMP', 'G001901.TMPB04#10MN.SMP',
       'G001901.TMPB03#10MN.SMP', 'G001901.TMPB02#10MN.SMP',
       'G001901.TMPB01#10MN.SMP', 'G001901.HFCS01#10MN.SMP',
       'G001901.TMPR01#10MN.AVG', 'G001901.RHMS04#10MN.SMP',
       'G001901.RHMS03#10MN.SMP', 'G001901.RHMS02#10MN.SMP',
       'G001901.RHMS01#10MN.SMP', 'G001901.CNEL04#10MN.SMP',
       'G001901.CNEL03#10MN.SMP', 'G001901.CNEL02#10MN.SMP',
       'G001901.CNEL01#10MN.SMP', 'G001901.WDIR01#10MN.STD',
       'G001901.WSPD01#10MN.STD', 'G001901.WSPD02#10MN.STD',
       'G001901.WSPD03#10MN.STD', 'G001901.WSPD01#10MN.MAX',
       'G001901.WSPD02#10MN.MAX', 'G001901.WSPD03#10MN.MAX',
       'G001901.WSPD01#10MN.MIN', 'G001901.WSPD02#10MN.MIN',
       'G001901.WSPD03#10MN.MIN', 'G001901.TMPI01#10MN.AVG',
       'G001901.TMPA01#10MN.STD', 'G001901.TMPA02#10MN.STD',
       'G001901.TMPA03#10MN.STD', 'G001901.TMPA01#10MN.MIN',
       'G001901.TMPA02#10MN.MIN', 'G001901.TMPA03#10MN.MIN',
       'G001901.TMPA01#10MN.MAX', 'G001901.TMPA02#10MN.MAX',
       'G001901.TMPA03#10MN.MAX', 'G001901.CDCZ07#10MN.SMP',
       'G001901.CDSS01#10MN.AVG', 'G001901.WVSS01#10MN.AVG',
       'G001901.TMPA04#10MN.AVG', 'G001901.TMPA04#10MN.STD',
       'G001901.TMPA04#10MN.MIN', 'G001901.TMPA04#10MN.MAX']

varnames = ['SWD', 'SWU', 'LWD', 'LWU', 'H', 'L',  'G', 'T10m', 'T6m', 'T4m', 'WS 10m', 'WS 6m', 'WS 4m' , 'WDir 4m' , 'CO2 conc', 'WV dens', 'RH 2m', 'ew' , "u'", "v'", "w'", "u'w'", "v'w'" ,"c'w'", 'Tsuelo 0m', 'Tsuelo 0.05m', 'Tsuelo 0.10m', 'Tsuelo 0.2m', 'Tsuelo 0.5m', 'Tsuelo 1m', 'Tsuelo 1.5m', 'Tsuelo 2m', 'Tsuelo 1.5m', 'Tsuelo 2m', 'Tsuelo 3m', 'Tsuelo 5m', 'Tsuelo 7.5m', 'Tsuelo 10m', 'Tsuelo 10.5m', 'Tsuelo 20m', 'none', 'none' , 'none' , 'none' , 'none' , 'none', 'none', 'WDir std', 'WS std 10m',  'WS std 6m', 'WS std 4m', 'WS max 10m',  'WS max 6m', 'WS max 4m', 'WS min 10m',  'WS min 6m', 'WS min 4m', 'Tint', 'T std 10m',  'T std 6m', 'T std 4m', 'T max 10m',  'T max 6m', 'T max 4m', 'T min 10m',  'T min 6m', 'T min 4m', 'Corr, term C02 flux', 'C02 signal strength', 'H20v signal strength', 'WD anem', 'WS anem', 'Ws anem max', 'T suelo media','Cont volumetrico del agua', 'G']


var_code = ('G001901.WSPD01#10MN.AVG','G001901.WSPD02#10MN.AVG','G001901.WSPD03#10MN.AVG')
legend_label = ('10m', '6m', '4m')
colors = ('lightskyblue', 'coral', 'limegreen')
var_name = 'Wind Speed'
unit = 'm/s'
    
fig, ax =plt.subplots(1,1, figsize=(12,7))
# plt.subplots_adjust(, hspace=0.5)
for idx in np.arange(3):
    ax.plot(data_fin.index, data_fin[var_code[idx]], linewidth=1.5, color = colors[idx])
    ax.fill_between(data_fin.index,
                    data_fin[var_code[idx]] + data_fin_std[var_code[idx]],
                    data_fin[var_code[idx]] - data_fin_std[var_code[idx]],
                    alpha=0.2, facecolor=colors[idx],
                    linewidth=4, antialiased=True)

ax.set_title('Average day (August-September-October) in El Arenosillo (INTA)')
ax.set_ylabel(unit)
ax.set_xlabel(r'Local hour')
ax.grid()
ax.legend(labels = legend_label)
ax.set_xticks(data_fin.index)
ax.tick_params(axis = 'x', labelrotation=0)
ax.xaxis.grid(True, which='minor')
ax.set_yscale('linear')
# ax.set_ylim(0.03, 13)


plt.show()
#plt.savefig(saveplot+'\\Turb_oarameters.jpg', bbox_inches = 'tight')
plt.close()
print('Ended.')
