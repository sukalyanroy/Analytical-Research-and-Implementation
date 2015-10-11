## The following lines imports the dependent packages required in the code.

import math
import sqlite3
import pandas as pd;

## The following lines interacts with the database renewable.db and store the 
## 2 tables (location and port) in pandas dataframe. Then it prints the 
## dataframes.

conn = sqlite3.connect('renewable.db') 
c = conn.cursor() 
locations = pd.read_sql_query("SELECT * from location", conn)
port = pd.read_sql_query("SELECT * from ports", conn)
print locations
print port


## The following function returns distance between two locations given the
## respective latitudes and longitudes.

def distance(lat_orig,long_orig,lat_dest,long_dest):

    radius = 6371 
    dlat = math.radians(lat_dest-lat_orig)
    dlon = math.radians(long_dest-long_orig)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat_orig)) \
        * math.cos(math.radians(lat_dest)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

## The following function calcultaes the charge of transporting raw materials 
## between two locations from the product of the distance between them, the 
## annual production and a factor (0.001) which is the charge per unit distance.
    
def charge(distance, production):
    
    charge = distance*production*0.001
    return charge


## production_sum = the sum of the annual production of raw materials from all
## locations.
## optimum_port_list = An empty list that will hold the best choice of port from
## every location. This will be represented by the index of the port in the 
## "port" table.
## total_economic_cost =  An empty list that will be used to store the sum of 
## the charge to transporting raw materials to a location from all the other 
## locations and cost to transfer all the material from that location to the 
## best choice of port.


total_economic_cost = []
optimum_port_list=[]
production_sum = sum(locations.production)

for i in range (0,len(locations)):
    total_charge_port = []   
    total_charge_location = 0
    total_location = []

# Calculates the cost of material transfer to all locations from all other locations

    for j in range(0,len(locations)): 
        
        inter_location = distance(locations.lat[i],locations.long[i],locations.lat[j],locations.long[j])
        charge_inter_location = charge(inter_location, locations.production[j])
        total_charge_location += charge_inter_location
    
# Calculates the distance of all 3 ports from all the locations and then 
# find out the charge to transfer all the raw material to the ports from the locations    
    
    for p in range (0, len(port)): 
        
        inter_loc_port = distance(locations.lat[i],locations.long[i],port.lat[p],port.long[p])        
        total_charge_port.append(charge(inter_loc_port, production_sum))
 

    
    total_charge_port_min = min(total_charge_port)   ## The charge for transferring materials to the best port choice from all the locations
    optimum_port_list.append(total_charge_port.index(min(total_charge_port)))   ## The index of the best port from every locations.
    total_economic_cost.append(total_charge_location + total_charge_port_min)   ## Appends the sum of total charge transferring all materials to a location and the charge of taking it the est port from that location
    index_total_economic_cost = total_economic_cost.index(min(total_economic_cost)) ## The index of the best location for the plant 

## The 2 print statements below prints the best choice of location and the port
## for the problem.

print "The best location for the plant is %d " %index_total_economic_cost  
print "The optimum location for port from the location is %d" %optimum_port_list[index_total_economic_cost]

    
## --------------- CODE ENDS ---------------------------##
    
