import numpy as np
import numpy.random as rnd
from Artificial_Cat import ArtificialCat

def CSO(n_agenti, T_sim, v0, v_max, densita, SRD, CDC, SPC, SMP, c, f_eval):

	seme_rnd=100
	rnd_gen=rnd.default_rng(seme_rnd)
	L= n_agenti/(2*densita)
	posizioniIniziali=rnd_gen.uniform(low=-L, high=L, size=(n_agenti, 2))
	velocitaIniziali=rnd_gen.normal(loc=v0, size=(n_agenti,1))
	angoliIniziali=rnd_gen.uniform(low=0, high=2*np.pi, size=n_agenti)
	velocitaVettoriIniziali=velocitaIniziali * np.array([np.cos(angoliIniziali), np.sin(angoliIniziali)]).T
	
	agenti={ArtificialCat(p,v) for p,v in zip(posizioniIniziali, velocitaVettoriIniziali)}
	CDC_vec= np.array([[1],[1]]) if CDC==2 else np.array([[1],[0]])
	
	def sistema(n_snaps):
		
		yield 0
		
		for k in range(0,n_snaps):
			#Scelta randomica della modalità degli agenti
			pSeeking=1/3
			scelteModalita=rnd_gen.choice(['seeking', 'tracing'], size=n_agenti, p=[pSeeking, 1-pSeeking]).tolist()
						
			for a in agenti:
				a.SetMode(scelteModalita[0])
				del scelteModalita[0]
				
				if(a.Modalita == 'seeking'):
					#creazione delle copia per SMP
					for i in range(SMP):
						posCopy=a.Posizione.copy()
						CDC_vecPerm=rnd_gen.permutation(CDC_vec)
						SRD_values=rnd_gen.normal(loc=SRD, scale=1e-2, size=(2,1))
						segni=rnd_gen.choice([1,-1], size=(2,1), p=[1/2, 1/2])
						
						posCopy[0][0] += segni[0][0]*CDC_vecPerm[0][0]*SRD_values[0][0]*posCopy[0][0]
						posCopy[1][0] += segni[1][0]*CDC_vecPerm[1][0]*SRD_values[1][0]*posCopy[1][0]
						
						fitnessValue=f_eval(posCopy[0][0], posCopy[1][0])
						
						a.SMP.append( (posCopy, fitnessValue) )
					
					if(SPC == True):
						a.SMP.pop()
						fitnessValue=f_eval(a.Posizione[0][0], a.Posizione[1][0])
						a.SMP.append( (a.Posizione.copy(), fitnessValue) )
						
					#Scelta del punto
					puntoMin = min(a.SMP, key=lambda x: x[1])[0]
					#puntoMax = max(a.SMP, key=lambda x: x[1])[0]
					a.Posizione=puntoMin.copy()
					
					a.SMP.clear()
				else:
					a.Velocita += c*(a.PosizioneMigliore-a.Posizione)
					a.Velocita[0][0] = max( min([v_max, a.Velocita[0][0]]), -v_max)
					a.Velocita[1][0] = max( min([v_max, a.Velocita[1][0]]), -v_max)
					a.Posizione += T_sim*a.Velocita
					
				
				#Valutazione con la posizione migliore
				valPos=f_eval(a.Posizione[0][0], a.Posizione[1][0])
				valBestPos=f_eval(a.PosizioneMigliore[0][0], a.PosizioneMigliore[1][0])
				if(valPos < valBestPos):
					a.PosizioneMigliore=a.Posizione.copy()
				
			yield k+1
					
	sistema.agenti=agenti
	return sistema
					
