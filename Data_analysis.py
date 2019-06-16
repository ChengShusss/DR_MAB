import numpy as np
import matplotlib.pyplot as plt

fontdic = {'family' : 'Times New Roman',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 20}

def plotInit():
	fig = plt.figure(figsize=(12, 7))
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	pass
	return fig, ax1, ax2, ax3, ax4

def figUpdata_1(ax, dataX, dataY, xlim, ylim):
	ax.cla()
	ax.set_xlim(xlim[0], xlim[1])
	ax.set_ylim(ylim[0], ylim[1])
	ax.set_title("Actual Reduction", fontdict=fontdic)
	I11 = ax.scatter(dataX[0], dataY[0], s=35, marker='2', color='r', label='Risk-Averse')
	I12 = ax.scatter(dataX[1], dataY[1], s=15, marker='d', color='b', label='Conventional method')
	I13 = ax.plot(dataX[2], dataY[2], ls='--', color='grey', label='Target')
	ax.legend(loc='upper right',prop={'family':'Times New Roman', 'size':10})
	pass

def figUpdata_2(ax, dataX, dataY, color, xlim, ylim):
	pass

def figUpdata_3(ax, dataX, dataY, color, xlim, ylim):
	pass

def figUpdata_4(ax, dataX, dataY, color, xlim, ylim):
	pass