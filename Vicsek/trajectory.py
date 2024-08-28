import numpy as np # type: ignore
import argparse
from matplotlib import pyplot as plt # type: ignore
from matplotlib import animation # type: ignore
from matplotlib.gridspec import GridSpec # type: ignore
from VicsekTrajectory import Vicsek

def SineTrajectory(passi: int, T_sim: float):
	for p in range(passi):
		y=np.sin(4*p*T_sim)
		x=1.0
		
		yield np.array([[x],[y]], dtype=np.dtype(float))
		
def CircularTrajectory(passi: int, T_sim: float):
	for p in range(passi):
		y=np.sin(p*T_sim)
		x=np.cos(p*T_sim)
		
		yield np.array([[x],[y]], dtype=np.dtype(float))
		
def InfiniteTrajectory(passi: int, T_sim: float):
	for p in range(passi):
		y=np.sin(2*p*T_sim + np.pi/2)
		x=np.cos(p*T_sim)
		
		yield np.array([[x],[y]], dtype=np.dtype(float))
		
def SpiralTrajectory(passi: int, T_sim: float, v: float):
	R=10
	for p in range(passi):
		y=np.sin(2*(v/R)*p*T_sim)
		x=np.cos(2*(v/R)*p*T_sim)
		R += 0.01
		
		yield np.array([[x],[y]], dtype=np.dtype(float))

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
	
	simulazione=Vicsek(T, densita, v0, n_agenti, eta_random, beta_attr, R0, Dattr, traj=CircularTrajectory(n_snaps, T), lamb=10)	
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
	lPhase, =axGr.plot([], [], lw=2)
	lVel, =axVel.plot([], [], lw=2)
	phase_plt=list()
	t_plt=list()
	vel_plt=list()
	vecPrec=None
	
	lineeDirezioneAgenti=dict()
	lunghezzaLinee=3
	
	for ag in simulazione.agenti:
		l, =ax.plot([],[], lw=2, color='blue')
		lineeDirezioneAgenti[ag]=l
	
	def init_plot():
		L=n_agenti/(2.0*densita)
		lim=L*2.0
		ax.set_xlim([-lim, lim])
		ax.set_ylim([-lim, lim])
		axGr.set_xlim([0, 1])
		axGr.set_ylim([-5, 5])
		axVel.set_xlim([0, 1])
		axVel.set_ylim([0, 10])	
		del t_plt[:], phase_plt[:], vel_plt[:]
		
		lPhase.set_data(t_plt, phase_plt)
		lVel.set_data(t_plt, vel_plt)
		
		return lPhase, lVel
	
	def update_points(dati):
		global vecPrec
		velocitaVicsek, CMVicsek, t = dati
		x_plt=list()
		y_plt=list()
		faseVelVec=np.arctan2(velocitaVicsek[1][0], velocitaVicsek[0][0])
		
		if(t==0):
			vecPrec=velocitaVicsek.copy()
			phase_plt.append(faseVelVec)
		else:
			normaVelPrec=np.linalg.norm(vecPrec)
			normaVelocitaVicsek=np.linalg.norm(velocitaVicsek)
			
			complVelPrec=complex(vecPrec[0][0], vecPrec[1][0])
			complVelVicsek=complex(velocitaVicsek[0][0], velocitaVicsek[1][0])
			if(complVelPrec != complex(0,0)):
				complTrasformazione=complVelVicsek/complVelPrec
				angolo=np.arctan2(complTrasformazione.imag, complTrasformazione.real)
				phase_plt.append( phase_plt[-1] + angolo )
			else:
				phase_plt.append( phase_plt[-1] )
				
			vecPrec=velocitaVicsek.copy()
		
		for ag in simulazione.agenti:
			x_plt.append( ag.Posizione[0][0] )
			y_plt.append( ag.Posizione[1][0] )
			lineeDirezioneAgenti[ag].set_data( [ ag.Posizione[0][0], ag.Posizione[0][0]+lunghezzaLinee*ag.Orientamento[0][0] ],[ ag.Posizione[1][0], ag.Posizione[1][0]+lunghezzaLinee*ag.Orientamento[1][0] ] )	
			
		moduloVelVec=np.linalg.norm(velocitaVicsek)
		vel_plt.append(moduloVelVec)
		t *= T
		t_plt.append(t)
		
		ax_xMin, ax_xMax = ax.get_xlim()
		ax_yMin, ax_yMax = ax.get_ylim()
		
		y_min, y_max=(min(y_plt), max(y_plt))
		x_min, x_max=(min(x_plt), max(x_plt))
		
		if(x_min <= ax_xMin):
			ax_xMin -= abs(ax_xMin)*0.5
			
		if(x_max >= ax_xMax):
			ax_xMax += abs(ax_xMax)*0.5
			
		if(y_min <= ax_yMin):
			ax_yMin -= abs(ax_yMin)*0.5
			
		if(y_max >= ax_yMax):
			ax_yMax += abs(ax_yMax)*0.5
		
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
		lPhase.set_data(t_plt, phase_plt)
		lVel.set_data(t_plt, vel_plt)
		CMpoint.set_data([xVec[0]], [yVec[0]])
	
		return points, vecVel, lPhase, lVel
	
	axGr.set_title("Fase vettore velocità CM")
	axVel.set_title("Modulo vettore velocità CM")
	
	anim=animation.FuncAnimation(fig, update_points, frames=istanti, interval=T*1000.0, init_func=init_plot, save_count=200, repeat=False)
	plt.show()
	
if __name__=="__main__":
	main()
	
