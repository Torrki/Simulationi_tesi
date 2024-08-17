import argparse
from matplotlib import pyplot as plt # type: ignore
from matplotlib import animation # type: ignore
from Grafo import *
from ACO import ACO

def Euristica_1(a, n):
	dist = np.linalg.norm( n.Posizione-a.Nodi[1].Posizione )
	eurVal= 10 - dist/4
	return eurVal

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
	parser_args.add_argument("alpha", help="Peso dello stato degli archi")
	parser_args.add_argument("beta", help="Peso della funzione euristica")
	argsCmd=parser_args.parse_args()
	
	n_agenti=int(argsCmd.n_agenti)
	n_snaps=int(argsCmd.n_snaps)
	T_sim=float(argsCmd.T_sim)
	v0=float(argsCmd.v_agenti)
	freq_spawn=int(argsCmd.freq_spawn)
	rho=float(argsCmd.rho)
	tau0=float(argsCmd.tau0)
	Q=float(argsCmd.Q)
	alpha=float(argsCmd.alpha)
	beta=float(argsCmd.beta)
	
	#Creazione grafo
	coords=[(10,10), (20,14), (16,20), (21,30), (23,36), (28,39), (35,33), (37,39), (0,19), (3,28), (10,32), (10,36), (12,39), (-3,31), (3,40), (28,45)]

	Nodi=[NodoGrafo(c[0], c[1]) for c in coords]
	Nido=Nodi[0]
	NodoCibo=Nodi[-1]
	G=Grafo(set(Nodi), Nido, NodoCibo)
	G.LinkNodes(Nido, Nodi[1],1)
	G.LinkNodes(Nodi[1], Nodi[2],2)
	G.LinkNodes(Nodi[2], Nodi[3],2)
	G.LinkNodes(Nodi[3], Nodi[4],2)
	G.LinkNodes(Nodi[4], Nodi[5],2)
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

	simulazione=ACO(n_agenti, T_sim, freq_spawn, v0, tau0, rho, Q, G, alpha=alpha, beta=beta, euristic=Euristica_1)
	istanti=simulazione(n_snaps)

	#Preparazione animazione
	fig, (axAn, axGr) =plt.subplots(nrows=2, ncols=1, figsize=(8,8))

	axGr.set_title("Ferormoni rami")
	xminAn = min(coords, key=lambda c: c[0])[0]
	xmaxAn = max(coords, key=lambda c: c[0])[0]
	yminAn = min(coords, key=lambda c: c[1])[1]
	ymaxAn = max(coords, key=lambda c: c[1])[1]
	axAn.set_xlim([xminAn-3, xmaxAn+3])
	axAn.set_ylim([yminAn-3, ymaxAn+3])

	dictLineeGr=dict()
	dictLineeAn=dict()
	dictProbabilita=dict()
	t_plt=list()

	points, =axAn.plot([],[],'bo')
	pointNido, =axAn.plot([],[], 'go')
	pointCibo, =axAn.plot([],[], 'ro')

	for a in G.Arcs:
		l, =axAn.plot([],[],lw=2,ls='-')
		dictLineeAn[a]=l

	for n in G.Nodi:
		listaArchiNodo=list(n.Archi)
		listaArchi = [a for a in listaArchiNodo if a.Nodi[0] is n]
		if(len(listaArchi) > 1):
			for a in listaArchi:
				l=dictLineeAn[a]
				dictLineeGr[a], =axGr.plot([],[],lw=2,color=l.get_color())
				dictProbabilita[a]=list()

	def init_plot():
		del t_plt[:]

		for a in G.Arcs:
			linea=dictLineeAn[a]
			xLinea=[ a.Nodi[0].Posizione[0][0], a.Nodi[1].Posizione[0][0] ]
			yLinea=[ a.Nodi[0].Posizione[1][0], a.Nodi[1].Posizione[1][0] ]
			linea.set_data(xLinea, yLinea)

			if(a in dictProbabilita.keys()):
				del dictProbabilita[a][:]
				dictLineeGr[a].set_data(t_plt, dictProbabilita[a])

		pointNido.set_data([Nido.Posizione[0][0]], [Nido.Posizione[1][0]])
		pointCibo.set_data([NodoCibo.Posizione[0][0]], [NodoCibo.Posizione[1][0]])

		axGr.set_ylim([0, 1.2])
		axGr.set_xlim([0,2])

	def update_figure(dati):
		statoACO, statoProb, t=dati

		t_plt.append(t*T_sim)
		x_points=list()
		y_points=list()

		for i in range(n_agenti):
			x_points.append(statoACO[i*2][0])
			y_points.append(statoACO[i*2+1][0])

		j=0
		points.set_data(x_points, y_points)
		listaRet=list()
		f_max=0
		for a,l in dictLineeGr.items():
			dato=statoProb[j][0]
			dictProbabilita[a].append(dato)
			l.set_data(t_plt, dictProbabilita[a])
			listaRet.append(l)

			f_max = dato if dato > f_max else f_max
			j += 1

		t_minGr, t_maxGr = axGr.get_xlim()
		f_minGr, f_maxGr = axGr.get_ylim()

		if(t_plt[-1] > t_maxGr):
			if(t_maxGr >= 8):
				t_minGr += 3
				t_maxGr += 3

				delIstanti = int(3/T_sim)
				
				del t_plt[:delIstanti]
				for p in dictProbabilita.values():
					del p[:delIstanti]

			else:
				t_maxGr *= 2
			
			axGr.set_xlim([t_minGr, t_maxGr])

		if(f_max > f_maxGr):
			f_maxGr *= 2

			axGr.set_ylim([0,f_maxGr])

		return [points] + listaRet
	
	anim =animation.FuncAnimation(fig, func=update_figure, frames=istanti, init_func=init_plot, save_count=200, interval=T_sim*1000)
	plt.show()
	
if(__name__ == "__main__"):
	main()

