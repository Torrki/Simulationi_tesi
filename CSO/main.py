from CSO import CSO
import numpy as np
from matplotlib import pyplot as plt # type: ignore
from matplotlib import animation # type: ignore

def Paraboloide(x, y):
	return np.power(x-4, 2)+np.power(y-4,2)
	
def MinimiLocali(x, y):
	return np.sin(x)*np.sin(y)
	
def Funzione(x,y):
	return -2*(np.power(x,2)+np.power(y,2))+(np.power(x, 4)+np.power(y,4)) -3

def Rosenbrock(x,y):
	return np.power(5-x, 2)+10*np.power( (y-np.power(x,2)), 2)

def main():
	n_agenti=30
	densita=1
	T_sim=0.01
	sistema=CSO(n_agenti, T_sim, 10, 16, densita, 1e-2, 1, False, 8, 5e-1, Funzione)
	istanti=sistema(8000)
	
	#Animazione
	fig, ax =plt.subplots()
	points, =ax.plot([], [],'bo')
			
	def update_figure(t):		
		x_plt=list()
		y_plt=list()
		
		for ag in sistema.agenti:
			x_plt.append(ag.Posizione[0][0])
			y_plt.append(ag.Posizione[1][0])
										
		points.set_data(x_plt, y_plt)
		
		#Impostazione dei margini della finestra del piano
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
		
		return points,

	L=n_agenti/(2*densita)
	lim=L*1.3
	ax.set_xlim([-lim, lim])
	ax.set_ylim([-lim, lim])
	anim=animation.FuncAnimation(fig, update_figure, frames=istanti, interval=T_sim*1000.0, save_count=200, repeat=False)
	plt.show()
	
if(__name__ == '__main__'):
	main()
