from ArtificialBird import ArtificialBird as AB
import numpy as np # type: ignore
from numpy import random as rnd # type: ignore

def PSO(n_agenti, densita, velocitaMax, T_sim, c1, c2, betaAttrazione, fEval, D_attr):
	'''
	Funzione per la configurazione di un modello PSO:
	T_sim 				è il periodo di osservazione
	densita 			è la densità degli agenti nello spazio
	velocitaMax 		è la velocità massima degli agenti
	n_agenti			è il numero di agenti attivi
	c1					è l'intensità dell'apprendimento individuale
	c2					è l'intensità dell'apprendimento sociale
	betaAttrazione		è l'intensità della forza di attrazione-repulsione
	fEval				è la funzione di valutazione nello spazio, deve essere f(x,y) -> float
	Dattr				è la distanza minima tra gli agenti nella forza di attrazione
	
	Torna una funzione generatore
	'''
	seme_random=120
	pScelto=1/2
	velocitaMedia=1
	deviazioneStd=0.01
	gen=rnd.default_rng(seme_random) #Random Generator
	L=n_agenti/(2.0*densita) #Raddoppio perchè lo spazio va da -L a L, dunque in lunghezza 2L
	AB.EvalFunction=fEval
	
	posizioniIniziali=gen.uniform(low=-L, high=L, size=(n_agenti,2))
	angoliIniziali=gen.uniform(high=2*np.pi, size=(1,n_agenti))
	orientamentiIniziali=np.array( [np.cos(angoliIniziali[0]),np.sin(angoliIniziali[0])] )

	moduliVelocitaIniziali=gen.normal(loc=velocitaMedia, scale=deviazioneStd, size=(1,n_agenti))
	moduliVelocitaIniziali = np.concatenate((moduliVelocitaIniziali, moduliVelocitaIniziali))
	velocitaIniziali=(moduliVelocitaIniziali*orientamentiIniziali).T

	Uccelli=[AB(posizioniIniziali[i], velocitaIniziali[i]) for i in range(n_agenti)]
	
	#del posizioniIniziali, angoliIniziali, orientamentiIniziali, moduliVelocitaIniziali, velocitaIniziali

	#Definizione topologia
	DizionarioVicini = dict()
	for u in Uccelli:
		I=set(Uccelli)-{u}	
		DizionarioVicini[u]=set(Uccelli)-{u}
		
		for uv in I:
			if len(DizionarioVicini[u]) == 1:
				break
				
			scelta=gen.choice([True, False], p=[1-pScelto, pScelto])
			if(scelta):
				DizionarioVicini[u] -= {uv}

		u.Vicini = DizionarioVicini[u]

	InsiemeValutazioni={(u,AB.EvalFunction(u.Posizione[0][0], u.Posizione[1][0])) for u in Uccelli}
	valutazioneMax=max(InsiemeValutazioni, key=lambda coppia: coppia[1])[1]
	InsiemeMigliori={coppia[0] for coppia in InsiemeValutazioni if coppia[1]==valutazioneMax}
	AgenteMigliore=InsiemeMigliori.pop()

	def sistema(n_snaps):
		'''
		Funzione per la simulazione del modello PSO
		passi		è il numero di passi della simulazione
		'''
		#Definizione valori autovalori nel tempo
		def Autovalore(a_min, a_max):
			t=0
			while(t <= n_snaps):
				yield a_max - (a_max-a_min)*(t/n_snaps)
				t += 1
		
		GenAutovalori=Autovalore(1,1.5)
		statoPSO=np.zeros((n_agenti*2,1))
		for u in range(len(Uccelli)):
			statoPSO[[u*2,u*2+1]]=Uccelli[u].Posizione
			
			del Uccelli[u].PosizioneMiglioreGlobale
			Uccelli[u].PosizioneMiglioreGlobale=AgenteMigliore.Posizione.copy()

		yield statoPSO.copy()

		for p in range(1, n_snaps+1):
			autovaloreP=next(GenAutovalori)		
			for u in range(n_agenti):
				Ucc=Uccelli[u]
				
				fAttrazione=np.zeros((2,1))
				for uv in Ucc.Vicini:
					distanza = uv.Posizione-Ucc.Posizione
					normaDistanza=np.linalg.norm(distanza)
					if(normaDistanza > 1):
						distanza /= normaDistanza
						
					fAttrazione += (normaDistanza - D_attr)*distanza
				
				vel_succ = autovaloreP*Ucc.Velocita + c1*(Ucc.PosizioneMigliore[0]-Ucc.Posizione) + c2*(Ucc.PosizioneMiglioreGlobale-Ucc.Posizione) + betaAttrazione*fAttrazione
				normaVelocita=np.linalg.norm(vel_succ)
				
				if normaVelocita > velocitaMax:
					c=normaVelocita/velocitaMax
					vel_succ /= c
				
				Ucc.Velocita=vel_succ
				Ucc.Posizione += T_sim*Ucc.Velocita
				valutazioneP=AB.EvalFunction(Ucc.Posizione[0][0], Ucc.Posizione[1][0])

				if valutazioneP > Ucc.PosizioneMigliore[1]:
					Ucc.PosizioneMigliore=(Ucc.Posizione.copy(), valutazioneP)
					
				statoPSO[[u*2,(u*2)+1]]=Ucc.Posizione
			
			for u1 in Uccelli:
				UccMigliore=max(u1.Vicini, key=lambda uv: uv.PosizioneMigliore[1])
				if u1.PosizioneMigliore[1] > UccMigliore.PosizioneMigliore[1]:
					UccMigliore=u1
				
				del u1.PosizioneMiglioreGlobale
				u1.PosizioneMiglioreGlobale=UccMigliore.Posizione.copy()
				
			yield statoPSO.copy()
	return sistema

