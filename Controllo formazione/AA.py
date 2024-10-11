import numpy as np #type: ignore

class ActiveAgent:
    def __init__(self, P0, kx, ky, P0_ref, role):
        self.Posizione=P0.copy().reshape((2,1))
        self.P_refPrec=P0_ref.copy().reshape((2,1))
        self.K = np.array([ [kx, 0],[0, ky] ])
        self.Name=role
        
    def Move(self, Tc, p_ref):
        self.Posizione = (np.eye(2) - Tc*self.K) @ (self.Posizione - self.P_refPrec) + p_ref
        
        self.P_refPrec=p_ref.copy()
        
