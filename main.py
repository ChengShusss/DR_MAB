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
eventNum = 400			#the count of demand response event
optoutDelay = -5			#the wait gap when user opt-out
tempDelay = -20			#the wait gap when user temperature rise or other situation occurs
methodNum = 2			#the count of used method
maxTime = 30
probC = 0.7			#following four item are the distribution parameter of users' load
probV = 0.08
powerC = 1.0
powerV = 0.15

fontdic = {'family' : 'Times New Roman',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 25}

meanPower = 0
varPower = 0.0
c_1 = c_2 = 0			#c_1 and c_2 are control parameter
userList = []
obsList  = []			#if necessary, additional obslist is accessible to match methodNum
realList = []
#X = range(eventNum)
chosenN  = []
optOutN  = []
realDecN = []
signalN  = []
feedBack = []
for i in range(methodNum):
	realDecN.append([0]*eventNum)
	signalN.append([0]*userNum)
	feedBack.append([0]*userNum)
	chosenN.append([0]*eventNum)
	optOutN.append([0]*eventNum)
optOut   = [0]*userNum
for i in range(userNum):
	userList.append(user())
	obsList.append([i,0.1])
	realList.append([i,0.1])
target = [120]*eventNum

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
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	
	#print(obsList)
	for eventI in range(1,eventNum+1):
		signalN[0] = riskAverse(userList, target[eventI-1], c_1, c_2, eventI)
		signalN[1] = convenMethod(userList, target[eventI-1], meanPower)
		realDecN[0][eventI-1], optOut, feedBack[0] = loadSimu(userList, signalN[0])
		optOutN[0][eventI-1] = np.sum(optOut)
		chosenN[0][eventI-1] = np.sum(signalN[0])
		userUpdata(userList, signalN[0], feedBack[0], optoutDelay, maxTime, tempDelay)
		realDecN[1][eventI-1], optOut, feedBack[1] = loadSimu(userList, signalN[1])
		optOutN[1][eventI-1] = np.sum(optOut)
		chosenN[1][eventI-1] = np.sum(signalN[1])
		
		

		X1 = list(range(eventI))
		ax1.cla()
		ax1.set_xlim(0,eventNum)
		ax1.set_ylim(int(min(target)*0.4),int(max(target)*1.8))
		ax1.set_title("Actual Reduction", fontdict=fontdic)
		I11 = ax1.scatter(X1, realDecN[0][0:eventI], s=35, marker='2', color='r', label='Risk-Averse')
		I12 = ax1.scatter(X1, realDecN[1][0:eventI], s=15, marker='d', color='b', label='Conventional method')
		I13 = ax1.plot(X1, target[0:eventI], ls='--', color='grey', label='Target')
		ax1.legend(loc='upper right',prop={'family':'Times New Roman', 'size':10})

		
		X21 = []
		Y21 = []
		Y22 = X22 = np.linspace(0.4,1.0,50)
		get_allUserObs(userList, obsList)
		for i in range(len(obsList)):
			Y21.append(obsList[i][1])
			X21.append(realList[i][1])
		color2 = ['b']*userNum
		for i in range(userNum):
			if(signalN[0][i] == 1):
				if(optOut[i] == 1):
					color2[i] = 'r'
				else:
					color2[i] = 'g'
		ax2.cla()
		ax2.set_xlim(0.4,1)
		ax2.set_ylim(-0.1,1.1)
		ax2.set_title("Knowledge of Users", fontdict=fontdic)
		ax2.scatter(X21, Y21 , s=1, color=color2)
		ax2.plot(X22, Y22)

		ax3.cla()
		ax3.set_xlim(0,eventNum)
		ax3.set_ylim(0,userNum*0.4)
		ax3.set_title("The count of user opt-out", fontdict=fontdic)
		#ax3.scatter(X21, Y21 , s=1, color=color2)
		ax3.plot(X1, optOutN[0][0:eventI], color='r')
		ax3.plot(X1, optOutN[1][0:eventI], color='b')
		ax3.plot(X1, chosenN[0][0:eventI], color='g')
		ax3.plot(X1, chosenN[1][0:eventI], color='grey')
		
		plt.pause(0.001)

	print("Finished at time {}s".format(float(time.process_time() - startTime)))
	plt.show()
	

if __name__ == '__main__':
	main()