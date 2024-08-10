import ArtificialAnt as AA
from Grafo import *

def ACO(n_agenti: int, n_snaps: int, T: float, freqSpawn: int, V: float, rho: float, tau0: float, Q: float, Grafo: Grafo):
	AA.ArtificialAnt.Q=Q
	AA.ArtificialAnt.V=V
	Nido=Grafo.Nido
	NodoCibo=Grafo.NodoCibo

	Formiche={AA.ArtificialAnt(Nido) for f in range(n_agenti)}

	def sistema(passi : int):
		FormicheAttive=list()
		statoACO=np.zeros((n_agenti*2,1))
		for j in range(n_agenti):
			statoACO[[j*2, (j*2)+1]]=np.copy(Nido.posizione)
		snaps=np.copy(statoACO)
		
		for p in range(passi):
			if(p % freqSpawn == 0 and len(Formiche) > 0):
				F0=Formiche.pop()
				F0.Attiva=True
				FormicheAttive.append(F0)
				
				arco0=Nido.ChoiceArc()
				F0.AppendArc(arco0)
				direzione0=arco0.Nodi[1].posizione-F0.Posizione
				direzione0=direzione0/np.linalg.norm(direzione0)
				F0.Direzione=direzione0
			
			for i in range(len(FormicheAttive)):
				f=FormicheAttive[i]
				lastArc=f.Percorso[-1]
				if(not f.Cibo):
					if(lastArc.Nodi[1].InBound(f.Posizione)):
						arco=lastArc.Nodi[1].ChoiceArc()
							
						if(arco is not None):
							f.AppendArc(arco)
									
							direzione=arco.Nodi[1].posizione-f.Posizione
							direzione=direzione/np.linalg.norm(direzione)
							f.Direzione=direzione
						elif(lastArc.Nodi[1] is NodoCibo):
							f.Cibo= True
							f.Direzione = -f.Direzione
				else:
					#Rilascio ferormoni
					lastArc.RilascioFormiche += Q/f.CostoPercorso
					if(lastArc.Nodi[0].InBound(f.Posizione)):
						
						f.Percorso.pop()
						if(lastArc.Nodi[0] is not Nido):
							lastArc=f.Percorso[-1]
							direzione=lastArc.Nodi[0].posizione-f.Posizione
							direzione=direzione/np.linalg.norm(direzione)
							f.Direzione=direzione
						else:
							f.Cibo= False
							f.CostoPercorso=0
							
							arco0=Nido.ChoiceArc()
							f.AppendArc(arco0)
							direzione0=arco0.Nodi[1].posizione-f.Posizione
							direzione0=direzione0/np.linalg.norm(direzione0)
							f.Direzione=direzione0
						
				dP=T*(V/lastArc.Costo)*f.Direzione
				f.Posizione += dP
				statoACO[[i*2, (i*2)+1]] += dP
				
			Grafo.Update()
			snaps = np.concatenate((snaps, statoACO), axis=1)
		return snaps
	return sistema
		
