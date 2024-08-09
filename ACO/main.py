import ArtificialAnt as AA
from Grafo import *
from matplotlib import pyplot as plt
from matplotlib import animation

coords=[(10,10), (20,14), (16,20), (21,30), (23,36), (28,39), (35,33), (37,39), (0,19), (3,28), (10,32), (10,36), (12,39), (-3,31), (3,40), (28,45)]

Nodi=[NodoGrafo(c[0], c[1]) for c in coords]
Nido=Nodi[0]
NodoCibo=Nodi[-1]

G=Grafo(0.8, 1e-3, set(Nodi))
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

n_snaps=2000
T=3e-2
n_agenti=100
freqSpawn=7

Formiche={AA.ArtificialAnt(Nido) for f in range(n_agenti)}

def sistema(passi : int):
	FormicheAttive=list()
	statoACO=np.zeros((n_agenti*2,1))
	for j in range(n_agenti):
		statoACO[[j*2, (j*2)+1]]=np.copy(Nido.posizione)
	snaps=np.copy(statoACO)
	
	for p in range(passi):
		if(p % freqSpawn == 0 and len(Formiche) > 0):
			F0=Formiche.pop()
			F0.Attiva=True
			FormicheAttive.append(F0)
			
			arco0=Nido.ChoiceArc()
			F0.AppendArc(arco0)
			direzione0=arco0.Nodi[1].posizione-F0.Posizione
			direzione0=direzione0/np.linalg.norm(direzione0)
			F0.Direzione=direzione0
		
		for i in range(len(FormicheAttive)):
			f=FormicheAttive[i]
			lastArc=f.Percorso[-1]
			if(not f.Cibo):
				if(lastArc.Nodi[1].InBound(f.Posizione)):
					arco=lastArc.Nodi[1].ChoiceArc()
						
					if(arco is not None):
						f.AppendArc(arco)
								
						direzione=arco.Nodi[1].posizione-f.Posizione
						direzione=direzione/np.linalg.norm(direzione)
						f.Direzione=direzione
					elif(lastArc.Nodi[1] is NodoCibo):
						f.Cibo= True
						f.Direzione = -f.Direzione
						print("Costo: ", f.CostoPercorso)
			else:
				if(lastArc.Nodi[0].InBound(f.Posizione)):
					#Rilascio ferormoni
					lastArc.RilascioFormiche += f.Q/f.CostoPercorso
					
					f.Percorso.pop()
					if(lastArc.Nodi[0] is not Nido):
						lastArc=f.Percorso[-1]
						direzione=lastArc.Nodi[0].posizione-f.Posizione
						direzione=direzione/np.linalg.norm(direzione)
						f.Direzione=direzione
					else:
						f.Cibo= False
						f.CostoPercorso=0
						
						arco0=Nido.ChoiceArc()
						f.AppendArc(arco0)
						direzione0=arco0.Nodi[1].posizione-f.Posizione
						direzione0=direzione0/np.linalg.norm(direzione0)
						f.Direzione=direzione0
					
			dP=T*(f.V/lastArc.Costo)*f.Direzione
			f.Posizione += dP
			statoACO[[i*2, (i*2)+1]] += dP
			
		G.Update()
		snaps = np.concatenate((snaps, statoACO), axis=1)
	return snaps
			
istanti=sistema(n_snaps)

#Animazione
fig, ax=plt.subplots()
points, =ax.plot([], [],'bo')

def update_points(nframe):
	x_plt=list()
	y_plt=list()
	
	for i in range(n_agenti):
		x_plt.append(istanti[i*2][nframe])
		y_plt.append(istanti[i*2+1][nframe])
	
	#for c in coords:
	#	x_plt.append(c[0])
	#	y_plt.append(c[1])
		
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

anim=animation.FuncAnimation(fig, update_points, n_snaps, interval=T*1000.0, blit=True)
plt.show()

