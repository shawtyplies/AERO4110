from performance import W
from performance import V_stall
from performance import rho
from performance import C_D_0
from performance import S
from performance import k

## Take-Off Analysis
V_to = V_stall*0.94*1.1 # m/s - the required take-off safety speed is at least 1.1V_s (Raymer)
print(f"take-off speed = {V_to*1.944} knots")
D = (0.5*rho*S*C_D_0)*(V_to**2) + ((2*k*(W**2))/(rho*S))*(V_to**-2) # drag at take-off
print(f"Drag at take-off = {D} N")