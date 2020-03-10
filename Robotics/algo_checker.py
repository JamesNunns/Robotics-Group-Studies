#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 23:47:22 2020

@author: robgc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# [time, event, ax, ay, az, gx, gy, gz, se0, se1, se2, se3, be, av, cmx, cmy, algo, position]


data = pd.read_csv("/home/robgc/Desktop/Project/Robotics-Group-Studies/Robotics/Output_data/26-03-2019 15:27:54 Tst.txt")

data.columns =["time", "", "", "","", "","", "","", "","", "", "be","", "","", "", "p"]

col = np.where(data["p"] == "extended","r", np.where(data["p"] == "crunched","b", "m"))

plt.scatter(data["time"], data["be"], color=col, s=0.2)