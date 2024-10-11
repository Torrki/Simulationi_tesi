import numpy as np # type: ignore
import argparse
from matplotlib import pyplot as plt # type: ignore
from matplotlib import animation # type: ignore
from matplotlib.gridspec import GridSpec # type: ignore
from Formazione import Formazione

def traiettoriaRef(Tc, n_istanti):
    for i in range(n_istanti+1):
        yield np.array([[50+40*np.cos(10*Tc*i)],[50+40*np.sin(10*Tc*i)]])
        
def GenFormazione(Tc, n_istanti):
    R=5
    rotazione=np.eye(2)
    teta=0
    for i in range(n_istanti+1):
        teta = 10*Tc*i
        rotazione[0][0]=np.cos(teta)
        rotazione[1][1]=np.cos(teta)
        rotazione[0][1]=-np.sin(teta)
        rotazione[1][0]=np.sin(teta)
        yield ( rotazione @ np.array([ [0, 30, -30, 0, 0],[0, 0, 0, -30, 30] ]) ).T

def main():
    T_sim=0.001
    densita=0.3
    n_agenti=5
    n_snaps=8000
	
    simulazione=Formazione(n_agenti, T_sim, densita, GenFormazione(T_sim, n_snaps), traiettoriaRef(T_sim, n_snaps))
    istanti=simulazione(n_snaps)
	
    #Animazione
    fig, axAn =plt.subplots()
    points, =axAn.plot([], [],'bo')
    leaderPoint, =axAn.plot([], [], 'mo')
    Rif, =axAn.plot([], [], 'go')
			
    def update_figure(dati):
        CM_vect, rif_vect, t= dati
        x_plt=list()
        y_plt=list()
        
        for ag in simulazione.agenti:
            if(ag.Name == 'leader'):
                leaderPoint.set_data([ [ag.Posizione[0][0]], [ag.Posizione[1][0]] ])
            else:
                x_plt.append(ag.Posizione[0][0])
                y_plt.append(ag.Posizione[1][0])
            
        #Impostazione dei margini della finestra del piano
        ax_xMin, ax_xMax = axAn.get_xlim()
        ax_yMin, ax_yMax = axAn.get_ylim()
		
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
		
        axAn.set_xlim([ax_xMin, ax_xMax])
        axAn.set_ylim([ax_yMin, ax_yMax])
							
        points.set_data(x_plt, y_plt)
        Rif.set_data([ [rif_vect[0][0]], [rif_vect[1][0]] ])
        return points, Rif, leaderPoint
        
    L=n_agenti/(2.0*densita)
    lim=L*1.3
    axAn.set_xlim([-40, 40])
    axAn.set_ylim([-40, 40])
    anim=animation.FuncAnimation(fig, update_figure, frames=istanti, interval=T_sim*1000.0, save_count=200, repeat=False)
    plt.show()
	
if(__name__ == "__main__"):
	main()
