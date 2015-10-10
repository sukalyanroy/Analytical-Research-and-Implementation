import math
import sqlite3
conn = sqlite3.connect('renewable.db') # create a "connection"
c = conn.cursor() # create a "cursor" 
c.execute("SELECT * FROM location;") # execute a SQL command


import pandas as pd;
pd.set_option('display.max_columns', None)


locations = pd.read_sql_query("SELECT * from location", conn)
port = pd.read_sql_query("SELECT * from ports", conn)
print locations
print port.head()
print len(locations.index)

def distance(lat_orig,long_orig,lat_dest,long_dest):

    radius = 6371 
    dlat = math.radians(lat_dest-lat_orig)
    dlon = math.radians(long_dest-long_orig)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat_orig)) \
        * math.cos(math.radians(lat_dest)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d
    
def charge(distance, production):
    
    charge = distance*production*0.001
    return charge


production_sum = sum(locations.production)
print production_sum

total_economic_cost = []
optimum_port_list=[]
for i in range (0,len(locations)):
    total_charge_port = []   
    total_charge_location = 0
    total_location = []

    for j in range(0,len(locations)):
        inter_location = distance(locations.lat[i],locations.long[i],locations.lat[j],locations.long[j])
        charge_inter_location = charge(inter_location, locations.production[j])
        total_charge_location += charge_inter_location

    
    for p in range (0, len(port)):
        inter_loc_port = distance(locations.lat[i],locations.long[i],port.lat[p],port.long[p])
        
        total_charge_port.append(charge(inter_loc_port, production_sum))
        
    total_charge_port_min = min(total_charge_port)
    optimum_port_list.append(total_charge_port.index(min(total_charge_port)))
    print optimum_port_list
    total_economic_cost.append(total_charge_location + total_charge_port_min)
    
    index_total_economic_cost = total_economic_cost.index(min(total_economic_cost))
    print index_total_economic_cost
  
print optimum_port_list[index_total_economic_cost]
    
print total_economic_cost
total_economic_cost_minimum = min(total_economic_cost)
print total_economic_cost_minimum
    
    
        
    
#print total_charge_port_min