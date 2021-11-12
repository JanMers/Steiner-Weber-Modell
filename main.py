import pandas as pd
import math

data = pd.read_csv("customer_data.csv")

print(data)

def get_start_coord(coord, data):
    counter_values=[row[coord]*row['demand'] for index, row in data.iterrows()]

    denom_values=[row['demand'] for index, row in data.iterrows()]

    return round(sum(counter_values)/sum(denom_values), 3)

def calc_target_value(x, y, data):
    distances=[math.sqrt(((row['x']-x)**2 + (row['y']-y)**2))*row['demand'] for index, row in data.iterrows()]

    return round(sum(distances), 3)

def check_criteria(x_1, y_1, x_2, y_2, alpha):
    #probably unneccesary
    if abs(x_2 - x_1) <= alpha and abs(y_2 - y_1) <= alpha:
        return True
    else:
        return False

def calc_new_coord(x, y, data):
    dist = [math.sqrt((row['x']-x)**2 + (row['y']-y)**2) for index, row in data.iterrows()]

    counter_x = [row['x']*row['demand'] for index, row in data.iterrows()]

    denom = [row['demand'] for index, row in data.iterrows()]

    counter_y = [row['y']*row['demand'] for index, row in data.iterrows()]

    x_new = (sum(counter_x)/sum(dist))/(sum(denom)/sum(dist))

    y_new = (sum(counter_y)/sum(dist))/(sum(denom)/sum(dist))

    print("new x: " + str(x_new))
    print("new y: " + str(y_new))

alpha = 0.001

x_0 = get_start_coord('x', data)
y_0 = get_start_coord('y', data)

calc_new_coord(x_0, y_0, data)

distance = calc_target_value(x_0, y_0, data)



