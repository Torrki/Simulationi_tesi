import ArtificialAnt as AA
from Grafo import *

def ACO(n_agenti: int, T: float, freqSpawn: int, V: float, tau0: float, rho: float, Q: float, Grafo: Grafo, alpha: float =1, beta:float =1, euristic =lambda a,n: 1.0):
	'''
	Funzione per la configurazione di un modello ACO:
	T_sim 				è il periodo di osservazione
	freqSpawn			ogni quanti passi attivare le nuove formiche
	V					è la velocità degli agenti
	n_agenti			è il numero di agenti attivi
	tau0				è la condizione iniziale dei ferormoni
	Q					ferormoni rilasciati dalle formiche
	Grafo				grafo che rappresenta la mappa delle formiche
	alpha				peso dello stato corrente nel calcolo della probabilità
	beta				peso della funzione euristica nel calcolo della probabilità
	euristic			funzione euristica nella forma f(Arco, NodoCibo) -> float

	Torna una funzione generatore
	'''
	def sistema(passi : int):
		'''
		Funzione per la simulazione del modello ACO
		passi			è il numero di passi della simulazione
		'''
		FormicheAttive=list()
		statoACO=np.zeros((n_agenti*2,1))
		listaStatiFerormoni=list()

		for n in Grafo.Nodi:
			listaArchiNodo=list(n.Archi)
			listaArchi = [a for a in listaArchiNodo if a.Nodi[0] is n]
			if(len(listaArchi) > 1):
				listaStatiFerormoni += listaArchi

		statoFerormoni=np.zeros((len(listaStatiFerormoni), 1))

		CostiFormiche=dict()
		for j in range(n_agenti):
			statoACO[[j*2, (j*2)+1]]=Nido.Posizione
			
		for a in Grafo.Arcs:
			if a in listaStatiFerormoni:
				i=listaStatiFerormoni.index(a)
				statoFerormoni[i][0]=a.Ferormoni

		yield statoACO.copy(), statoFerormoni.copy(), 0
		
		for p in range(1,passi+1):
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
					if(lastArc.Nodi[0].InBound(f.Posizione)):
						
						lastArc.RilascioFormiche += Q/CostiFormiche[f]
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
						
				dP=T*V*f.Direzione
				f.Posizione += dP
				statoACO[[i*2, i*2+1]] += dP
				
			Grafo.Update()
			
			for a in range(len(listaStatiFerormoni)):
				statoFerormoni[a][0]=listaStatiFerormoni[a].Ferormoni
				
			yield statoACO.copy(), statoFerormoni.copy(), p
			
	Nido=Grafo.Nido
	NodoCibo=Grafo.NodoCibo

	Formiche={AA.ArtificialAnt(Nido) for f in range(n_agenti)}

	for a in Grafo.Arcs:
		a.TassoEvaporazione=rho
		a.Ferormoni=tau0
		a.RilascioFormiche=0
		a.Alpha=alpha
		a.Beta=beta
		a.Euristica=euristic(a, NodoCibo)

		lunghezzaTratto = np.linalg.norm( a.Nodi[1].Posizione-a.Nodi[0].Posizione )
		#Usare come costo il tempo impiegato
		#a.Costo=lunghezzaTratto/V
		#Usare come costo la distanza 
		a.Costo=lunghezzaTratto
		
	return sistema
		
