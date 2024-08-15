import ArtificialAnt as AA
from Grafo import *

def ACO(n_agenti: int, T: float, freqSpawn: int, V: float, tau0: float, Q: float, Grafo: Grafo):
	'''
	Funzione per la configurazione di un modello ACO:
	T_sim 				è il periodo di osservazione
	freqSpawn			ogni quanti passi attivare le nuove formiche
	V					è la velocità degli agenti
	n_agenti			è il numero di agenti attivi
	tau0				è la condizione iniziale dei ferormoni
	Q					ferormoni rilasciati dalle formiche
	Grafo				grafo che rappresenta la mappa delle formiche
	
	Torna una funzione generatore
	'''
	Nido=Grafo.Nido
	NodoCibo=Grafo.NodoCibo

	Formiche={AA.ArtificialAnt(Nido) for f in range(n_agenti)}

	def sistema(passi : int):
		'''
		Funzione per la simulazione del modello ACO
		passi			è il numero di passi della simulazione
		'''
		FormicheAttive=list()
		statoACO=np.zeros((n_agenti*2,1))
		archiGrafo=list(Grafo.Arcs)
		statoFerormoni=np.zeros((len(archiGrafo), 1))
		CostiFormiche=dict()
		for j in range(n_agenti):
			statoACO[[j*2, (j*2)+1]]=Nido.Posizione
			
		for a in range(len(archiGrafo)):
			statoFerormoni[a]=tau0
		
		for p in range(passi):
			if(p % freqSpawn == 0 and len(Formiche) > 0):
				F0=Formiche.pop()
				F0.Attiva=True
				FormicheAttive.append(F0)
				
				arco0=Nido.ChoiceArc()
				F0.Percorso.append(arco0)
				direzione0=arco0.Nodi[1].Posizione-F0.Posizione
				direzione0 /= np.linalg.norm(direzione0)
				F0.Direzione=direzione0
				CostiFormiche[F0]=arco0.Costo
			
			for i in range(len(FormicheAttive)):
				f=FormicheAttive[i]
				lastArc=f.Percorso[-1]
				if(not f.Cibo):
					if(lastArc.Nodi[1].InBound(f.Posizione)):
						arco=lastArc.Nodi[1].ChoiceArc()
							
						if(arco is not None):
							f.Percorso.append(arco)
							CostiFormiche[f] += arco.Costo
									
							direzione=arco.Nodi[1].Posizione-f.Posizione
							direzione /= np.linalg.norm(direzione)
							f.Direzione=direzione
						elif(lastArc.Nodi[1] is NodoCibo):
							f.Cibo= True
							f.Direzione = -f.Direzione
				else:
					#Rilascio ferormoni
					lastArc.RilascioFormiche += Q/CostiFormiche[f]
					if(lastArc.Nodi[0].InBound(f.Posizione)):
						
						f.Percorso.pop()
						if(lastArc.Nodi[0] is not Nido):
							lastArc=f.Percorso[-1]
							direzione=lastArc.Nodi[0].Posizione-f.Posizione
							direzione /= np.linalg.norm(direzione)
							f.Direzione=direzione
						else:
							f.Cibo= False
							
							arco0=Nido.ChoiceArc()
							f.Percorso.append(arco0)
							direzione0=arco0.Nodi[1].Posizione-f.Posizione
							direzione0 /= np.linalg.norm(direzione0)
							f.Direzione=direzione0
							CostiFormiche[f]=arco0.Costo
						
				dP=T*(V/lastArc.Costo)*f.Direzione
				f.Posizione += dP
				statoACO[[i*2, i*2+1]] += dP
				
			Grafo.Update()
			
			for a in range(len(archiGrafo)):
				statoFerormoni[a]=archiGrafo[a].Ferormoni
				
			yield (statoACO.copy(), statoFerormoni.copy(), p)
	return sistema
		
