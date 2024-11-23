""" 
Flight operating envelope 

"""

import numpy as np
import matplotlib.pyplot as plt

# Aircraft Parameters
MTOW = 903  # kg
W = MTOW * 9.81  # N
S = 14.4  # m^2
C_D_0 = 0.03 
P_av = 134226 * 0.84  # watts
C_L_max = 2.4
rho_values = [1.225, 1.112, 1.007, 0.9093, 0.8194, 0.7364, 0.7056]  # kg/m^3 at different altitudes
altitudes = np.linspace(0, 20000, len(rho_values))  
service_ceiling = 12087 # in ft

# Calculate V_s and V_max at each altitude
V_s_values = np.sqrt(2 * W / (np.array(rho_values) * S * C_L_max)) * 1.94384  # in knots
V_max_values = ((2 * P_av) / (np.array(rho_values) * S * C_D_0))**(1/3) * 1.94384  # in knots

# Plot
plt.figure(figsize=(10, 6))
plt.plot(V_s_values, altitudes, label="Stall Speed", color='blue')
plt.plot(V_max_values, altitudes, label="Max Speed", color='green')

# Add service ceiling line
plt.axhline(service_ceiling, color='orange', linestyle='--', label="Service Ceiling")
# plt.axhline(safe_service_ceiling, color='purple', linestyle='--', label="Safe Service Ceiling")

ax = plt.gca()
ax.set_xlim([0, 200])
ax.set_ylim([0, 15000])

# Labels and legend
plt.xlabel("Airspeed (kts)")
plt.ylabel("Altitude (ft)")
plt.title("Airspeed vs. Altitude Flight Envelope")
plt.legend()
plt.grid()
plt.show()
