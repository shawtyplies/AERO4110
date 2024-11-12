""" 
Flight operating envelope 

"""

import numpy as np
import matplotlib.pyplot as plt

# Aircraft Parameters
MTOW = 868.63  # kg
W = MTOW * 9.81  # N
S = 14.4  # m^2
C_D_0 = 0.03 
P_av = 134226 * 0.84  # watts
C_L_max = 1.6
rho_values = [1.225, 1.056, 0.905, 0.770, 0.654, 0.5494, 0.4597]  # kg/m^3 at different altitudes
alt_values = [0, 5000, 10000, 15000, 20000, 25000, 30000] # ft
pressures = []
# altitudes = np.linspace(0, 15534, len(alt_values))  # ft
# service_ceiling = 15534 # ft
# service_ceiling_met = 15534 / 3.281  # m

# Calculate V_s and V_max at each altitude
V_s_values = np.sqrt(2 * W / (np.array(rho_values) * S * C_L_max)) * 1.944 # knots
V_max_values = ((2 * P_av) / (np.array(rho_values) * S * C_D_0))**(1/3) * 1.944 # knots
# TAS = 

# service ceiling 


# Plot
plt.figure(figsize=(10, 6))
plt.plot(V_s_values, rho_values, label="Stall Speed (V_s)", color='blue')
plt.plot(V_max_values, rho_values, label="Max Speed (V_max)", color='red')
ax = plt.gca()
# ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 40000])

# Add service ceiling line
# plt.axhline(service_ceiling, color='green', linestyle='--', label="Service Ceiling")

# Labels and legend
plt.xlabel("Airspeed (knots)")
plt.ylabel("Altitude (ft)")
plt.title("Airspeed vs. Altitude Flight Envelope")
plt.legend()
plt.grid()
plt.show()

