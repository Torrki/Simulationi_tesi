import numpy as np
import argparse
from matplotlib import pyplot as plt
from matplotlib import animation
from Vicsek import Vicsek

def main():
	#parser per inserire la configurazione da linea di comando
	parser_args=argparse.ArgumentParser(description="Programma per la simulazione di un modello Vicsek", prog="Vicsek Sim")
	parser_args.add_argument("n_agenti", help="Numero di agenti attivi nella simulazione")
	parser_args.add_argument("n_snaps", help="Numero di snapshot dello stato del sistema")
	parser_args.add_argument("T_sim", help="Passo di simulazione")
	parser_args.add_argument("v_agenti", help="Modulo della velocità di ogni agente")
	parser_args.add_argument("densita_lineare", help="Densità degli agenti lungo gli assi del sistema di riferimento")
	parser_args.add_argument("eta_random", help="Intensità del rumore")
	parser_args.add_argument("beta_attr", help="Intensità della forza di attrazione")
	parser_args.add_argument("R0", help="Raggio dell'intorno degli agenti")
	argsCmd=parser_args.parse_args()
	
	T=float(argsCmd.T_sim)
	linear_density=float(argsCmd.densita_lineare)
	v0=float(argsCmd.v_agenti)
	n_agenti=int(argsCmd.n_agenti)
	eta_random=float(argsCmd.eta_random)
	beta_attr=float(argsCmd.beta_attr)
	n_snaps=int(argsCmd.n_snaps)
	R0=float(argsCmd.R0)
	
	simulazione=Vicsek(T, linear_density, v0, n_agenti, eta_random, beta_attr, R0)
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
	
