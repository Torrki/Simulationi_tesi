import argparse
from matplotlib import pyplot as plt
from matplotlib import animation
from Grafo import *
from ACO import ACO

def main():
	#parser per inserire la configurazione da linea di comando
	parser_args=argparse.ArgumentParser(description="Programma per la simulazione di un modello ACO", prog="ACO Sim")
	parser_args.add_argument("n_agenti", help="Numero di agenti attivi nella simulazione")
	parser_args.add_argument("n_snaps", help="Numero di snapshot dello stato del sistema")
	parser_args.add_argument("T_sim", help="Passo di simulazione")
	parser_args.add_argument("v_agenti", help="Modulo della velocità di ogni agente")
	parser_args.add_argument("freq_spawn", help="ogni quanti passi di simulazione far comparire una nuova formica")
	parser_args.add_argument("rho", help="tasso di evaporazione, deve essere tra 0 <= rho < 1")
	parser_args.add_argument("tau0", help="condizione iniziale dei ferormoni sugli archi")
	parser_args.add_argument("Q", help="Quantità di rilascio di ferormoni delle formiche")
	argsCmd=parser_args.parse_args()
	
	n_agenti=int(argsCmd.n_agenti)
	n_snaps=int(argsCmd.n_snaps)
	T_sim=float(argsCmd.T_sim)
	v0=float(argsCmd.v_agenti)
	freq_spawn=int(argsCmd.freq_spawn)
	rho=float(argsCmd.rho)
	tau0=float(argsCmd.tau0)
	Q=float(argsCmd.Q)
	
	#Creazione grafo
	coords=[(10,10), (20,14), (16,20), (21,30), (23,36), (28,39), (35,33), (37,39), (0,19), (3,28), (10,32), (10,36), (12,39), (-3,31), (3,40), (28,45)]

	Nodi=[NodoGrafo(c[0], c[1]) for c in coords]
	Nido=Nodi[0]
	NodoCibo=Nodi[-1]

	G=Grafo(tau0, rho, set(Nodi), Nido, NodoCibo)
	G.LinkNodes(Nido, Nodi[1],1)
	G.LinkNodes(Nodi[1], Nodi[2],1)
	G.LinkNodes(Nodi[2], Nodi[3],1)
	G.LinkNodes(Nodi[3], Nodi[4],1)
	G.LinkNodes(Nodi[4], Nodi[5],1)
	G.LinkNodes(Nodi[5], NodoCibo,1)
	G.LinkNodes(Nodi[3], Nodi[6],1)
	G.LinkNodes(Nodi[6], Nodi[7],1)
	G.LinkNodes(Nodi[7], NodoCibo,1)
	G.LinkNodes(Nido, Nodi[8],1)
	G.LinkNodes(Nodi[8], Nodi[9],1)
	G.LinkNodes(Nodi[9], Nodi[10],1)
	G.LinkNodes(Nodi[10], Nodi[11],1)
	G.LinkNodes(Nodi[11], Nodi[12],1)
	G.LinkNodes(Nodi[12], NodoCibo,1)
	G.LinkNodes(Nodi[9], Nodi[13],1)
	G.LinkNodes(Nodi[13], Nodi[14],1)
	G.LinkNodes(Nodi[14], Nodi[12],1)
	G.LinkNodes(Nodi[11], Nodi[14],1)
	
	simulazione=ACO(n_agenti, n_snaps, T_sim, freq_spawn, v0, rho, tau0, Q, G)
	istanti=simulazione(n_snaps)

	#Animazione
	fig, (axAn,axGr) =plt.subplots(nrows=2, ncols=1, figsize=(10,9))
	numeroArchi=len(G.Arcs)
	points, =axAn.plot([], [],'bo')
	listaLinee=list()
	listaFerormoni=list()
	t_plt=list()
	
	for a in range(numeroArchi):
		l, =axGr.plot([], [],lw=2)
		listaLinee.append(l)
		listaFerormoni.append(list())
	
	def init_plot():
		X_min = min(coords, key=lambda t: t[0])[0]
		X_max = max(coords, key=lambda t: t[0])[0]

		Y_min = min(coords, key=lambda t: t[1])[1]
		Y_max = max(coords, key=lambda t: t[1])[1]

		L_x = 0.1 * (X_max-X_min)
		L_y = 0.1 * (Y_max-Y_min)
		axGr.set_xlim([0, 1])
		axGr.set_ylim([0,tau0*1.5])
		axAn.set_xlim([X_min-L_x,X_max+L_x])
		axAn.set_ylim([Y_min-L_y,Y_max+L_y])		
		del t_plt[:]
		
		for a in range(numeroArchi):
			del listaFerormoni[a][:]
			listaLinee[a].set_data(t_plt, listaFerormoni[a])

	def update_figure(dati):
		statoACO, statoFerormoni, t=dati
		x_plt=list()
		y_plt=list()
		t *= T_sim
		
		for i in range(n_agenti):
			x_plt.append(statoACO[i*2][0])
			y_plt.append(statoACO[i*2+1][0])
			
		t_plt.append(t)
		f=statoFerormoni[0]
		for a in range(numeroArchi):
			listaFerormoni[a].append(statoFerormoni[a])
			f = statoFerormoni[a] if statoFerormoni[a] > f else f
																		
		tmin, tmax = axGr.get_xlim()
		fmin, fmax = axGr.get_ylim()
		
		if(t >= tmax):
			tmax *= 2
			axGr.set_xlim([tmin, tmax])
			
		if(f >= fmax):
			fmax *= 2
			axGr.set_ylim([fmin, fmax])
							
		points.set_data(x_plt, y_plt)
		for a in range(numeroArchi):
			listaLinee[a].set_data(t_plt, listaFerormoni[a])
		
		return [points] + listaLinee

	anim=animation.FuncAnimation(fig, update_figure, frames=istanti, interval=T_sim*1000.0, init_func=init_plot)
	plt.show()
	
if(__name__ == "__main__"):
	main()

