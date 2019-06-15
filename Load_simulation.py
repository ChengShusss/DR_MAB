#coding=UTF-8
__author__ = 'S.CHENG'
'''
  Provides methods that simulate the performance of users' load, while there are many factors havn't 
been taken in consideration, whick would be analyzied future.
'''
from user import *
import numpy as np

def loadSimu(userL, signalL):
	realReduction = 0
	optOut = [0]*len(userL)
	feedBack = [0]*len(userL)
	for i in range(len(userL)):
		if(signalL[i] == 1):
			if(np.random.random() < userL[i].get_userRealProb()):
				realReduction += userL[i].get_userPower()
				feedBack[i] = 1
			else:
				optOut[i] = 1
	return realReduction, optOut, feedBack