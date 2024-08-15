import numpy as np # type: ignore

class ActiveAgent:
	'''
	Classe per rappresentare gli agenti attivi del modello Vicsek
	lo stato è descritto dall'unione dei due vettori
	'''
	raggioIntorno=0
	def __init__(self, R0, S0):
		self.Posizione=R0.copy().reshape((2,1))
		self.Orientamento=S0.copy().reshape((2,1))
		
	def inBound(self, Agente):
		diff_vect=Agente.Posizione-self.Posizione
		return np.linalg.norm(diff_vect) <= ActiveAgent.raggioIntorno
