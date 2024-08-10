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

	G=Grafo(rho, tau0, set(Nodi), Nido, NodoCibo)
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
	fig, ax=plt.subplots()
	points, =ax.plot([], [],'bo')

	def update_points(nframe):
		x_plt=list()
		y_plt=list()
		
		for i in range(n_agenti):
			x_plt.append(istanti[i*2][nframe])
			y_plt.append(istanti[i*2+1][nframe])
			
		points.set_data( np.array([ x_plt,
																y_plt ]) )
		return points,
	X_min = min(coords, key=lambda t: t[0])[0]
	X_max = max(coords, key=lambda t: t[0])[0]

	Y_min = min(coords, key=lambda t: t[1])[1]
	Y_max = max(coords, key=lambda t: t[1])[1]

	L_x = 0.1 * (X_max-X_min)
	L_y = 0.1 * (Y_max-Y_min)
	ax.set_xlim([X_min-L_x,X_max+L_x])
	ax.set_ylim([Y_min-L_y,Y_max+L_y])

	anim=animation.FuncAnimation(fig, update_points, n_snaps, interval=T_sim*1000.0, blit=True)
	plt.show()
	
if(__name__ == "__main__"):
	main()

