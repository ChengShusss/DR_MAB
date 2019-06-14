#coding=UTF-8
__author__ = 'S.CHENG'

from user import *
import numpy as np

def loadFeedback(userL, signalL):
	realReduction = 0
	for i in range(signalL):
		if(signalL[i] == 1):
			if(np.random.random() < userL[i].get_userRealProb()):
				pass
			else:
				pass
	return realReduction