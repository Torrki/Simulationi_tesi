import numpy as np # type: ignore

def Normalizzazione(vec):
	if(np.linalg.norm(vec) > 0):
		angolo=np.arctan2(vec[1][0], vec[0][0])
		vec[0][0]=np.cos(angolo)
		vec[1][0]=np.sin(angolo)

