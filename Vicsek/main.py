import numpy as np
import matplotlib as plot
import numpy.random as rnd
import argparse
from ActiveAgent import ActiveAgent
from matplotlib import pyplot as plt
from matplotlib import animation

seme_random=55
gen=rnd.default_rng(seme_random) #Random Generator

def Vicsek(T: float, density: float, v0: float, N:int, eta: float): #funzione decoratore per configurare la simulazione
	'''
	Funzione per la configurazione di un modello Vicsek:
	T 					è il periodo di osservazione
	density 		è la densità degli agenti nello spazio
	v0 					è la velocità degli agenti
	N						è il numero di agenti attivi
	eta					é l'intensità del rumore
	
	torna una funzione che permette di eseguire la simulazione
	'''
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
					s_vicini += connettivita[j,i]*agenti[j].getDirection()
					
				rumore=gen.standard_normal(size=(2,1))
				rumore_norm = rumore/np.linalg.norm(rumore)
					
				statoVicsek[[i_stato,i_stato+1]] += T*v0*s_i #aggiornamento delle posizioni nello stato
				agenti[i].setPosition(statoVicsek[[i_stato,i_stato+1]])
				
				new_s= (s_vicini+eta*rumore_norm)/np.linalg.norm(s_vicini+eta*rumore_norm) #aggiornamento dell'orientamento degli agenti
					
				agenti[i].setDirection( new_s )
				
			snaps=np.concatenate((snaps, statoVicsek),axis=1) #aggiungo il nuovo stato nella raccolta
		return snaps
	
	return sistema
	


def main():
	#parser per inserire la configurazione da linea di comando
	parser_args=argparse.ArgumentParser(description="Programma per la simulazione di un modello Vicsek", prog="Vicsek Sim")
	parser_args.add_argument("n_agenti", help="Numero di agenti attivi nella simulazione")
	parser_args.add_argument("n_snaps", help="Numero di snapshot dello stato del sistema")
	parser_args.add_argument("T_sim", help="Passo di simulazione")
	parser_args.add_argument("v_agenti", help="Modulo della velocità di ogni agente")
	parser_args.add_argument("densita_lineare", help="Densità degli agenti lungo gli assi del sistema di riferimento")
	parser_args.add_argument("eta_random", help="Intensità del rumore")
	parser_args.add_argument("R0", help="Raggio dell'intorno degli agenti")
	argsCmd=parser_args.parse_args()
	
	T=float(argsCmd.T_sim)
	linear_density=float(argsCmd.densita_lineare)
	v0=float(argsCmd.v_agenti)
	n_agenti=int(argsCmd.n_agenti)
	eta_random=float(argsCmd.eta_random)
	n_snaps=int(argsCmd.n_snaps)
	ActiveAgent.raggioIntorno=float(argsCmd.R0)
	
	simulazione=Vicsek(T, linear_density, v0, n_agenti, eta_random)
	istanti=simulazione(n_snaps)
	
	#Animazione
	fig, ax=plt.subplots()
	points, =ax.plot([], [],'o')
	
	def update_points(nframe):
		x_plt=list()
		y_plt=list()
		for i in range(n_agenti):
			x_plt.append( istanti[i*2,nframe] )
			y_plt.append( istanti[i*2+1,nframe] )
			
		points.set_data( np.array([ x_plt,
																y_plt ]) )
		return points,
	
	L_plot=(n_agenti/(2.0*linear_density))+30
	ax.set_xlim([-L_plot,L_plot])
	ax.set_ylim([-L_plot,L_plot])
	
	anim=animation.FuncAnimation(fig, update_points, n_snaps, interval=T*1000.0, blit=True)
	plt.show()
	
if __name__=="__main__":
	main()
	
