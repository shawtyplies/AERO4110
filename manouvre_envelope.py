import numpy as np
import matplotlib.pyplot as plt

# Aircraft parameters (in knots for velocity)
v_stall = 60  # Stall speed (knots)
v_cruise = 104.21  # Cruise speed (knots)
v_dive = 152.6  # Maximum dive speed (knots)
n_max = 3.8  # Maximum positive load factor
n_min = -1.5  # Maximum negative load factor

# Create velocity array for plotting (from 0 to V_dive)
v = np.linspace(0, v_dive, 500)

# Symmetric load factor calculation (mirrored positive and negative load factors)
n_factor = np.clip((v / v_stall)**2, 0, n_max)  # Use the same equation for both positive and negative sides

# Maneuvering envelope: constant load from V_cruise to V_dive
n_maneuver_pos = np.piecewise(v, [v < v_cruise, v >= v_cruise], [lambda v: np.clip((v / v_stall)**3, 0, n_max), n_max])
n_maneuver_neg = -n_maneuver_pos  # Mirror the positive load factor for the negative side

# Plotting the VN diagram
plt.figure(figsize=(10, 6))

# Positive side of the envelope (clipped)
plt.plot(v, n_maneuver_pos, label="Positive Load Factor", color='blue')

# Negative side of the envelope (mirrored)
plt.plot(v, n_maneuver_neg, label="Negative Load Factor", color='blue', linestyle='--')

# Stall speed at 1g (vertical line)
plt.axvline(x=v_stall, color='black', linestyle=':', label="V_stall 1g")

# Cruise speed (vertical line)
plt.axvline(x=v_cruise, color='black', linestyle='-.', label="V_cruise")

# Maximum dive speed (V_dive) (vertical line)
plt.axvline(x=v_dive, color='black', linestyle='-', label="V_dive")

# Structural load limits
plt.axhline(y=n_max, color='red', linestyle='-', label="Maximum Positive Load Factor")
plt.axhline(y=n_min, color='red', linestyle='-', label="Maximum Negative Load Factor")

# Adding annotations for velocities

plt.text(v_cruise - 5, n_min - 1.1, f"{v_cruise:.2f}", rotation=0, verticalalignment='bottom')
plt.text(v_dive - 5, n_min - 1.1, f"{v_dive}", rotation=0, verticalalignment='bottom')

# Labels and limits
plt.xlim(0, v_dive + 10)
plt.ylim(n_min - 0.5, n_max + 0.5)
plt.xlabel("Velocity (kts)")
plt.ylabel("Load Factor (n)")
plt.title("VN Diagram (Symmetric Maneuver Envelope)")

# Legend
plt.legend()

# Grid
plt.grid(True)

# Show the plot
plt.show()
