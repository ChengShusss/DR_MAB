#coding=UTF-8
__author__ = 'S.CHENG'
import numpy as np


class user:
	realProb = 0.0
	obserProb = 0.0
	chosenTimes = 0
	state = 0
	power = 1

	def set_userPara(self, rP=0.0, oP = 0.0, cT=0, s=0, p=1):
		self.realProb = rP
		self.obserProb = oP
		self.chosenTimes = cT
		self.state = s
		self.power = p

	def set_userRealProb(self, rP):
		self.realProb = rP
		#print("set_userRealProb:", realProb)

	def set_userObserProb(self, oP):
		self.obserProb = oP

	def set_userChoseTimes(self, cT):
		self.chosenTimes = cT

	def set_userState(self, s):
		self.state = s

	def set_userPower(self, p):
		self.power = p

	def get_userRealProb(self):
		return self.realProb

	def get_userObserProb(self):
		return self.obserProb

	def get_userChoseTimes(self):
		return self.chosenTimes

	def get_userState(self):
		return self.state

	def get_userPower(self):
		return self.power

	def display():
		print("UserInfo:\nrealProb:", self.realProb, "obserProb:", self.obserProb, 
				"\nchosenTimes:", self.chosenTimes,	"state:", self.state,
				"\npower:", self.power)


def userInit(userL, prob_c = 0.8, prob_v=0.05, power_c = 1.0, power_v= 0.1):
	#generate user probablity and power distribution
	probDis = np.random.randn(len(userL))*prob_v + prob_c
	#in case that prob is geater than 1	
	powerDis = np.random.randn(len(userL))*power_v + power_c
	for i in range(0,len(userL)):
		if (probDis[i]>1.0):
			probDis[i] = 1.0
			print ("100% willness occurs")
		if (probDis[i]<0.0):
			probDis[i] = 0.0
			print ("0% willness occurs")
		if (powerDis[i]<0.0):
			powerDis[i] = 0.0
			print ("0 kW load occurs")
		userL[i].set_userRealProb(probDis[i])
		userL[i].set_userPower(powerDis[i])
		userL[i].set_userObserProb(prob_c)
		#print(i, ":", userL[i].realProb, ",", userL[i].power)
	return userL
	
def get_userInfo(userL):
	exPowerList = []
	for i in range(0, len(userL)):
		exPowerList.append(userL[i].get_userRealProb()*userL[i].get_userPower())
	evgPower = np.mean(exPowerList)
	variPower = np.var(exPowerList)
	return evgPower, variPower

def get_allUserObs(userL, ObsL):
	for i in range(len(userL)):
		ObsL[i][1] = userL[i].get_userObserProb()

def userUpdata(userI, feedback, optDelay, maxT, tempDelay):
	if(feedback == 0):
		userI.set_userState(optDelay)
		userObs = userI.get_userObserProb()*(userI.get_userChoseTimes()/(userI.get_userChoseTimes()+1))
		userI.set_userObserProb(userObs)
	elif(feedback == 1):
		userObs = (userI.get_userObserProb()*userI.get_userChoseTimes()+1)/(userI.get_userChoseTimes()+1)
		userI.set_userObserProb(userObs)
		if(userI.get_userState() > maxT):
			userI.set_userState(tempDelay)	
	userI.set_userChoseTimes(UserI.get_userChoseTimes()+1)