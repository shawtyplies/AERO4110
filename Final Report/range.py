import math

specific_fuel_consumption = 0.000115226 #0.0001471
specific_fuel_consumption_l = 0.000152
lift_to_drag_ratio = (11.12+10.28) / 2 # 9.31
initial_weight = 1968
final_weight = 1747
velocity = 176  
prop_efficiency = 0.84
velocity_mp = 101 


range_cruise = (
        ((velocity/((specific_fuel_consumption * velocity)/(550*prop_efficiency))) * lift_to_drag_ratio * (math.log(initial_weight/final_weight)) ))

print(f"Range = {range_cruise} ft")
print(f"Range = {range_cruise/6076} nmi")

loiter_endurance = (lift_to_drag_ratio)*((550*prop_efficiency)/(specific_fuel_consumption_l*velocity_mp))* (math.log(initial_weight/final_weight))
print(f"Loiter = {loiter_endurance} sec")
print(f"Range = {loiter_endurance/3600} hours")