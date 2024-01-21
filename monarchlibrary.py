# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 17:37:30 2024

@author: Administrator
"""

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

class mapStyle:
        class colors:
            colors_rain = [(0.1,0.1,0.1,0),'#00FB4C','#00E445','#00CD3E','#00B537','#009E2E','#018628','#016F20','#005518','#FFFF50','#FCD347','#FBA141','#FF763B','#FF272B','#D80E3A','#B6093D','#900649','#C90DA9','#FF04DC']
            cmap_rain = plt.cm.colors.ListedColormap(colors_rain)
            levels_rain = [0,0.005,0.01,0.025,0.05,0.075,0.1,0.125,0.15,0.2,0.25,0.375,0.5,0.625,0.75,0.875,1,1.5,10]
            norm_rain = BoundaryNorm(levels_rain, cmap_rain.N, clip=True)
            
            colors_snow = [(0.1,0.1,0.1,0),'#02FEFE','#00EAFD','#01D3FD','#03BFFC','#00AAFC','#0092FC','#0275F2','#0459E8','#073AD6','#0D23C4','#0A1DBB','#05159B','#291099','#490C92','#AC0F8B','#CC0D8F','#FF0C80']
            cmap_snow = plt.cm.colors.ListedColormap(colors_snow)
            levels_snow = [0,0.001,0.005,0.01,0.02,0.03,0.04,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.4,0.5,1]
            norm_snow = BoundaryNorm(levels_snow, cmap_snow.N, clip=True)
            
            colors_zr = [(0.1,0.1,0.1,0),'#FAA7B9','#F17FAD','#EC75A6','#DE5A91','#DD578F','#D13D7B','#C6276C','#B80E61','#AA0547','#B90B44','#B71621','#CC1626','#CF1A1E','#DC2C09','#E53206','#FB4100','#FF5215']
            cmap_zr = plt.cm.colors.ListedColormap(colors_zr)
            levels_zr = [0,0.001,0.005,0.01,0.02,0.03,0.04,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.4,0.5,1]
            norm_zr = BoundaryNorm(levels_zr, cmap_zr.N, clip=True)
            
            colors_ip = [(0.1,0.1,0.1,0),'#B2A1FF','#B688FF','#BD75FE','#C560FD','#C257F9','#B938EA','#B52DE4','#AE28DB','#8F13B1','#9113B0','#A61EA0','#B50D9A','#B70E8F','#C92C79','#D13976','#D73F6A','#E04855']
            cmap_ip = plt.cm.colors.ListedColormap(colors_ip)
            levels_ip = [0,0.001,0.005,0.01,0.02,0.03,0.04,0.05,0.075,0.1,0.125,0.15,0.175,0.2,0.25,0.3,0.4,0.5,1]
            norm_ip = BoundaryNorm(levels_ip, cmap_ip.N, clip=True)
            
            colors_accusnow = [(0.1,0.1,0.1,0), '#E1E1E1', '#C8C8C8', '#AFAFAF', '#969696', '#A9E7F2', '#73BFD7', '#3C98BB', '#0270A0', '#0046B0', '#2864BC', '#4D82C8', '#74A0D3','#9ABEDF','#C1DCEB','#C9ADDB','#C195D2','#B97EC9','#B066C1','#A84FB8','#A037AF','#870A47','#971C5A','#A72D6E','#B63F81','#C65095','#D663A8','#EBA7B7','#E89BA1','#E78F8A','#E38274','#E2765D','#DE6A47','#DC8150','#E19568','#E6A97F','#ECBD97','#F1D1AF','#F6E5C6','#FCF9DE']
            cmap_accusnow = plt.cm.colors.ListedColormap(colors_accusnow)
            levels_accusnow = [0, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 40, 44, 48, 52, 56, 60, 1000]
            norm_accusnow = BoundaryNorm(levels_accusnow, cmap_accusnow.N, clip=True)
            
            colors_accuprecip = [(0.1,0.1,0.1,0), '#B1EDCF', '#97D8B7', '#7DC19E', '#62AA85', '#48936D', '#2F7E54', '#15673C', '#15678C', '#337E9F', '#5094B6', '#6EACC8', '#8BC4DE','#A9DBF2','#EBD5EB','#D9BED8','#C5A7C5','#B38FB2','#A0779F','#8E5F8D','#7A4779','#682F67','#6C0233','#87253B','#A54945','#C16E4E','#DE9357','#FAC66C','#FBD479','#FDE385','#FEF192','#FFFF9F']
            cmap_accuprecip = plt.cm.colors.ListedColormap(colors_accuprecip)
            levels_accuprecip = [0,0.01,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,3.5,4,4.5,5,5.5,6,7,8,9,10,12,14,16,20,24,1000]
            norm_accuprecip = BoundaryNorm(levels_accuprecip, cmap_accuprecip.N, clip=True)
