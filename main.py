#coding=UTF-8
__author__ = 'S.CHENG'
'''
This code is the simulation of following paper:
Li Y, Hu Q, Li N. Learning and selecting the right customers for reliability: A multi-armed bandit approach.

lib required: numpy, matplotlib.
'''
import numpy as np
import matplotlib as plt

from user import *

#global variable
userNum = 500			#the count of users
eventNum = 200			#the count of demand response event
optoutDelay = 5			#the wait gap when user opt-out
tempDelay = -20			#the wait gap when user temperature rise or other situation occurs
methodNum = 2			#the count of used method
prob_c = 0.8			#following four item are the distribution parament of users' load
prob_v = 0.05
power_c = 1.0
power_v = 0.15

meanPower = 0
varPower = 0.0
c_1 = c_2 = 0			#c_1 and c_2 are control parament
userList = []
obsList = []
signalList = [0]*userNum
chosenN  = [[0]*eventNum]*methodNum
optoutN  = [[0]*eventNum]*methodNum
realDecN = [[0]*eventNum]*methodNum
for i in range(userNum):
	userList.append(user())
	obsList.append([i,0.1])
target = [120]*eventNum

def main():
	print ("Parament of Initiation:\nThe count of users:", userNum, "\nprob_c:", prob_c, "prob_v:", prob_v,
			"\npower_c:", power_c, "power_v:", power_v)
	user_init(userList, prob_c, prob_v, power_c, power_v)
	meanPower,varPower = get_userInfo(userList)
	print("mean of Power:", meanPower, "\nvariance of Power:", varPower)
	c_1 = 0.1*meanPower/varPower;
	c_2 = 2.0*meanPower;
	get_allUserObs(userList, obsList)

if __name__ == '__main__':
	main()