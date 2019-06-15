#coding=UTF-8
__author__ = 'S.CHENG'
'''
This code is the simulation of following paper:
Li Y, Hu Q, Li N. Learning and selecting the right customers for reliability: A multi-armed bandit approach.

lib required: numpy, matplotlib.
'''
import numpy as np
import matplotlib.pyplot as plt

from user import *
from MAB_method import *
from Load_simulation import *

#global variable
userNum = 500			#the count of users
#eventNum = 200			#the count of demand response event
eventNum = 50
optoutDelay = -5			#the wait gap when user opt-out
tempDelay = -20			#the wait gap when user temperature rise or other situation occurs
methodNum = 5			#the count of used method
maxTime = 30
probC = 0.8			#following four item are the distribution parament of users' load
probV = 0.05
powerC = 1.0
powerV = 0.15

meanPower = 0
varPower = 0.0
c_1 = c_2 = 0			#c_1 and c_2 are control parament
userList = []
obsList  = []			#if necessary, additional obslist is accessable to match methodNum
realList = []
chosenN  = [[0]*eventNum]*methodNum
optOutN  = [[0]*eventNum]*methodNum
realDecN = [[0]*eventNum]*methodNum
optOut   = [0]*userNum
signalN  = [[0]*userNum]*methodNum
feedBack = [[0]*userNum]*methodNum
for i in range(userNum):
	userList.append(user())
	obsList.append([i,0.1])
	realList.append([i,0.1])
target = [120]*eventNum

def main():
	print ("Parament of Initiation:\nThe count of users:", userNum, "\nprobC:", probC, "probV:", probV,
			"\npowerC:", powerC, "powerV:", powerV)
	userInit(userList, probC, probV, powerC, powerV)
	meanPower,varPower = get_userInfo(userList)
	print("mean of Power:", meanPower, "\nvariance of Power:", varPower)
	c_1 = 0.1*meanPower/varPower;
	c_2 = 2.0*meanPower;
	
	#print(obsList)
	for eventI in range(1,eventNum+1):
		signalN[0] = riskAverse(userList, target[eventI-1], c_1, c_2, eventI)
		signalN[1] = convenMethod(userList, target[eventI-1], meanPower)
		
		realDecN[0][eventI-1], optOut, feedBack[0] = loadSimu(userList, signalN[0])
		userUpdata(userList, signalN[0], feedBack[0], optoutDelay, maxTime, tempDelay)
		realDecN[1][eventI-1], optOut, feedBack[1][eventI-1] = loadSimu(userList, signalN[1])
		chosenN[0][eventI-1] = np.sum(signalN[0])
		optOutN[0][eventI-1] = np.sum(optOut)

		# for i in range(methodNum):
		# 	chosenN[i][eventI-1] = np.sum(signalN[i])
		# 	optOutN[i][eventI-1] = np.sum(optOut)

		# if(eventI%10 == 0):
		# 	print(i)
		# 	print(signalN[0])
	
	print(realDecN[0][0:100], chosenN[0][0:100], optOutN[0][0:100])	
	# get_allUserObs(userList, obsList)
	# #print(realDecN[1][0:100], chosenN[1][0:100], optOutN[1][0:100])	
	# print(obsList[0:100])
	
	get_allUserReal(userList, realList)
	get_allUserObs(userList, obsList)
	X1 = []
	Y1 = []
	Y2 = X2 = np.linspace(0.6,1.0,50)
	for i in range(len(obsList)):
		Y1.append(obsList[i][1])
		X1.append(realList[i][1])

	plt.scatter(X1,Y1, s=5, alpha=.5)
	plt.plot(X2,Y2)
	plt.show()

if __name__ == '__main__':
	main()