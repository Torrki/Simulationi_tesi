import numpy as np # type: ignore

class ArtificialBird:
	'''
	Classe che rappresenta un uccello artificiale con un suo stato definito da posizione e velocità
	è anche il nodo nel grafo della connettività dello sciame
	'''
		
	def __init__(self, p0, v0):
		self.Posizione=p0.copy().reshape((2,1))
		self.Velocita=v0.copy().reshape((2,1))
		self.Vicini=set()
		self.PosizioneMigliore=( p0.copy().reshape((2,1)), -np.inf )
		self.PosizioneMiglioreGlobale=np.zeros((2,1))
		
