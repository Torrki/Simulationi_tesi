import numpy as np
from numpy import random as rnd

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
		tmp=(1-self.TassoEvaporazione)*self.Ferormoni + self.RilascioFormiche
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
		self.posizione=np.array([[x],[y]], dtype=np.dtype(float))
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
		distanza=pos-self.posizione
		return np.linalg.norm(distanza) < 2e-1
			
class Grafo:
	def __init__(self, tau_0, rho, nodi):
		self.Nodi=nodi
		self.Tau0=tau_0
		self.Rho=rho
			
	def LinkNodes(self, Ns, Ne, costo):
		if Ns in self.Nodi and Ne in self.Nodi:
			nuovoArco=ArcoGrafo(self.Tau0, self.Rho, Ns, Ne, costo)
			
	def Update(self):	
		archiAggiornati=set()
		
		for n in self.Nodi:
			for a in n.Archi:
				if a not in archiAggiornati:
					a.Update()
					archiAggiornati=archiAggiornati.union({a})
			
		
