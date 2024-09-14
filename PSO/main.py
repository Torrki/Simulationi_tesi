import argparse
from matplotlib import pyplot as plt # type: ignore
from matplotlib import animation # type: ignore
import numpy as np # type: ignore
from PSO import PSO

def MinimiLocali(x,y):
	return np.sin(x/4)*np.sin(y/4)

def Cerchio(x,y, dx=0, dy=0):
	circonferenza=np.power(x-dx,2) + np.power(y-dy,2) - 4
	return -np.power(circonferenza, 2) + 1
	
def Poli(x,y):
	polo_x=np.power(np.power(x,2)-16,2)
	polo_y=np.power(np.power(y,2)-16,2)
	return -(polo_x+polo_y)

def Paraboloide_0(x,y):
	return (np.power(x,2)+np.power(y,2) -3)
	
def Paraboloide_1(x,y):
	return -(np.power(x-10,2)+np.power(y-10,2) -3)
	
def Paraboloide_2(x,y):
	return -(np.power(x+4,2)+np.power(y+4,2) -3)
	
def Paraboloide_3(x,y):
	return -(np.power(x+4,2)+np.power(y-4,2) -3)
	
def Paraboloide_4(x,y):
	return -(np.power(x-4,2)+np.power(y+4,2) -3)

def main():
	#parser per inserire la configurazione da linea di comando
	parser_args=argparse.ArgumentParser(description="Programma per la simulazione di un modello PSO", prog="PSO Sim")
	parser_args.add_argument("n_agenti", help="Numero di agenti attivi nella simulazione")
	parser_args.add_argument("n_snaps", help="Numero di snapshot dello stato del sistema")
	parser_args.add_argument("T_sim", help="Passo di simulazione")
	parser_args.add_argument("v_max", help="Modulo della velocità massima degli agenti")
	parser_args.add_argument("densita", help="Densità degli agenti lungo gli assi del sistema di riferimento")
	parser_args.add_argument("c1", help="Intensità dell'apprendimento individuale")
	parser_args.add_argument("c2", help="Intensità dell'apprendimento sociale")
	parser_args.add_argument("beta_attr", help="Intensità della forza di attrazione")
	parser_args.add_argument("D_attr", help="Distanza minima della forza di attrazione tra gli agenti")
	argsCmd=parser_args.parse_args()
	
	T_sim=float(argsCmd.T_sim)
	densita=float(argsCmd.densita)
	v_max=float(argsCmd.v_max)
	n_agenti=int(argsCmd.n_agenti)
	c1=float(argsCmd.c1)
	c2=float(argsCmd.c2)
	beta_attr=float(argsCmd.beta_attr)
	n_snaps=int(argsCmd.n_snaps)
	D_attr=float(argsCmd.D_attr)
	
	simulazione=PSO(n_agenti, densita, v_max, T_sim, c1, c2, beta_attr, Paraboloide_0, D_attr)
	istanti=simulazione(n_snaps)
	
	#Animazione
	fig, axAn =plt.subplots()
	points, =axAn.plot([], [],'bo')
			
	def update_figure(statoPSO):		
		x_plt=list()
		y_plt=list()
		
		for i in range(n_agenti):
			x_plt.append(statoPSO[i*2][0])
			y_plt.append(statoPSO[i*2+1][0])
		
		y_min, y_max=(min(y_plt), max(y_plt))
		x_min, x_max=(min(x_plt), max(x_plt))
		
		axAn.set_xlim([x_min-5, x_max+5])
		axAn.set_ylim([y_min-5, y_max+5])
							
		points.set_data(x_plt, y_plt)
		return points,

	L=n_agenti/(2.0*densita)
	lim=L*1.3
	axAn.set_xlim([-lim, lim])
	axAn.set_ylim([-lim, lim])
	anim=animation.FuncAnimation(fig, update_figure, frames=istanti, interval=T_sim*1000.0, save_count=200, repeat=True)
	plt.show()
	
if(__name__ == "__main__"):
	main()
