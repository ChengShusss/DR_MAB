#coding=UTF-8
__author__ = 'S.CHENG'
import numpy as np

class user:
	realProb = 0.0
	obserProb = 0.0
	chosenTimes = 0
	state = 0
	power = 1
	maxTimes = 15
	#what happen to git 

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

	def set_userChosenTimes(self, cT):
		self.chosenTimes = cT

	def set_userState(self, s):
		self.state = s

	def set_userPower(self, p):
		self.power = p

	def get_userRealProb(self):
		return self.realProb

	def get_userObserProb(self):
		return self.obserProb

	def get_userChosenTimes(self):
		return self.chosenTimes

	def get_userState(self):
		return self.state

	def get_userPower(self):
		return self.power

	def get_userExpDec(self):
		return self.power*self.obserProb

	def display(self):
		print("userL[i]nfo:\nrealProb:", self.realProb, "obserProb:", self.obserProb, 
				"\nchosenTimes:", self.chosenTimes,	"state:", self.state,
				"\npower:", self.power)

def userInit(userL, prob_c = 0.8, prob_v=0.05, power_c = 1.0, power_v= 0.1):
	#generate user probablity and power distribution
	probDis = np.random.randn(len(userL))*prob_v + prob_c
	#in case that prob is geater than 1	
	powerDis = np.random.randn(len(userL))*power_v + power_c
	for i in range(0,len(userL)):
		# if(probDis[i]>(prob_c-prob_v/2)):
		# 	probDis[i] = np.random.randn()*prob_v/5 + prob_c
		if(probDis[i]>1.0):
			probDis[i] = 1.0
			print ("100% willness occurs")
		if(probDis[i]<0.0):
			probDis[i] = 0.0
			print ("0% willness occurs")
		if(powerDis[i]<0.0):
			powerDis[i] = 0.0
			print ("0 kW load occurs")
		userL[i].set_userRealProb(probDis[i])
		userL[i].set_userPower(powerDis[i])
		obProb = probDis[i]*(0.8+0.4*np.random.random())
		if(obProb > 1.0):
			obProb = 1.0
		userL[i].set_userObserProb(obProb)
		userL[i].set_userChosenTimes(5)
	return userL
	
def get_userInfo(userL):
	#return user information: mean power and variance of power
	exPowerList = []
	for i in range(0, len(userL)):
		exPowerList.append(userL[i].get_userRealProb()*userL[i].get_userPower())
	evgPower = np.mean(exPowerList)
	variPower = np.var(exPowerList)
	return evgPower, variPower

def get_allUserObs(userL, ObsL):
	#return user information: observed prob
	for i in range(len(userL)):
		ObsL[i][1] = userL[i].get_userObserProb()

def get_allUserReal(userL, RealL):
	#return user information: real prob
	for i in range(len(userL)):
		RealL[i][1] = userL[i].get_userRealProb()

def userUpdata(userL, signal, feedback, optDelay, maxT, tempDelay):
	#updata user information according to feedback
	for i in range(len(userL)):
		if(signal[i] == 1):
			T = float(userL[i].get_userChosenTimes())
			p = float(userL[i].get_userObserProb())
			if(feedback[i] == 0):
				userL[i].set_userState(optDelay)
				if(userL[i].get_userChosenTimes() > 0):
					userObs = p*T/(T+1)
					userL[i].set_userObserProb(userObs)
				else:userL[i].set_userObserProb(0.0)		
			elif(feedback[i] == 1):
				if(userL[i].get_userChosenTimes() > 0):
					userObs = (p*T+1)/(T+1)
					if(userObs > 1.0):
						userObs = 1.0
					userL[i].set_userObserProb(userObs)
					if(userL[i].get_userState() > maxT):
						userL[i].set_userState(tempDelay)	
				else:userL[i].set_userObserProb(1.0)
			userL[i].set_userChosenTimes(userL[i].get_userChosenTimes()+1)
		else:
			if(userL[i].get_userState()<0):
				userL[i].set_userState(userL[i].get_userState() + 1)

def userProbVary(userL, rand, mode):
	#for future analysis of handling with users uncertainty
	pass
