import numpy as np # type: ignore
import numpy.random as rnd # type: ignore
from ActiveAgent import ActiveAgent
from utilities import Normalizzazione

def Vicsek(T: float, densita: float, v0: float, N:int, eta: float, beta: float, R0: int, Dattr: int, x0=0, y0=0, trajFuncGen=np.zeros((2,1)), lamb=1): #funzione wrapper per configurare la simulazione
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
	traj		è una funzione generatore che restituisce i passi della traiettoria desiderata
	
	Torna una funzione generatore
	'''
	#Creazione stato iniziale del sistema			
	ActiveAgent.raggioIntorno=float(R0)
	seme_random=10
	gen=rnd.default_rng(seme_random) #Random Generator
	L=N/(2.0*densita) #Raddoppio perchè lo spazio va da -L a L, dunque in lunghezza 2L
	
	posizioniInizialiX=gen.uniform(low=-L+x0, high=L+x0, size=(N,1))
	posizioniInizialiY=gen.uniform(low=-L+y0, high=L+y0, size=(N,1))
	posizioniIniziali = np.concatenate((posizioniInizialiX, posizioniInizialiY), axis=1)
	angoliIniziali=gen.uniform(high=2*np.pi, size=(1,N))
	orientamentiIniziali=np.array( [ np.cos(angoliIniziali[0]),np.sin(angoliIniziali[0]) ], dtype=np.dtype(float) ).T
	
	def sistema(passi: int, repeat: bool):
		'''
		Funzione per la simulazione del modello Vicsek
		passi			è il numero di passi della simulazione
		'''	
		agenti=list(sistema.agenti)
		while(1):
			traj=trajFuncGen(passi, T, v0)
			velocitaCM=np.zeros((2,1))
			CM=np.zeros((2,1))
			for k in range(len(agenti)):
				agenti[k].Posizione=posizioniIniziali[k].copy().reshape((2,1))
				agenti[k].Orientamenti=orientamentiIniziali[k].copy().reshape((2,1))
				velocitaCM += agenti[k].Orientamento * (agenti[k].Velocita/N)
				CM += agenti[k].Posizione/N

			yield velocitaCM.copy(), CM.copy(), 0
			
			#simulazione dei passi
			for k in range(1,passi+1):
				traj_k_pos =next(traj)
				erroreCM = traj_k_pos - CM
				
				velocitaCM[0][0]=0
				velocitaCM[1][0]=0
				CM[0][0]=0
				CM[1][0]=0
				
				for ag in sistema.agenti:
					s_i=ag.Orientamento
					dP=T*ag.Velocita*s_i
					ag.Posizione += dP
					
					#Calcolo della direzione dei vicini e della forza di attrazione
					s_vicini=np.zeros((2,1))
					forzaAttrazioneAgenti=np.zeros((2,1))
					for ag_vicino in sistema.agenti:
						if(ag.inBound(ag_vicino)):
							dist_ij=ag_vicino.Posizione-ag.Posizione #Quando i==j è un vettore nullo, la forza è automaticamente annullata e viene inserito solo l'orientamento dell'agente stesso
							normaDistanza=np.linalg.norm(dist_ij)
							
							#Normalizzazione tramite il calcolo dell'angolo e creazione di un vettore con la stessa direzione a norma unitaria
							Normalizzazione(dist_ij)
							
							forzaAttrazione_ij = beta*(normaDistanza - Dattr)*dist_ij
							forzaAttrazioneAgenti += forzaAttrazione_ij
							s_vicini += ag_vicino.Orientamento
					
					rumore_x=gen.standard_normal(size=(1,1))
					rumore_y=gen.standard_normal(size=(1,1))
					rumore=np.array([ [rumore_x[0][0]], [rumore_y[0][0]] ], dtype=np.dtype(float))
					Normalizzazione(rumore)
					
					#Aggiornamento orientamento agenti
					new_s=s_vicini + eta*rumore + forzaAttrazioneAgenti + lamb*(erroreCM)
					Normalizzazione(new_s)					
					ag.Orientamento=new_s

					#Calcolo vettore velocità del centro di massa
					velocitaCM += ag.Orientamento * (ag.Velocita/N)
					CM += ag.Posizione / N
					
				yield velocitaCM.copy(), CM.copy(), k
				
			if(not repeat):
				break
																	
	sistema.agenti= { ActiveAgent(posizioniIniziali[k], orientamentiIniziali[k], v0 ) for k in range(N)} #creazione degli N agenti con gli stati iniziali
	
	return sistema	

