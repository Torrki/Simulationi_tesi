import numpy as np

class ArtificialAnt:	
	def __init__(self, startNode):
		self.Percorso=list()
		self.Posizione=np.copy(startNode.posizione)
		self.Direzione=np.empty((2,1))
		self.Cibo=False
		self.Attiva=False
		self.CostoPercorso=0
		
	def AppendArc(self, arc):
		self.Percorso.append(arc)
		self.CostoPercorso += arc.Costo
		
