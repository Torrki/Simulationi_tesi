import numpy as np # type: ignore
import argparse
from matplotlib import pyplot as plt # type: ignore
from matplotlib import animation # type: ignore
from matplotlib.gridspec import GridSpec # type: ignore
from Vicsek import Vicsek

def main():
	#parser per inserire la configurazione da linea di comando
	parser_args=argparse.ArgumentParser(description="Programma per la simulazione di un modello Vicsek", prog="Vicsek Sim")
	parser_args.add_argument("n_agenti", help="Numero di agenti attivi nella simulazione")
	parser_args.add_argument("n_snaps", help="Numero di snapshot dello stato del sistema")
	parser_args.add_argument("T_sim", help="Passo di simulazione")
	parser_args.add_argument("v_agenti", help="Modulo della velocità di ogni agente")
	parser_args.add_argument("densita", help="Densità degli agenti lungo gli assi del sistema di riferimento")
	parser_args.add_argument("eta_random", help="Intensità del rumore")
	parser_args.add_argument("beta_attr", help="Intensità della forza di attrazione")
	parser_args.add_argument("R0", help="Raggio dell'intorno degli agenti")
	parser_args.add_argument("D_attr", help="Distanza minima della forza di attrazione tra gli agenti")
	argsCmd=parser_args.parse_args()
	
	T=float(argsCmd.T_sim)
	densita=float(argsCmd.densita)
	v0=float(argsCmd.v_agenti)
	n_agenti=int(argsCmd.n_agenti)
	eta_random=float(argsCmd.eta_random)
	beta_attr=float(argsCmd.beta_attr)
	n_snaps=int(argsCmd.n_snaps)
	R0=float(argsCmd.R0)
	Dattr=float(argsCmd.D_attr)
	
	simulazione=Vicsek(T, densita, v0, n_agenti, eta_random, beta_attr, R0, Dattr)
	istanti=simulazione(n_snaps)
	
	#Animazione
	fig = plt.figure()
	gs=GridSpec(2,2, figure=fig)
	ax=fig.add_subplot(gs[:,0])
	axGr=fig.add_subplot(gs[0,1])
	axVel=fig.add_subplot(gs[1,1])
	points, =ax.plot([], [], 'bo')
	CMpoint, =ax.plot([], [], 'ro')
	vecVel, =ax.plot([], [], lw=2, color='red')
	l, =axGr.plot([], [], lw=2)
	lVel, =axVel.plot([], [], lw=2)
	phase_plt=list()
	t_plt=list()
	vel_plt=list()
	vecPrec=None
	
	def init_plot():
		L=n_agenti/(2.0*densita)
		lim=L*2.0
		ax.set_xlim([-lim, lim])
		ax.set_ylim([-lim, lim])
		axGr.set_xlim([0, 1])
		axGr.set_ylim([-5, 5])
		axVel.set_xlim([0, 1])
		axVel.set_ylim([0, 10])	
		del t_plt[:]
		del phase_plt[:]
		del vel_plt[:]
		l.set_data(t_plt, phase_plt)
		lVel.set_data(t_plt, vel_plt)
		
		return l, lVel
	
	def update_points(dati):
		global vecPrec
		statoVicsek, velocitaVicsek, CMVicsek, t = dati
		x_plt=list()
		y_plt=list()
		faseVelVec=np.arctan2(velocitaVicsek[1][0], velocitaVicsek[0][0])
		
		if(t==0):
			vecPrec=velocitaVicsek.copy()
			phase_plt.append(faseVelVec)
		else:
			coseno = (vecPrec.T @ velocitaVicsek)/(np.linalg.norm(vecPrec)*np.linalg.norm(velocitaVicsek))

			moduloCoseno = np.abs(coseno[0][0])		#Per gestire gli errori numerici dovuti ai float
			if(moduloCoseno > 1):
					coseno[0][0] /= moduloCoseno

			vecPrecRot=(np.array([[0, -1], [1, 0]]) @ vecPrec).T
			angolo= np.arccos(coseno)[0][0] if vecPrecRot @ velocitaVicsek <= 0 else -np.arccos(coseno)[0][0]
			
			phase_plt.append( phase_plt[-1] + angolo )
			vecPrec=velocitaVicsek.copy()
		
		for i in range(n_agenti):
			x_plt.append( statoVicsek[i*2][0] )
			y_plt.append( statoVicsek[i*2+1][0] )
			
		moduloVelVec=np.linalg.norm(velocitaVicsek)
		vel_plt.append(moduloVelVec)
		t *= T
		t_plt.append(t)
		
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
		
		tmin, tmax = axGr.get_xlim()
		fmin, fmax = axGr.get_ylim()
		vmin, vmax = axVel.get_ylim()
		
		if(t >= tmax):
			if(tmax >= 8.0):
				tmax += 3.0
				tmin += 3.0
				
				nIstantiDel = int(3/T)
				
				del t_plt[:nIstantiDel]
				del phase_plt[:nIstantiDel]
				del vel_plt[:nIstantiDel]
			else:
				tmax *= 2
			axGr.set_xlim([tmin, tmax])
			axVel.set_xlim([tmin, tmax])
				
		if(phase_plt[-1] >= fmax):
			fmax *= 2
			axGr.set_ylim([fmin, fmax])
		elif(phase_plt[-1] <= fmin):
			fmin *= 2
			axGr.set_ylim([fmin, fmax])

		if(vel_plt[-1] >= vmax):
			vmax *= 2
			axVel.set_ylim([0, vmax])

		points.set_data(x_plt,y_plt)
		xVec=(CMVicsek[0][0], CMVicsek[0][0]+moduloVelVec*np.cos(faseVelVec))
		yVec=(CMVicsek[1][0], CMVicsek[1][0]+moduloVelVec*np.sin(faseVelVec))
		vecVel.set_data(xVec, yVec)
		l.set_data(t_plt, phase_plt)
		lVel.set_data(t_plt, vel_plt)
		CMpoint.set_data([xVec[0]], [yVec[0]])
	
		return points, vecVel, l, lVel
	
	axGr.set_title("Fase vettore velocità CM")
	axVel.set_title("Modulo vettore velocità CM")
	
	anim=animation.FuncAnimation(fig, update_points, frames=istanti, interval=T*1000.0, init_func=init_plot, save_count=200)
	plt.show()
	
if __name__=="__main__":
	main()
	
