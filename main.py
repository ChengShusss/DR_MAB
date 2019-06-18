#coding=UTF-8
__author__ = 'S.CHENG'
'''
This code is the simulation of following paper:
Li Y, Hu Q, Li N. Learning and selecting the right customers for reliability: A multi-armed bandit approach.

lib required: numpy, matplotlib, pandas
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
userNum = 3000			#the count of users
eventNum = 400			#the count of demand response event
optoutDelay = -5		#the wait gap when user opt-out
tempDelay = -10			#the wait gap when user temperature rise or other situation occurs
methodNum = 2			#the count of used method
maxTime = 30
#following four item are the distribution parameter of users' load
probC = 0.8				#the exception of user prob
probV = 0.08				#the variance of user prob
powerC = 1.0			#the exception of users' load power
powerV = 0.15			#the variance of users' load power
meanPower = 0
varPower = 0.0
c_1 = c_2 = 0			#c_1 and c_2 are control parameter
userList = []			#userList for MAB method
userListC= []			#userList for conventional method
obsList  = []			#the list of users observed prob
realList = []			#the list of users real prob
chosenN  = []			#the count of chosen users in each event
optOutN  = []			#the count of users who opt out in each event
realDecN = []			#reduction in practice in each event
signalN  = []			#control signal (just for temporary storage of signal in one event)
feedBack = []			#the users' feedback(whether load reduct)
optOut   = [0]*userNum	#the status whether users opt-out
target = [800]*eventNum	#the target of DR

Info = {
		'userNum':userNum,
		'eventNum':eventNum}
#below 'for' sentence is arranged to solve the problem of deep copy 
for i in range(methodNum):
	realDecN.append([0]*eventNum)
	signalN.append([0]*userNum)
	feedBack.append([0]*userNum)
	chosenN.append([0]*eventNum)
	optOutN.append([0]*eventNum)

for i in range(userNum):
	userList.append(user())
	obsList.append([i,0.1])
	realList.append([i,0.1])


def main():
	print("Program Started at:", time.asctime(time.localtime(time.time())))
	startTime = time.process_time()
	print(" Parameter of Initiation:\n   The count of users:", userNum,
			"\n   probC:", probC, "probV:", probV,
			"\n   powerC:", powerC, "powerV:", powerV)
	userInit(userList, probC, probV, powerC, powerV)	#initiate users
	meanPower,varPower = get_userInfo(userList)	
	get_allUserReal(userList, realList)
	print("   mean of Power:", meanPower, "\n   variance of Power:", varPower,'\n')
	c_1 = 0.1*meanPower/varPower;
	c_2 = 2.0*meanPower;

	userIndex = []
	userReal = []
	#prepare for data storage, which would be written in CSV file
	for i in range(userNum): 
		userIndex.append("user"+str(i+1))
		userReal.append(realList[i][1])
	with open(r'Data\UserKnowledge.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)  
		reducCsv.writerow(userIndex)
		reducCsv.writerow(userReal)
	with open(r'Data\UserKnowledgeColor.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)  
		reducCsv.writerow(userIndex)
	
	#the loop statement of demand response
	for eventI in range(1,eventNum+1):
		#get the control signal
		signalN[0] = riskAverse(userList, target[eventI-1], c_1, c_2, eventI)
		signalN[1] = convenMethod(userList, target[eventI-1], meanPower)

		#for simulation of Risk-Averse
		realDecN[0][eventI-1], optOut, feedBack[0] = loadSimu(userList, signalN[0])
		optOutN[0][eventI-1] = np.sum(optOut)
		chosenN[0][eventI-1] = np.sum(signalN[0])
		userUpdata(userList, signalN[0], feedBack[0], optoutDelay, maxTime, tempDelay)

		#for simulation of conventional method
		realDecN[1][eventI-1], optOut, feedBack[1] = loadSimu(userList, signalN[1])
		optOutN[1][eventI-1] = np.sum(optOut)
		chosenN[1][eventI-1] = np.sum(signalN[1])
		
		#store the date for delayed data analysis
		Y21 = []
		get_allUserObs(userList, obsList)
		for i in range(len(obsList)):
			Y21.append(obsList[i][1])
		color2 = ['b']*userNum
		for i in range(userNum):
			if(signalN[0][i] == 1):
				if(optOut[i] == 1):color2[i] = 'r'
				else:color2[i] = 'g'

		with open(r'Data\UserKnowledge.csv','a', newline='') as CSVFile: 
			reducCsv=csv.writer(CSVFile)  
			reducCsv.writerow(Y21)
		with open(r'Data\UserKnowledgeColor.csv','a', newline='') as CSVFile: 
			reducCsv=csv.writer(CSVFile)  
			reducCsv.writerow(color2)

	#store the overall date for delayed data analysis
	with open(r'Data\Reduction.csv','w', newline='') as CSVFile: 
		reducCsv=csv.writer(CSVFile)
		reducCsv.writerow(list(range(1, eventNum+1)))
		reducCsv.writerow(target)
		reducCsv.writerow(realDecN[0])
		reducCsv.writerow(realDecN[1])
	with open(r'Data\Optout.csv','w', newline='') as CSVFile: 
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
	
	#acquire the data of simulation and plot the figure
	reducData = pd.read_csv(r'Data\Reduction.csv')
	optData  = pd.read_csv(r'Data\Optout.csv')
	userData  = pd.read_csv(r'Data\UserKnowledge.csv')
	colorData = pd.read_csv(r'Data\UserKnowledgeColor.csv', dtype=str)
	plotAll(reducData, optData, userData, colorData, Info)

	print("Program finished after running for {}s".format\
			(float(time.process_time() - startTime)))
	
if __name__ == '__main__':
	#ensure code is conducted only this is called by system
	main()