import numpy as np # type: ignore
import numpy.random as rnd # type: ignore
from ActiveAgent import ActiveAgent

def Vicsek(T: float, densita: float, v0: float, N:int, eta: float, beta: float, R0: int, Dattr: int, x0=0, y0=0): #funzione wrapper per configurare la simulazione
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
	def sistema(passi: int):
		'''
		Funzione per la simulazione del modello Vicsek
		passi			è il numero di passi della simulazione
		'''	
		#Stato iniziale del sistema, con posizione e velocità del CM
		agenti=list(sistema.agenti)
		N=len(agenti)
		
		statoVicsek=np.zeros((N*2,1))
		velocitaCM=np.zeros((2,1))
		CM=np.zeros((2,1))
		R=10
		
		#Calcolo CM
		for i in range(N):
			CM += agenti[i].Posizione/N
			
		PCollisione=CM.copy()
		
		#Calcolo velocità CM e orientamento degli agenti verso CM
		for i in range(N):
			dist_iCM = PCollisione-agenti[i].Posizione
			normaDistCM = np.linalg.norm(dist_iCM)			
			if(normaDistCM >= 1e-2):
				dist_iCM /= normaDistCM
				
			agenti[i].Orientamento = dist_iCM
			velocitaCM += agenti[i].Orientamento * (agenti[i].Velocita/N)
		
		yield velocitaCM.copy(), CM.copy(), 0
		
		#simulazione dei passi
		for k in range(1,passi+1):
			velocitaCM[0][0]=0
			velocitaCM[1][0]=0
			CM[0][0]=0
			CM[1][0]=0
			
			for i in range(N):
				#Aggiornamento stato
				i_stato=i*2
				s_i=agenti[i].Orientamento
				
				dP=T*agenti[i].Velocita*s_i
				agenti[i].Posizione += dP
				
				#Calcolo vettore orientamento dei vicini e vettore della forza repulsiva
				s_vicini=np.zeros((2,1))
				forzaAttrazioneAgenti=np.zeros((2,1))
				for j in range(N):
					if( agenti[i].inBound(agenti[j]) ):
						dist_ij=agenti[j].Posizione-agenti[i].Posizione		#Quando i==j è un vettore nullo, la forza è automaticamente annullata e viene inserito solo l'orientamento dell'agente stesso
						normaDistanza=np.linalg.norm(dist_ij)
						
						if(normaDistanza >= 1):
							dist_ij /= normaDistanza
						
						forzaAttrazione_ij = beta*(int(normaDistanza) - Dattr)*dist_ij
						forzaAttrazioneAgenti += forzaAttrazione_ij
						s_vicini += agenti[j].Orientamento
						
				dist_ijCM=PCollisione - agenti[i].Posizione
				moduloDistanzaCM = np.linalg.norm(dist_ijCM)
				if(moduloDistanzaCM >= 1):
					dist_ijCM /= moduloDistanzaCM
					
				#Rotazione forza CM
				angolo=( -1 / ( np.power(moduloDistanzaCM - R,2) + 1 ) )*np.pi/2
				dist_ijCM_Rot = np.array([[np.cos(angolo), -np.sin(angolo)],[np.sin(angolo), np.cos(angolo)]], dtype=np.dtype(float)) @ dist_ijCM
					
				forzaCM=1/( np.power(moduloDistanzaCM-R, 2) + 1)
				
				rumore_x=gen.standard_normal(size=(1,1))
				rumore_y=gen.standard_normal(size=(1,1))
				rumore=np.array([ [rumore_x[0][0]], [rumore_y[0][0]] ], dtype=np.dtype(float))
				rumore /= np.linalg.norm(rumore)
				
				versoreforzaCM = dist_ijCM+dist_ijCM_Rot
				normaVersoreforzaCM = np.linalg.norm(versoreforzaCM)
				if(normaVersoreforzaCM >= 1):
					versoreforzaCM /= normaVersoreforzaCM
				
				new_s=s_vicini+ eta*rumore + forzaAttrazioneAgenti + 2*forzaCM*versoreforzaCM
				normaNew_s=np.linalg.norm(new_s)
				if(normaNew_s >= 1):
					new_s /= normaNew_s
				agenti[i].Orientamento=new_s
				
				#Calcolo vettore velocità del CM
				velocitaCM += agenti[i].Orientamento * (agenti[i].Velocita/N)
				CM += agenti[i].Posizione / N
				
			del PCollisione
			PCollisione=CM.copy()
				
			yield velocitaCM.copy(), CM.copy(), k
			
	ActiveAgent.raggioIntorno=float(R0)
	sistema.seme_random=10
	gen=rnd.default_rng(sistema.seme_random) #Random Generator
	L=N/(2.0*densita) #Raddoppio perchè lo spazio va da -L a L, dunque in lunghezza 2L
	
	posizioniInizialiX=gen.uniform(low=-L+x0, high=L+x0, size=(N,1))
	posizioniInizialiY=gen.uniform(low=-L+y0, high=L+y0, size=(N,1))
	posizioniIniziali = np.concatenate((posizioniInizialiX, posizioniInizialiY), axis=1)
	angoliIniziali=gen.uniform(high=2*np.pi, size=(1,N))
	orientamentiIniziali=np.array( [ np.cos(angoliIniziali[0]),np.sin(angoliIniziali[0]) ], dtype=np.dtype(float) ).T
																	
	sistema.agenti= { ActiveAgent(posizioniIniziali[k], orientamentiIniziali[k], v0 ) for k in range(N)} #creazione degli N agenti con gli stati iniziali
	
	del posizioniIniziali, angoliIniziali, orientamentiIniziali
	return sistema
	
def UnionVicsek(vic_1, vic_2):
	vic_1.agenti |= vic_2.agenti
	del vic_2
	
Vicsek.UnionVicsek=UnionVicsek

