#coding=UTF-8
__author__ = 'S.CHENG'
'''
  Provides methods according MAB framework.
'''
from user import *
import numpy as np

def riskAverse(userL, target, c1, c2, k):
	#power.*(p - c1 *power.* p .* (1-p)) + c2.*sqrt(2*log(k)./(n+1))
	signal = [0]*len(userL)
	indexList = []
	expReduc = 0
	for i in range(len(userL)):
		T = userL[i].get_userChosenTimes()
		p = userL[i].get_userObserProb()
		power   = userL[i].get_userPower()
		index = power*(p - c1*power*p*(1-p)) + c2*np.sqrt(2*np.log(k)/(T+1)) 
		indexList.append([i, index, power*p, power, p])
	indexList.sort(key=takeIndex, reverse=True)
	for i in range(len(userL)):
		if(userL[indexList[i][0]].get_userState() >= 0):
			expReduc += indexList[i][2]
			signal[indexList[i][0]] = 1
			if (expReduc >= target):
				break
	return signal

def CUCBAVG(userL, target, c1, c2, k):
	#power.*p + c2.*sqrt(2*log(k)./(n+1))
	signal = [0]*len(userL)
	indexList = []
	expReduc = 0
	for i in range(len(userL)):
		T = userL[i].get_userChosenTimes()
		p = userL[i].get_userObserProb()
		power   = userL[i].get_userPower()
		index = power*p + c2*np.sqrt(2*np.log(k)/(T+1)) 
		indexList.append([i, index, power*p, power, p])
	indexList.sort(key=takeIndex, reverse=True)
	for i in range(len(userL)):
		if(userL[indexList[i][0]].get_userState() >= 0):
			expReduc += indexList[i][2]
			signal[indexList[i][0]] = 1
			if (expReduc >= target):
				break
	return signal

def convenMethod(userL, target, meanPower):
	signal = [0]*len(userL)
	chosenUserList = np.random.choice(len(userL), int(target/meanPower))
	for i in range(len(chosenUserList)):
		signal[chosenUserList[i]] = 1
	return signal

def takeIndex(element):
	return element[1]