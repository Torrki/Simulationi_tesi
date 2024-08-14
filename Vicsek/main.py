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
	parser_args.add_argument("D_attr", help="Distanza minima della forza di attrazione tra gli agenti")
	argsCmd=parser_args.parse_args()
	
	T=float(argsCmd.T_sim)
	linear_density=float(argsCmd.densita_lineare)
	v0=float(argsCmd.v_agenti)
	n_agenti=int(argsCmd.n_agenti)
	eta_random=float(argsCmd.eta_random)
	beta_attr=float(argsCmd.beta_attr)
	n_snaps=int(argsCmd.n_snaps)
	R0=float(argsCmd.R0)
	Dattr=float(argsCmd.D_attr)
	
	simulazione=Vicsek(T, linear_density, v0, n_agenti, eta_random, beta_attr, R0, Dattr)
	istanti=simulazione(n_snaps)
	
	#Animazione
	fig, ax=plt.subplots()
	points, =ax.plot([], [],'o')
	
	def update_points(statoVicsek):
		x_plt=list()
		y_plt=list()
		for i in range(n_agenti):
			x_plt.append( statoVicsek[i*2][0] )
			y_plt.append( statoVicsek[i*2+1][0] )
			
		points.set_data(x_plt,y_plt)		
		
		ax_xMin, ax_xMax = ax.get_xlim()
		ax_yMin, ax_yMax = ax.get_ylim()
		
		y_min, y_max=(min(y_plt), max(y_plt))
		x_min, x_max=(min(x_plt), max(x_plt))
		
		if(x_min <= ax_xMin):
			ax_xMin -= v0*3
			
		if(x_max >= ax_xMax):
			ax_xMax += v0*3
			
		if(y_min <= ax_yMin):
			ax_yMin -= v0*3
			
		if(y_max >= ax_yMax):
			ax_yMax += v0*3
		
		ax.set_xlim([ax_xMin, ax_xMax])
		ax.set_ylim([ax_yMin, ax_yMax])
	
		return points,
		
	L=n_agenti/(2.0*linear_density)
	lim=L*2.0
	ax.set_xlim([-lim, lim])
	ax.set_ylim([-lim, lim])
	
	anim=animation.FuncAnimation(fig, update_points, frames=istanti, interval=T*1000.0, blit=True)
	plt.show()
	
if __name__=="__main__":
	main()
	
