import numpy as np
import numpy.random as rnd
from ActiveAgent import ActiveAgent

def Vicsek(T: float, density: float, v0: float, N:int, eta: float, beta: float, R0: int): #funzione decoratore per configurare la simulazione
	'''
	Funzione per la configurazione di un modello Vicsek:
	T 					è il periodo di osservazione
	density 		è la densità degli agenti nello spazio
	v0 					è la velocità degli agenti
	N						è il numero di agenti attivi
	eta					è l'intensità del rumore
	beta				è l'intensità della forza di attrazione-repulsione
	
	torna una funzione che permette di eseguire la simulazione
	'''
	ActiveAgent.raggioIntorno=float(R0)
	seme_random=55
	gen=rnd.default_rng(seme_random) #Random Generator
	L=N/(2.0*density) #Raddoppio perchè lo spazio va da -L a L, dunque in lunghezza 2L
	
	posizioniIniziali=gen.uniform(low=-L, high=L, size=(2,N))
	angoliIniziali=gen.uniform(high=2*np.pi, size=N)
	orientamentiIniziali=np.array( [[np.cos(a) for a in angoliIniziali],
																	[np.sin(a) for a in angoliIniziali]] )
																	
	agenti=[ActiveAgent(np.resize( posizioniIniziali[:,k], (2,1) ), np.resize( orientamentiIniziali[:,k], (2,1) )) for k in range(N)] #creazione degli N agenti con gli stati iniziali
	
	def sistema(passi: int):
		'''
		Funzione per la simulazione del modello Vicsek
		passi			è il numero di passi della simulazione
		
		Torna una matrice (N*2)Xpassi in cui la colonna k-esima è lo stato del sistema al passo k-esimo
		'''
		statoVicsek=agenti[0].getPosition() #creo lo stato iniziale del sistema, che comprende solo le posizioni degli agenti
		for i in range(1, N):
			statoVicsek=np.concatenate((statoVicsek, agenti[i].getPosition()))
		snaps=np.copy(statoVicsek)
		
		#simulazione dei passi
		for k in range(passi):
			connettivita=np.zeros((N,N))
			for i in range(N):
				i_stato=i*2
				s_i=agenti[i].getDirection()
				
				s_vicini=np.zeros((2,1)) #vettore medio della direzione dei vicini, compreso anche l'agente i-esimo
				for j in range(N):
					connettivita[j,i]=agenti[i].inBound(agenti[j])
					
					dist_ij=agenti[j].getPosition()-agenti[i].getPosition()
					normaDistanza=np.linalg.norm(dist_ij)
					if(normaDistanza >= 1.0):
						dist_ij=dist_ij/normaDistanza
					
					s_vicini += connettivita[j,i]*agenti[j].getDirection() + connettivita[j,i]*beta*pow( (int(normaDistanza) - (R0-2)), 3)*dist_ij
					
				rumore=gen.standard_normal(size=(2,1))
				rumore_norm = rumore/np.linalg.norm(rumore)
					
				statoVicsek[[i_stato,i_stato+1]] += T*v0*s_i #aggiornamento delle posizioni nello stato
				agenti[i].setPosition(statoVicsek[[i_stato,i_stato+1]])
				
				new_s=s_vicini+eta*rumore_norm
				new_s= new_s/np.linalg.norm(new_s) #aggiornamento dell'orientamento degli agenti
					
				agenti[i].setDirection( new_s )
				
			snaps=np.concatenate((snaps, statoVicsek),axis=1) #aggiungo il nuovo stato nella raccolta
		return snaps
	
	return sistema

