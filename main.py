#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import numpy as np
from random import random
import numpy.random as rand
#subprocess works only for python3!

def stellar_evol():
	""" Counting the SSE code Hurley et al.(2000) and forming an output table"""
	starNumb = 10000
	data, starsMasses = [], []
	minMass, maxMass = 10.0, 50.0
	beta = 2.3
	q=2000000000
	taumax = q/(minMass**beta)
	for count in range(starNumb):	#creating array of masses
		rnd = random()
		sM=(((1.0-rnd)/(minMass**(beta-1.0))) + (rnd/(maxMass**(beta-1.0))))**((-1.0)/(beta-1.0))
		starsMasses.append(sM)
	time_dist = np.random.uniform(0, 3*taumax, len(starsMasses))	#creating array of times

	#order = 0  #just for check the starNumb during process
	for i in range(starNumb):
		#order = order + 1
		#print(order)
		M = round(starsMasses[i])
		T = time_dist[i]/1000000
		Z = 0.02
		input_f = open('evolve.in', 'w')	
		input_f.write('%1.2f %1.2f %1.2f \n%1.1f %1.1f %1.1f %1.0f \n%1.0f %1.0f %1.0f %1.0f %1.1f %1.0f \n%1.2f %1.2f %1.2f' #сreatig 'evolve.in' for SSE
			%(M,Z,T,0.5,0.0,1.0,190.0,0,1,0,1,3.0,999,0.05,0.01,0.02))

		#Running the makefile
		#WARNING! Works only in the directory where main.py+sse.h+makefile is located
		subprocess.run(["make", "sse", "-q"])
		subprocess.run(["./sse", "-q"])

		with open('evolve.dat', 'rb') as f:
			m = str(f.readlines()[-1].decode()) #read the last string
			k = m.split()
			if k[1] == '1.0000':	#add MS stars (evol_stat = 1)
				data.append(m)

	#Save an array to a binary file in NumPy (.npy) format. Use np.load('output.npy') to open it
	np.save('output',data)
	print(np.load('output.npy'))

if __name__ == '__main__':
	stellar_evol()