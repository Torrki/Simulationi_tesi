import numpy as np #type: ignore

class ArtificialCat:
	def __init__(self, R0, V0):
		if(type(R0) is np.ndarray and type(V0) is np.ndarray):
			self.Posizione=R0.copy().reshape((2,1))
			self.Velocita=V0.copy().reshape((2,1))
			self.SMP=list()
			self.PosizioneMigliore=R0.copy().reshape((2,1))
			self.__modalita='seeking'
		else:
			raise ValueError("I parametri devono essere dei vettori 2x1")
		
	@property
	def Modalita(self):
		return self.__modalita
		
	def SetMode(self, m):
		if(m=='seeking' or m=='tracing'):
			self.__modalita=m
		else:
			raise ValueError('La modalità {0} non è ammissibile per gli agenti\n'.format(m))
			
