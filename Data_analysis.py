#coding=UTF-8
__author__ = 'S.CHENG'

import numpy as np
import matplotlib.pyplot as plt

fontdic = {'family' : 'Times New Roman',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 20}

def plotAll(decData, optData, userData, colorData, info):
	fig = plt.figure(figsize=(12, 7))
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)

	target = decData.iloc[0].tolist()
	decU   = decData.iloc[1].tolist()
	decC   = decData.iloc[2].tolist()
	userX  = userData.iloc[0].tolist()
	Y22 = X22 = np.linspace(0.4,1.0,50)
	axisLim = [[0,info['eventNum']],
				[int(min(min(target), min(decU), min(decC))*0.9),
					 int(max(max(target), max(decU), max(decC))*1.1)],
				[0.4,1],[-0.1,1.1],
				[0,info['eventNum']],[0,(info['userNum'])*0.1],
				[],
				[]]
	X1 = list(range(info['eventNum']))
	loopL = list(range(0, info['eventNum'], int(info['eventNum']/30)))
	loopL.append(info['eventNum'] - 1)
	for i in loopL:
		#fig of reduction
		ax1.cla()
		ax1.set_xlim(axisLim[0][0], axisLim[0][1])
		ax1.set_xlabel("Time", fontdict=fontdic, size=15, x= 0.95, y=-0.2)
		ax1.set_ylabel("Real reduction", fontdict=fontdic, size=15)
		ax1.set_ylim(axisLim[1][0], axisLim[1][1])
		ax1.set_title("Actual Reduction", fontdict=fontdic)
		I11 = ax1.scatter(X1[0:i+1], decData.iloc[1,0:i+1], s=35, marker='2',
						 color='r', label='Risk-Averse')
		I12 = ax1.scatter(X1[0:i+1], decData.iloc[2,0:i+1], s=5, marker='d',
						 color='b', label='Conventional method')
		I13 = ax1.plot(X1[0:i+1], decData.iloc[0,0:i+1], ls='--', color='grey', label='Target')
		ax1.legend(loc='upper right',prop={'family':'Times New Roman', 'size':10})

		#fig of knowledge of users
		ax2.cla()
		ax2.set_xlim(axisLim[2][0], axisLim[2][1])
		ax2.set_ylim(axisLim[3][0], axisLim[3][1])
		ax2.set_xlabel("Actual Prob distribute", fontdict=fontdic, size='small')
		ax2.set_ylabel("Thought Prob distribute", fontdict=fontdic, size='small')
		ax2.set_title("Knowledge of Users", fontdict=fontdic)
		colorSet = colorData.iloc[i].tolist()
		ax2.scatter(userX, userData.iloc[i+1].tolist(), s=1, color=colorSet)
		ax2.plot(X22, Y22)

		#fig of the count of chosen users and opt-out users
		ax3.cla()
		ax3.set_xlim(axisLim[4][0], axisLim[4][1])
		ax3.set_ylim(axisLim[5][0], axisLim[5][1])
		ax3.set_xlabel("Time", fontdict=fontdic, size='small')
		ax3.set_ylabel("User opt-outs", fontdict=fontdic, size='small')
		ax3.set_title("The count of user opt-out", fontdict=fontdic)
		#ax3.scatter(X21, Y21 , s=1, color=color2)
		ax3.plot(X1[0:i+1], optData.iloc[0, 0:i+1], color='r')
		ax3.plot(X1[0:i+1], optData.iloc[1, 0:i+1], color='b')
		ax3.plot(X1[0:i+1], optData.iloc[2, 0:i+1], color='g')
		ax3.plot(X1[0:i+1], optData.iloc[3, 0:i+1], color='grey')

		plt.pause(0.001)

	plt.show()		#to retain image





#subplot loaction adjustment: https://www.zhihu.com/question/21953954