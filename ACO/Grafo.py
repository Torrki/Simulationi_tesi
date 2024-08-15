import numpy as np # type: ignore
from numpy import random as rnd # type: ignore

lowerBound=1e-6	#per evitare che il valore dei ferormoni vada a 0, creerebbe underflow del valore e una divisione per 0 nel calcolo della probabilità

class ArcoGrafo:
	def __init__(self, tau_0, rho, N1, N2, c):
		self.Ferormoni=tau_0
		self.TassoEvaporazione=rho
		self.RilascioFormiche=0
		self.Nodi=(N1, N2)	#L'arco va da N1 a N2
		self.Costo=c
		N1.LinkArco(self)
		N2.LinkArco(self)
		
	def Update(self):
		U=lowerBound if self.RilascioFormiche == 0 else self.RilascioFormiche
		tmp=(1-self.TassoEvaporazione)*self.Ferormoni + U
		self.Ferormoni=tmp
		self.RilascioFormiche=0
		
	@property
	def Probabilita(self):
		archiNodo=[a for a in self.Nodi[0].Archi if a.Nodi[0] is self.Nodi[0]]
		somma=0
		for a in archiNodo:
			somma = somma + a.Ferormoni
			
		return self.Ferormoni/somma
		
class NodoGrafo:
	def __init__(self, x, y):
		self.Posizione=np.array([[x],[y]], dtype=np.dtype(float))
		self.Archi=set()
	
	def LinkArco(self, arco):
		self.Archi=self.Archi.union({arco})
		
	def ChoiceArc(self):
		#Conversione in lista per avere un ordine nell'iteratore
		listaArchi=list([a for a in self.Archi if a.Nodi[0] is self])
		if( len(listaArchi) > 0 ):
			arrayArchi=np.array(listaArchi, dtype=np.dtype(ArcoGrafo))
			arrayProbs=np.array([a.Probabilita for a in listaArchi], dtype=np.dtype(float))
			return rnd.choice(arrayArchi, p=arrayProbs)
			
	def InBound(self, pos):
		distanza=pos-self.Posizione
		return np.linalg.norm(distanza) < 2e-1
			
class Grafo:
	def __init__(self, tau_0, rho, nodi, Ni, Nc):
		self.Nodi=nodi
		self.Nido=Ni
		self.NodoCibo=Nc
		self.Tau0=tau_0
		self.Rho=rho
	
	@property
	def Arcs(self):
		archi=set()
		
		for n in self.Nodi:
			for a in n.Archi:
				if a not in archi:
					archi=archi.union({a})
		return archi
			
			
	def LinkNodes(self, Ns, Ne, costo):
		if Ns in self.Nodi and Ne in self.Nodi:
			ArcoGrafo(self.Tau0, self.Rho, Ns, Ne, costo)
			
	def Update(self):	
		archiAggiornati=set()
		
		for n in self.Nodi:
			for a in n.Archi:
				if a not in archiAggiornati:
					a.Update()
					archiAggiornati |= {a}

