import numpy as np

class ArtificialAnt:	
	def __init__(self, startNode):
		self.Percorso=list()
		self.Posizione=startNode.Posizione.copy()
		self.Direzione=np.empty((2,1))
		self.Cibo=False
		self.Attiva=False
		
