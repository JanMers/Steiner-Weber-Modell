import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import threading

data = pd.read_csv("customer_data.csv")

print("Input data set:\n" + str(data))

global solution_list
solution_list = [[0,0]]

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
    x_counter = [(row['x']*row['demand'])/(math.sqrt((row['x']-x)**2 + (row['y']-y)**2)) for index, row in data.iterrows()]

    y_counter = [(row['y']*row['demand'])/(math.sqrt((row['x']-x)**2 + (row['y']-y)**2)) for index, row in data.iterrows()]

    denominator = [row['demand']/(math.sqrt((row['x']-x)**2 + (row['y']-y)**2)) for index, row in data.iterrows()]

    x_new = round(sum(x_counter)/sum(denominator), 3)

    y_new = round(sum(y_counter)/sum(denominator), 3)

    new_coord = [x_new, y_new]

    return new_coord

def start_iteration(data):

    #start parameters for stop criteria
    #difference must be larger than alpha
    difference = 100
    alpha = 0.001


    x_0 = get_start_coord('x', data)
    y_0 = get_start_coord('y', data)

    old_coord = [x_0, y_0]
    iter_count = 1

    while difference >= alpha :
        time.sleep(1)
        new_coord = calc_new_coord(old_coord[0], old_coord[1], data)

        x_diff = abs(new_coord[0] - old_coord[0])
        y_diff = abs(new_coord[1] - old_coord[1])

        difference = max(x_diff, y_diff)

        print("Iteration " + str(iter_count) + " with x,y= " +str(new_coord) + " and target value= " + str(calc_target_value(new_coord[0], new_coord[1], data)))
        iter_count += 1

        #putting solution to queue
        solution_list.append(new_coord)

        old_coord = new_coord

    print("Stop criteria reached.")

def plot_data(data):
    fig = plt.figure()
    global ax
    ax = fig.add_subplot(111)

    ani = animation.FuncAnimation(fig, animate, interval=100)

    plt.show()

def animate(i):
    ax.clear()
    ax.scatter(data['x'], data['y'])

    for index, row in data.iterrows():
        ax.annotate(' d=' + str(row['demand']), (row['x'], row['y']))

    coordinates = solution_list[-1]

    ax.scatter(coordinates[0], coordinates[1], c="r")
    ax.annotate(len(solution_list)-1, (coordinates[0], coordinates[1]))

def start_threads(data):

    t1 = threading.Thread(target=start_iteration, args=(data,))
    t1.start()

    t2 = threading.Thread(target=plot_data, args=(data,))
    t2.start()

start_threads(data)
