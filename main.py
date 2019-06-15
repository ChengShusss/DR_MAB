#coding=UTF-8
__author__ = 'S.CHENG'
'''
This code is the simulation of following paper:
Li Y, Hu Q, Li N. Learning and selecting the right customers for reliability: A multi-armed bandit approach.

lib required: numpy, matplotlib.
'''
import time
import numpy as np
import matplotlib.pyplot as plt

from user import *
from MAB_method import *
from Load_simulation import *

#global variable
userNum = 500			#the count of users
eventNum = 100			#the count of demand response event
optoutDelay = -5			#the wait gap when user opt-out
tempDelay = -20			#the wait gap when user temperature rise or other situation occurs
methodNum = 2			#the count of used method
maxTime = 30
probC = 0.8			#following four item are the distribution parameter of users' load
probV = 0.05
powerC = 1.0
powerV = 0.15

meanPower = 0
varPower = 0.0
c_1 = c_2 = 0			#c_1 and c_2 are control parameter
userList = []
obsList  = []			#if necessary, additional obslist is accessible to match methodNum
realList = []
X = range(eventNum)
chosenN  = [[0]*eventNum]*methodNum
optOutN  = [[0]*eventNum]*methodNum
realDecN = []
for i in range(methodNum):
	realDecN.append([0]*eventNum)
optOut   = [0]*userNum
signalN  = [[0]*userNum]*methodNum
feedBack = [[0]*userNum]*methodNum
for i in range(userNum):
	userList.append(user())
	obsList.append([i,0.1])
	realList.append([i,0.1])
target = [150]*eventNum

def main():
	startTime = time.process_time()
	print ("Parameter of Initiation:\nThe count of users:", userNum, "\nprobC:", probC, "probV:", probV,
			"\npowerC:", powerC, "powerV:", powerV)
	userInit(userList, probC, probV, powerC, powerV)
	meanPower,varPower = get_userInfo(userList)
	get_allUserReal(userList, realList)
	print("mean of Power:", meanPower, "\nvariance of Power:", varPower,'\n')
	c_1 = 0.1*meanPower/varPower;
	c_2 = 2.0*meanPower;


	fig = plt.figure(figsize=(12, 7))
	ax1 = plt.subplot(221)
	ax1.set_xlim(0,eventNum)
	ax1.set_ylim(int(min(target)*0.6),int(max(target)*1.5))
	ax2 = plt.subplot(222)
	ax2.set_xlim(0,1.0)
	ax2.set_ylim(0,1)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	
	#print(obsList)
	for eventI in range(1,eventNum+1):
		signalN[0] = riskAverse(userList, target[eventI-1], c_1, c_2, eventI)
		signalN[1] = convenMethod(userList, target[eventI-1], meanPower)
		realDecN[0][eventI-1], optOut, feedBack[0] = loadSimu(userList, signalN[0])
		userUpdata(userList, signalN[0], feedBack[0], optoutDelay, maxTime, tempDelay)
		realDecN[1][eventI-1], optOut, feedBack[1] = loadSimu(userList, signalN[1])
		chosenN[0][eventI-1] = np.sum(signalN[0])
		optOutN[0][eventI-1] = np.sum(optOut)

		X1 = list(range(eventI))
		ax1.scatter(X1, realDecN[0][0:eventI], s=35, marker='2', color='b')
		ax1.scatter(X1, realDecN[1][0:eventI], s=15, marker='d', color='r')
		ax1.plot(X1, target[0:eventI], ls='--', color='grey')

		get_allUserObs(userList, obsList)
		X21 = []
		Y21 = []
		Y22 = X22 = np.linspace(0.6,1.0,50)
		for i in range(len(obsList)):
			Y21.append(obsList[i][1])
			X21.append(realList[i][1])
		ax2.cla()
		ax2.scatter(X21, Y21 , s=5, color='b')
		ax2.plot(X22, Y22)
		
		plt.pause(0.001)

	print("Finished at time {}s".format(float(time.process_time() - startTime)))
	plt.show()
	

if __name__ == '__main__':
	main()