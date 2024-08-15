import numpy as np # type: ignore
import numpy.random as rnd # type: ignore
from ActiveAgent import ActiveAgent

def Vicsek(T: float, densita: float, v0: float, N:int, eta: float, beta: float, R0: int, Dattr: int): #funzione wrapper per configurare la simulazione
	'''
	Funzione per la configurazione di un modello Vicsek:
	T 			è il periodo di osservazione
	densita 	è la densità degli agenti nello spazio
	v0 			è la velocità degli agenti
	N			è il numero di agenti attivi
	eta			è l'intensità del rumore
	beta		è l'intensità della forza di attrazione-repulsione
	R0			è il raggio che definisce l'intorno degli agenti
	Dattr		è la distanza minima tra gli agenti nella forza di attrazione
	
	Torna una funzione generatore
	'''
	ActiveAgent.raggioIntorno=float(R0)
	seme_random=55
	gen=rnd.default_rng(seme_random) #Random Generator
	L=N/(2.0*densita) #Raddoppio perchè lo spazio va da -L a L, dunque in lunghezza 2L
	
	posizioniIniziali=gen.uniform(low=-L, high=L, size=(N,2))
	angoliIniziali=gen.uniform(high=2*np.pi, size=(1,N))
	orientamentiIniziali=np.array( [ np.cos(angoliIniziali[0]),np.sin(angoliIniziali[0]) ], dtype=np.dtype(float) ).T
																	
	agenti= [ ActiveAgent(posizioniIniziali[k], orientamentiIniziali[k] ) for k in range(N)] #creazione degli N agenti con gli stati iniziali
	
	del posizioniIniziali, angoliIniziali, orientamentiIniziali

	def sistema(passi: int):
		'''
		Funzione per la simulazione del modello Vicsek
		passi			è il numero di passi della simulazione
		'''
		statoVicsek=np.zeros((N*2,1))	#creo lo stato iniziale del sistema, che comprende solo le posizioni degli agenti
		velocitaCM=np.zeros((2,1))
		CM=np.zeros((2,1))
		for i in range(N):
			statoVicsek[[i*2,i*2+1]]=agenti[i].Posizione
			velocitaCM += agenti[i].Orientamento * (v0/N)
			CM += agenti[i].Posizione/N
			
		yield statoVicsek.copy(), velocitaCM.copy(), CM.copy(), 0
		
		#simulazione dei passi
		for k in range(1,passi+1):
			velocitaCM[0][0]=0
			velocitaCM[1][0]=0
			CM[0][0]=0
			CM[1][0]=0
			for i in range(N):
				i_stato=i*2
				s_i=agenti[i].Orientamento
				
				s_vicini=np.zeros((2,1)) #vettore medio della direzione dei vicini, compreso anche l'agente i-esimo
				for j in range(N):
					vicino=agenti[i].inBound(agenti[j])
					if(vicino):
						dist_ij=agenti[j].Posizione-agenti[i].Posizione
						normaDistanza=np.linalg.norm(dist_ij)
						if(normaDistanza >= 1.0):
							dist_ij /= normaDistanza
						
						s_vicini += agenti[j].Orientamento + beta*np.power( (int(normaDistanza) - Dattr), 3)*dist_ij
					
				rumore=gen.standard_normal(size=(2,1))
				rumore /= np.linalg.norm(rumore)
					
				dP=T*v0*s_i
				agenti[i].Posizione += dP								#aggiornamento delle posizioni nello stato
				statoVicsek[[i_stato,i_stato+1]]+=dP
				
				new_s=s_vicini+eta*rumore
				new_s /= np.linalg.norm(new_s)
				agenti[i].Orientamento=new_s	#aggiornamento dell'orientamento degli agenti
				
				#Calcolo vettore velocità del centro di massa
				velocitaCM += agenti[i].Orientamento * (v0/N)
				CM += agenti[i].Posizione / N
				
			yield statoVicsek.copy(), velocitaCM.copy(), CM.copy(), k
	
	return sistema

