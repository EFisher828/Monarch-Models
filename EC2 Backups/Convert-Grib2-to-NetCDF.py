# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:54:52 2024

@author: Administrator
"""

import os
import iris

baseDir = "C:/Users/Administrator/Documents/MonarchModels/Data/GFS/MostRecent"

for file in os.listdir(baseDir):
    input_filename = os.path.join(baseDir,file)
    
    output_filename = input_filename.split('.')[0] + '.nc'
            
    cubes = iris.load(input_filename)
    iris.save(cubes,output_filename)