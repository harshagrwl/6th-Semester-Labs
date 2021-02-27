import tkinter as tk
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
import random
import time as tm

class ExpAccurate(tk.Frame):
	# initial parameters
	gameAreaHeight = 300
	stimuliBasePosition = [200, -30]
	stimuliSideLength = 30
	stimuliFontSize = 20
	stimuliKey = ['S', 'L', 'E', 'I', 'R', 'U', 'F', 'J']
	stimuliTotalAmount = 8
	timeStart = []                                  
	timeHit = []                                    
	timeDelta = []                                  
	plotTimeXList = []                              
	clips = 0
	plotTimeXClips = []								
	counterMax = 10                                 
	# counterMax = 1
	timerValidHit = 5
	flagPause = False
	flagTransit = False
	flagStart = False
	coefficient_determination = 0.0

	def __init__(self, parent=None):
		tk.Frame.__init__(self, parent)
		self.pack()
		self.makeWidgets()
		self.defStimuliCollection()
		self.stimuliAmount = 2						
		self.counter = 0							
		self.flagStart = False
		self.flagPause = False
		self.flagTransit = False

		self.bind_all('<space>', self.start)		

	def makeWidgets(self):
		self.frameExplain = tk.Frame(self)
		self.frameGameArea = tk.Canvas(self, bd=2, bg='white', relief=tk.GROOVE, width=500, height=self.gameAreaHeight)
		self.frameControlPanel = tk.Frame(self)

		self.frameExplain.grid(row=0, column=0, padx=10, pady=10)
		self.frameGameArea.grid(row=1, column=0, padx=10, pady=10)
		self.frameGameArea.grid_propagate(0)
		self.frameControlPanel.grid(row=0, rowspan=2, column=1, padx=10, pady=10)
		self.labelPause = tk.Label(self.frameExplain, text="Hick Hyman's Simulation by Harsh Agarwal (181IT117). Press Spacebar to start.",font=("Arial", 10))
		# stimuli hints
		self.stimuliHints = [0 for x in range(8)]
		for x in range(8):
			self.stimuliHints[x] = tk.Label(self.frameExplain, text=self.stimuliKey[x], relief=tk.GROOVE, width=5)
		self.labelRequirement = tk.Label(self.frameControlPanel, text="If checked, stimuli are dropping, otherwise they are still", wraplength=200)
		# toggle stimuli dropping animation
		self.varToggle = tk.IntVar()
		self.btnToggleMode = tk.Checkbutton(self.frameControlPanel, text="Stimuli animation", variable=self.varToggle)
		self.btnPreload = tk.Button(self.frameControlPanel, text="Preload Dataset")
		self.btnFilter = tk.Button(self.frameControlPanel, text="Filter Outliers")

		self.labelPause.grid(row=0, column=0, columnspan=8, padx=10, pady=10, sticky=tk.W)
		self.stimuliHints[0].grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[1].grid(row=2, column=7, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[2].grid(row=1, column=1, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[3].grid(row=1, column=6, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[4].grid(row=1, column=2, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[5].grid(row=1, column=5, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[6].grid(row=2, column=3, sticky=tk.NSEW, padx=10, pady=10)
		self.stimuliHints[7].grid(row=2, column=4, sticky=tk.NSEW, padx=10, pady=10)
		self.labelRequirement.grid(row=0, column=0, padx=10, pady=10)
		self.btnPreload.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)
		self.btnToggleMode.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)
		self.btnFilter.grid(row=3, column=0, sticky=tk.NSEW, padx=10, pady=10)

		self.btnPreload.bind('<ButtonRelease-1>', self.preload)
		self.btnFilter.bind('<ButtonRelease-1>', self.filter)

	def defStimuliCollection(self):
		self.stimuli = [0 for x in range(8)]
		self.stimuliTexts = [0 for x in range(8)]
		for x in range(8):
			self.stimuli[x] = self.frameGameArea.create_rectangle(self.stimuliBasePosition[0], self.stimuliBasePosition[1], self.stimuliBasePosition[0] + self.stimuliSideLength, self.stimuliBasePosition[1] + self.stimuliSideLength, fill='#C0FFF8', activefill='#63B2A9', tags=self.stimuliKey[x], state=tk.HIDDEN)
			self.stimuliTexts[x] = self.frameGameArea.create_text(self.stimuliBasePosition[0] + 0.5*self.stimuliSideLength, self.stimuliBasePosition[1] + 0.5*self.stimuliSideLength, text=self.stimuliKey[x], font=self.stimuliFontSize, tags=self.stimuliKey[x], state=tk.HIDDEN)

	def start(self, event):
		self.flagStart = True
		self.generateStimuliSet(self.stimuliAmount)
		self.bind_all('<KeyPress>', self.onKeyHit)
		self.bind_all('<space>', self.pauseResume)

	def generateStimuliSet(self, argAmount):
		self.plotTimeXClips.append(self.clips)
		self.flagTransit = True
		self.indexList = []				
		for i in range(argAmount):
			self.indexList.append(i)
			self.stimuliHints[i].config(relief=tk.RAISED, bg='#63B2A9', fg='white')
		self.speed = 5
		self.counterTransit = 0
		self.transitStimuliSet()

	def transitStimuliSet(self):
		if self.counterTransit < 4:
			if self.stimuliHints[0].cget('state') == tk.NORMAL:
				for i in range(self.stimuliAmount):
					self.stimuliHints[i].config(state=tk.DISABLED, bg='SystemButtonFace', relief=tk.GROOVE)
			else:
				for i in range(self.stimuliAmount):
					self.stimuliHints[i].config(state=tk.NORMAL, bg='#63B2A9', relief=tk.RAISED)
			self.counterTransit += 1
			self.frameGameArea.after(500, self.transitStimuliSet)
		else:
			self.frameGameArea.after(1500, self.generateRandomStimuli(self.indexList))

	def generateRandomStimuli(self, argIndexList):
		self.indexCurrent = random.sample(argIndexList, 1)
		self.frameGameArea.itemconfigure(self.stimuli[self.indexCurrent[0]], state=tk.NORMAL)
		self.frameGameArea.itemconfigure(self.stimuliTexts[self.indexCurrent[0]], state=tk.NORMAL)
		self.frameGameArea.coords(self.stimuli[self.indexCurrent[0]], self.stimuliBasePosition[0], self.stimuliBasePosition[1], self.stimuliBasePosition[0] + self.stimuliSideLength, self.stimuliBasePosition[1] + self.stimuliSideLength)
		self.frameGameArea.coords(self.stimuliTexts[self.indexCurrent[0]], self.stimuliBasePosition[0] + 0.5*self.stimuliSideLength, self.stimuliBasePosition[1] + 0.5*self.stimuliSideLength)

		self.flagTransit = False
		if self.flagStart == True:
			self.animateStimuli()
			self.flagStart = False
		self.timeStart.append(tm.time())

	def animateStimuli(self):
		if self.flagPause == False:
			if self.flagTransit == False:
				if self.varToggle.get() == 1:
					if self.frameGameArea.coords(self.stimuli[self.indexCurrent[0]])[1] > self.gameAreaHeight + 3:
						del(self.timeStart[-1])

						if self.counter < self.counterMax - 1:
							self.generateRandomStimuli(self.indexList)
							self.counter += 1
						else:
							if self.stimuliAmount < 8:
								self.counter = 0
								self.stimuliAmount += 1
								self.generateStimuliSet(self.stimuliAmount)
							else:
								self.flagPause = True
								win = tk.Toplevel()
								win.wm_title("Message")
								tk.Label(win, text="Experiment is done, please check your results").grid(row=0, column=0, padx=20, pady=10, sticky=tk.NSEW)
								tk.Button(win, text="Okay", command=win.destroy).grid(row=1, column=0, padx=20, pady=10, sticky=tk.NSEW)	
								self.expEnd()
					else:	
						self.frameGameArea.move(self.stimuli[self.indexCurrent[0]], 0, self.speed)
						self.frameGameArea.move(self.stimuliTexts[self.indexCurrent[0]], 0, self.speed)
				# if choose to still stimuli
				else:
					self.frameGameArea.coords(self.stimuli[self.indexCurrent[0]], 250-0.5*self.stimuliSideLength, 
						0.5*(self.gameAreaHeight-self.stimuliSideLength), 250+0.5*self.stimuliSideLength, 0.5*(self.gameAreaHeight+self.stimuliSideLength))
					self.frameGameArea.coords(self.stimuliTexts[self.indexCurrent[0]], 250, 0.5*self.gameAreaHeight)
					if(len(self.timeStart)):
						if(tm.time()-self.timeStart[-1]) > self.timerValidHit:
							self.disappearStimuli()
			self.frameGameArea.after(20, self.animateStimuli)

	def disappearStimuli(self):
		self.frameGameArea.itemconfigure(self.stimuli[self.indexCurrent[-1]], state=tk.HIDDEN, fill='#C0FFF8')
		self.frameGameArea.itemconfigure(self.stimuliTexts[self.indexCurrent[-1]], state=tk.HIDDEN)
		if self.counter < self.counterMax - 1:
			self.generateRandomStimuli(self.indexList)
			self.counter += 1
		else:
			if self.stimuliAmount < 8:
				self.counter = 0
				self.stimuliAmount += 1
				self.generateStimuliSet(self.stimuliAmount)
			else:
				self.flagPause = True
				win = tk.Toplevel()
				win.wm_title("Message")
				tk.Label(win, text="Experiment is done, please restart").grid(row=0, column=0, padx=20, pady=10, sticky=tk.NSEW)
				tk.Button(win, text="Okay", command=win.destroy).grid(row=1, column=0, padx=20, pady=10, sticky=tk.NSEW)	
				self.expEnd()

	def onKeyHit(self, event):
		if self.flagPause == False:
			self.indexHit = []
			if event.char == self.stimuliKey[self.indexCurrent[0]] or event.char == self.stimuliKey[self.indexCurrent[0]].lower():
				self.indexHit.append(self.indexCurrent[0])
				self.timeHit.append(tm.time())
				self.timeDelta.append((self.timeHit[-1] - self.timeStart[-1])*1000)
				self.plotTimeXList.append(self.stimuliAmount)
				self.clips += 1
				self.frameGameArea.itemconfigure(self.stimuli[self.indexCurrent[0]], fill='#63B2A9')
				self.flagPause = True
				self.flagTransit = True
				self.frameGameArea.after(300, self.afterCorrectKeyHit)

	def afterCorrectKeyHit(self):
		self.flagTransit = False
		self.frameGameArea.itemconfigure(self.stimuli[self.indexCurrent[0]], state=tk.HIDDEN, fill='#C0FFF8')
		self.frameGameArea.itemconfigure(self.stimuliTexts[self.indexCurrent[0]], state=tk.HIDDEN)
		self.flagPause = False
		self.frameGameArea.after(1000, self.animateStimuli)
	
		if self.counter < self.counterMax - 1:
			self.generateRandomStimuli(self.indexList)
			self.counter += 1
		
			fig = plt.figure()
			graph = fig.add_subplot(1,1,1)
			graph.set(title="Hick-Hyman Law empirical data fitting", ylabel="Reaction Time (ms)", xlabel="Degree of Choice, n")
			graph.scatter(self.plotTimeXList, self.timeDelta, color='#4A857E', alpha=0.5)
			plt.xticks(range(min(self.plotTimeXList)-1, max(self.plotTimeXList)+2, 1))
			plt.grid()
			display.clear_output(wait=True)
			plt.show()
		else:
		
			if self.stimuliAmount < 8:
				self.counter = 0
				self.stimuliAmount += 1
				self.generateStimuliSet(self.stimuliAmount)
			else:
				self.flagPause = True
				win = tk.Toplevel()
				win.wm_title("Message")
				tk.Label(win, text="Experiment is done, please restart").grid(row=0, column=0, padx=20, pady=10, sticky=tk.NSEW)
				tk.Button(win, text="Okay", command=win.destroy).grid(row=1, column=0, padx=20, pady=10, sticky=tk.NSEW)	
				self.expEnd()

	def pauseResume(self, event):
		if self.flagTransit == False:
			self.flagPause = not self.flagPause
			self.animateStimuli()
			if self.flagPause == True:
				self.labelPause.config(text="Press <SPACE> key to CONTINUE")
			else:
				self.labelPause.config(text="Press <SPACE> key to PAUSE at any time")

	def expEnd(self):
		self.unbind_all('<KeyPress>')
		fig, ax = plt.subplots()
		ax.set(title="Hick-Hyman Law empirical data fitting", ylabel="Reaction Time (ms)", xlabel="Degree of Choice, n")
		plt.scatter(self.plotTimeXList, self.timeDelta, color='#4A857E', alpha=0.5)
		plt.xticks(range(min(self.plotTimeXList)-1, max(self.plotTimeXList)+2, 1))
		plt.grid()	
		plotTimeXLogList = np.log2(self.plotTimeXList)
		z = np.polyfit(plotTimeXLogList, self.timeDelta, 1)
		f = np.poly1d(z)
		plotTimeXArray = np.array(self.plotTimeXList)
		x = np.arange(plotTimeXArray.min()-0.3, plotTimeXArray.max()+0.3, 0.1)
		xLog = np.log2(x)
		y = f(xLog)
		plt.plot(x, y)
		ybar = np.mean(self.timeDelta)
		sstot, ssres = (0 for i in range(2))
		for i in range(len(self.timeDelta)):
			sstot += (self.timeDelta[i] - ybar)**2
			ssres += (f(np.log2(self.plotTimeXList[i])) - self.timeDelta[i])**2
		self.coefficient_determination = 1 - ssres/sstot
		display.clear_output(wait=True)
		plt.show()
		self.btnFilter.config(state=tk.NORMAL)
		print("Data fitting result: %.1f log(DOC) + %.1f\n(DOC: Degree Of Choice)\n" %(z[0],z[1]))
		print("R-squared = %f" %self.coefficient_determination)

	def preload(self, event):
		self.timeDelta = [1315,1350,1340,1400,1320,2100,1350,1340,1400,1320,
						1350,1400,1980,1450,1750,1350,1400,1390,1450,1370,
						1400,1450,1430,1500,1420,1400,1467,1440,1490,1820,
						1450,1500,1920,1550,1470,1450,1500,1480,1540,1470,
						1497,1532,1520,1590,1510,1490,2240,1530,1590,1510,
						1520,1570,1550,1520,1540,1508,1578,1560,1620,1440,
						1543,1570,1570,1590,1560,1540,1590,1573,2800,1610,]
		self.plotTimeXList = []
		for i in range(2,9):
			self.plotTimeXList += [i for j in range(10)]
		self.expEnd()

	def filter(self, event):
		tmpTimeDelta, tmpPlotTimeXList = ([] for i in range(2))
		tmpPlotTimeX_Ref = self.plotTimeXList[0]
		tmpTimeDelta_filtering, tmpPlotTimeX_filtering = ([] for i in range(2))
		for i in range(len(self.timeDelta)):
			if self.plotTimeXList[i] == tmpPlotTimeX_Ref:
				tmpTimeDelta_filtering.append(self.timeDelta[i])
				tmpPlotTimeX_filtering.append(self.plotTimeXList[i])
			else:
				tmpPlotTimeX_Ref = self.plotTimeXList[i]
				threshold = 0.8 * np.std(tmpTimeDelta_filtering)
				for j in range(len(tmpTimeDelta_filtering)):
					if abs(tmpTimeDelta_filtering[j] - np.mean(tmpTimeDelta_filtering)) <= threshold:
						tmpTimeDelta.append(tmpTimeDelta_filtering[j])
						tmpPlotTimeXList.append(tmpPlotTimeX_filtering[j])
				tmpTimeDelta_filtering, tmpPlotTimeX_filtering = ([] for i in range(2))
				tmpTimeDelta_filtering.append(self.timeDelta[i])
				tmpPlotTimeX_filtering.append(self.plotTimeXList[i])
				if i == len(self.timeDelta) - 1:
					threshold = 0.8 * np.std(tmpTimeDelta_filtering)
					for j in range(len(tmpTimeDelta_filtering)):
						if abs(tmpTimeDelta_filtering[j] - np.mean(tmpTimeDelta_filtering)) <= threshold:
							tmpTimeDelta.append(tmpTimeDelta_filtering[j])
							tmpPlotTimeXList.append(tmpPlotTimeX_filtering[j])
		self.timeDelta = tmpTimeDelta
		self.plotTimeXList = tmpPlotTimeXList
		self.expEnd()

if __name__ == "__main__":
	root = tk.Tk()
	root.title("IT351 Assignment - Hick-Hyman's Law Experiment")
	ExpAccurate(root).mainloop()
	root.after(5, lambda: root.focus_force())