import numpy as np

class ArtificialAnt:	
	def __init__(self, startNode):
		self.Percorso=list()
		self.Posizione=np.copy(startNode.Posizione)
		self.Direzione=np.empty((2,1))
		self.Cibo=False
		self.Attiva=False
		
