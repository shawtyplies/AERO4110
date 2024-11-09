""" 
Flight operating envelope 

"""

import numpy as np
import matplotlib.pyplot as plt

# Aircraft Parameters
MTOW = 868.63 # kg
W = MTOW*9.81 # N
S = 14.4 # m^2
C_D_0 = 0.03 
P_av = 134226*0.84 # watts
C_L_max = 1.6
rho = [1.225, 1.056, 0.905, 0.770, 0.654]
service_ceiling = 15534 / 3.281 # m

# Relations
V_s = np.sqrt(2*W/((rho*S*C_L_max))) # m/s
V_max = ((2*P_av) / (rho*S*C_D_0))**(1/3) # m/s