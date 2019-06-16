#coding=UTF-8
__author__ = 'S.CHENG'
'''
This code is the simulation of following paper:
Li Y, Hu Q, Li N. Learning and selecting the right customers for reliability: A multi-armed bandit approach.

lib required: numpy, matplotlib.
'''
import csv
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from user import *
from MAB_method import *
from Data_analysis import *
from Load_simulation import *

#global variable
userNum = 2000			#the count of users
eventNum = 400			#the count of demand response event
optoutDelay = -5			#the wait gap when user opt-out
tempDelay = -10			#the wait gap when user temperature rise or other situation occurs
methodNum = 2			#the count of used method
maxTime = 30
probC = 0.9			#following four item are the distribution parameter of users' load
probV = 0.1
powerC = 1.0
powerV = 0.15
meanPower = 0
varPower = 0.0
c_1 = c_2 = 0			#c_1 and c_2 are control parameter
userList = []
obsList  = []			#if necessary, additional obslist is accessible to match methodNum
realList = []
chosenN  = []
optOutN  = []
realDecN = []
signalN  = []
feedBack = []
Info = {
		'userNum':userNum,
		'eventNum':eventNum}
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
target = [400]*eventNum

def main():
	print("Program Started at:", time.asctime(time.localtime(time.time())))
	startTime = time.process_time()
	print(" Parameter of Initiation:\n   The count of users:", userNum,
			"\n   probC:", probC, "probV:", probV,
			"\n   powerC:", powerC, "powerV:", powerV)
	userInit(userList, probC, probV, powerC, powerV)
	meanPower,varPower = get_userInfo(userList)
	get_allUserReal(userList, realList)
	userIndex = []
	userReal = []
	for i in range(userNum): 
		userIndex.append("user"+str(i+1))
		userReal.append(realList[i][1])
	with open('UserKnowledge.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)  
		reducCsv.writerow(userIndex)
		reducCsv.writerow(userReal)
	with open('UserKnowledgeColor.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)  
		reducCsv.writerow(userIndex)
	print("   mean of Power:", meanPower, "\n   variance of Power:", varPower,'\n')
	c_1 = 0.1*meanPower/varPower;
	c_2 = 2.0*meanPower;
	
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
		
		Y21 = []
		get_allUserObs(userList, obsList)
		for i in range(len(obsList)):
			Y21.append(obsList[i][1])
		color2 = ['b']*userNum
		for i in range(userNum):
			if(signalN[0][i] == 1):
				if(optOut[i] == 1):color2[i] = 'r'
				else:color2[i] = 'g'

		with open('UserKnowledge.csv','a', newline='') as CSVFile: 
			reducCsv=csv.writer(CSVFile)  
			reducCsv.writerow(Y21)
		with open('UserKnowledgeColor.csv','a', newline='') as CSVFile: 
			reducCsv=csv.writer(CSVFile)  
			reducCsv.writerow(color2)

	with open('Reduction.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)  
		reducCsv.writerow(list(range(1, eventNum+1)))
		reducCsv.writerow(target)
		reducCsv.writerow(realDecN[0])
		reducCsv.writerow(realDecN[1])
	with open('Optout.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)  
		reducCsv.writerow(list(range(1, eventNum+1)))
		reducCsv.writerow(optOutN[0])
		reducCsv.writerow(optOutN[1])
		reducCsv.writerow(chosenN[0])
		reducCsv.writerow(chosenN[1])

	print("Finished simulation after running for {}s\n".format\
			(float(time.process_time() - startTime)))
	print("Started to analyze data after running for {}s".format\
			(float(time.process_time() - startTime)))
	reducData = pd.read_csv("Reduction.csv")
	optData  = pd.read_csv("Optout.csv")
	userData  = pd.read_csv("UserKnowledge.csv")
	colorData = pd.read_csv("UserKnowledgeColor.csv", dtype=str)
	plotAll(reducData, optData, userData, colorData, Info)

	print("Program finished after running for {}s".format\
			(float(time.process_time() - startTime)))
	
if __name__ == '__main__':
	main()