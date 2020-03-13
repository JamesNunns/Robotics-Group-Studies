#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:02:23 2020

@author: will
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv("./Nao_readout_timings.csv")

print data

calls = data['calls']
joint_calls = data['joint_calls']

joints = data['joints']
get_posture = data['get_p']
set_posture = data['set_p']
get_accel = data['set_a']


fig, ax1 = plt.subplots()

ax1.set_title('Nao Response Times')
ax1.set_ylabel('Time')
ax1.set_xlabel('Number of Calls')

ax1.plot(joint_calls, joints, label="Move Joint")
ax1.plot(joint_calls, set_posture, label)