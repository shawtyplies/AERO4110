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
rho_values = [1.225, 1.112, 1.007, 0.9093, 0.8194, 0.7364, 0.6601, 0.5900, 0.5258, 0.4671, 0.4135]  # kg/m^3 at different altitudes
altitudes = np.linspace(0, 20000, len(rho_values))  # convert service ceiling to meters
service_ceiling = 15534 / 3.281  # in meters

# Calculate V_s and V_max at each altitude
V_s_values = np.sqrt(2 * W / (np.array(rho_values) * S * C_L_max))
V_max_values = ((2 * P_av) / (np.array(rho_values) * S * C_D_0))**(1/3)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(V_s_values, altitudes, label="Stall Speed (V_s)", color='blue')
plt.plot(V_max_values, altitudes, label="Max Speed (V_max)", color='red')

# Add service ceiling line
plt.axhline(service_ceiling, color='green', linestyle='--', label="Service Ceiling")

ax = plt.gca()
# ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 20000])

# Labels and legend
plt.xlabel("Airspeed (m/s)")
plt.ylabel("Altitude (m)")
plt.title("Airspeed vs. Altitude Flight Envelope")
plt.legend()
plt.grid()
plt.show()
