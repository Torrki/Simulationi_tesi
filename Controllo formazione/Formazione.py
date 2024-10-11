from AA import ActiveAgent
import numpy as np # type: ignore
from numpy import random as rnd # type: ignore

def Formazione(n_agenti, Tc, densita, posizioni, riferimento):
    guadagni_x = [7]*n_agenti
    guadagni_y = [7]*n_agenti
    ruoli= ['leader'] + ['slave']*(n_agenti-1)
    L = n_agenti/(2.0*densita)
    seme_random=100
    
    gen=rnd.default_rng(seme_random) #Random Generator
    posizioniInizialiX=gen.uniform(low=-L, high=L, size=(n_agenti,1))
    posizioniInizialiY=gen.uniform(low=-L, high=L, size=(n_agenti,1))
    posizioniIniziali = np.concatenate((posizioniInizialiX, posizioniInizialiY), axis=1)
    print(posizioniIniziali)
    posFormazione_0 = next(posizioni)
    rif_0=next(riferimento)
	
    listaAgenti=[ActiveAgent(p0, kx, ky, rif_0+pf_0.reshape((2,1)), r) for p0, kx, ky, pf_0, r in zip(posizioniIniziali, guadagni_x, guadagni_y, posFormazione_0, ruoli)]

    def sistema(n_snaps):
        CM=np.zeros((2,1))
    
        for ag in listaAgenti:
            CM += ag.Posizione
        CM /= n_agenti
        leaderAgent = next(ag for ag in listaAgenti if ag.Name=='leader')
        
        yield CM.copy() , rif_0, 0
        for i in range(1, n_snaps+1):
            CM[0][0]=0
            CM[1][0]=0
            rif=next(riferimento)
            posFormazione=next(posizioni)
            for ag, pf in zip(listaAgenti, posFormazione):
                if(ag == leaderAgent):
                    p_ref=rif+pf.reshape((2,1))
                    ag.Move(Tc, p_ref)
                else:
                    p_ref=leaderAgent.P_refPrec + pf.reshape((2,1))
                    ag.Move(Tc, p_ref)                
                CM += ag.Posizione
            CM /= n_agenti
                
            yield CM.copy(), rif, i
            
    sistema.agenti=listaAgenti
    return sistema
