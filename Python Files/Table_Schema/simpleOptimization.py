import math
import pulp
from getBatteryDetails import batteryDetails, BatteryDetails
from getBatteryHeader import batteryHeader
from getErcotDAPrices import ercotDAPrices 
from processOutput import outputProcessor
from datetime import datetime

BATTERY_ID = 1
DELIVERY_DATE    = "3/12/2026"
SETTLEMENT_POINT = "HB_HOUSTON"

#Create batteryHeader object
batteryHead = batteryHeader()
#Call the getBatteryHeader and pass BATTERY_ID, it returns a sequence of BatteryHeader Objects
batHeadSeq = batteryHead.getBatteryHeader(BATTERY_ID)
#Assign the first object in the sequence to the variable batteryHeader
batteryHeader = batHeadSeq[0]
print(batteryHeader.battery_id)
#Create batteryDetails object
batteryDet = batteryDetails()
#Call the getBatteryDetails and pass BATTERY_ID, it returns a sequence of BatteryDetails Objects
batDetSeq = batteryDet.getBatteryDetails(BATTERY_ID)
#Assign the first object in the sequence to the variable batteryDetails
batteryDetails = batDetSeq[0]
#Print out the capacity_kwh hours attribute of the assigned object
print(batteryDetails.capacity_kwh)

capacity          = batteryDetails.capacity_kwh
max_charge_kw     = batteryDetails.max_charge_kw
max_discharge_kw  = batteryDetails.max_discharge_kw
charge_efficiency = math.sqrt(batteryDetails.round_trip_efficiency)
discharge_efficiency = math.sqrt(batteryDetails.round_trip_efficiency)
min_soc           = batteryDetails.min_soc_pct * capacity
max_soc           = batteryDetails.max_soc_pct * capacity
initial_soc       = batteryDetails.soc_initial
degradation_cost  = batteryDetails.cycle_cost / capacity
cycle_limit       = batteryDetails.cycle_limit

daPrices = ercotDAPrices()

price_rows = (
    daPrices.getDAPrices(DELIVERY_DATE, SETTLEMENT_POINT)
)

print(price_rows)
#print(price_rows[0]["settlement_point_price"])

price_per_kwh = {t: float(r["settlement_point_price"]) / 1000.0 for t, r in enumerate(price_rows)}
hours = range(len(price_rows))

charge_kw    = {t: pulp.LpVariable(f"charge_kw_{t}",    lowBound=0, upBound=max_charge_kw)    for t in hours}
discharge_kw = {t: pulp.LpVariable(f"discharge_kw_{t}", lowBound=0, upBound=max_discharge_kw) for t in hours}
state_of_charge = {t: pulp.LpVariable(f"soc_{t}", lowBound=min_soc, upBound=max_soc)          for t in hours}
is_charging  = {t: pulp.LpVariable(f"is_charging_{t}", cat="Binary")                          for t in hours}

prob = pulp.LpProblem("battery_dispatch", pulp.LpMaximize)
prob += pulp.lpSum(
    discharge_kw[t] * discharge_efficiency * price_per_kwh[t]
    - charge_kw[t] * price_per_kwh[t]
    - (charge_kw[t] * charge_efficiency + discharge_kw[t]) * degradation_cost
    for t in hours
)

prob += state_of_charge[0] == initial_soc + charge_kw[0] * charge_efficiency - discharge_kw[0]
for t in hours:
    prob += charge_kw[t]    <= max_charge_kw    * is_charging[t]
    prob += discharge_kw[t] <= max_discharge_kw * (1 - is_charging[t])
    if t > 0:
        prob += state_of_charge[t] == state_of_charge[t - 1] + charge_kw[t] * charge_efficiency - discharge_kw[t]

prob += pulp.lpSum(discharge_kw[t] for t in hours) <= cycle_limit * capacity

prob.solve(pulp.PULP_CBC_CMD(msg=0))

print(f"\nBattery: {batteryHeader.name}  |  Date: {DELIVERY_DATE}")
print(f"{'Hour':<6} {'Action':<11} {'Charge kW':>10} {'Discharge kW':>13} {'SoC kWh':>10} {'Price $/MWh':>12} {'Revenue $':>10}")
print("-" * 78)

#Print data out
total_revenue = 0.0
for t in hours:
    ch  = pulp.value(charge_kw[t])      or 0.0
    dis = pulp.value(discharge_kw[t])   or 0.0
    soc = pulp.value(state_of_charge[t]) or 0.0
    price_mwh = float(price_rows[t]["settlement_point_price"]) / 1000.0

    if ch > 0.01:
        action = "charge"
    elif dis > 0.01:
        action = "discharge"
    else:
        action = "hold"

    revenue = (
        dis * discharge_efficiency * price_per_kwh[t]
        - ch * price_per_kwh[t]
        - (ch * charge_efficiency + dis) * degradation_cost
    )
    total_revenue += revenue
    
    print(f"{t+1:<6} {action:<11} {ch:>10.1f} {dis:>13.1f} {soc:>10.1f} {price_mwh:>12.2f} {revenue:>10.2f}")

print("-" * 78)
print(f"{'Total Revenue':>66}  {total_revenue:>10.2f}")

#Load data into SQLite database
schedule = []
for t in hours:
    ch  = pulp.value(charge_kw[t])       or 0.0
    dis = pulp.value(discharge_kw[t])    or 0.0
    soc = pulp.value(state_of_charge[t]) or 0.0
    price_mwh = float(price_rows[t]["settlement_point_price"])

    if ch > 0.01:
        action = "charge"
    elif dis > 0.01:
        action = "discharge"
    else:
        action = "hold"

    revenue = (
        dis * discharge_efficiency * price_per_kwh[t]
        - ch * price_per_kwh[t]
        - (ch * charge_efficiency + dis) * degradation_cost
    )

    schedule.append({
        'hour':         t + 1,
        'action':       action,
        'charge_kw':    ch,
        'discharge_kw': dis,
        'soc_kw':       soc,
        'price_mwh':    price_mwh,
        'revenue':      revenue
    })

loadOutput = outputProcessor()
output_id = loadOutput.saveOutputHeader(BATTERY_ID, DELIVERY_DATE,"SO")
#output_id = loadOutput.saveOutputHeader(BATTERY_ID, datetime.strptime(DELIVERY_DATE, "%m/%d/%Y").date(),"SO")
loadOutput.saveOutputDetails(output_id, schedule)