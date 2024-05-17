import numpy as np

class ActiveAgent:
	'''
	Classe per rappresentare gli agenti attivi del modello Vicsek
	r 		è la posizione, un vettore colonna 2x1
	s 		è l'orientamento, un vettore colonna 2x1
	lo stato è descritto dall'unione dei due vettori
	 _____
	|     |
	|  r  |
	|_____|
	|     |
	|  s  |
	|_____|
	'''
	#raggioIntorno=5
	def __init__(self, r0, s0):
		self.stato=np.concatenate((r0,s0), dtype=np.dtype(float))
	
	def getPosition(self):
		return self.stato[[0,1]]
		
	def getDirection(self):
		return self.stato[[2,3]]
		
	def setPosition(self, r):
		self.stato[[0,1]]=r
		
	def setDirection(self, s):
		self.stato[[2,3]]=s
		
	def inBound(self, a):
		diff_vect=self.stato[[0,1]]-a.stato[[0,1]]
		return np.linalg.norm(diff_vect) < ActiveAgent.raggioIntorno
