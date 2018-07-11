import random
import pandas as pd
import numpy as np
import geopy.distance


# Formulating a way to calculate distances


def distance_between(x, i):  # creates a list of distances of location i from all other locations in list x
    dist_from_pt = []
    for j in range(len(x)):
        dist_from_pt.append(geopy.distance.vincenty(i, x[j]).km)
    return dist_from_pt


def distance_thresh_greater(x, thresh):  # pass the list of distances here. Comes out with a list which says true for points which surpass the thresh
    distance_true = []
    for i in range(len(x)):
        distance_true.append(x[i] > thresh)
    return distance_true


# The next function passes the list of distances here. Comes out with a list which says true for points which are less than the thresh

def distance_thresh_lesser(x, thresh):
    distance_true = []
    for i in range(len(x)):
        distance_true.append(x[i] < thresh)
    return distance_true


def task_gen(x, thresh, n_tasks_greater, n_tasks_lesser):
    task_list = [x.pop(random.randint(0, len(x) - 1))]
    while len(task_list) < n_tasks_lesser:
        i = 1
        list_sub = random.randint(0, len(x) - 1)
        task = x[list_sub]
        distances_from_task = distance_between(task_list, task)
        dist_thresh = distance_thresh_lesser(distances_from_task, thresh)
        if True in dist_thresh:
            task_list.append(x.pop(list_sub))
        if i == 1000:
            break
        i += 1
    while len(task_list) < n_tasks_greater + n_tasks_lesser:
        i = 1
        list_sub = random.randint(0, len(x) - 1)
        task = x[list_sub]  # removing one obs from loc_list
        distances_from_task = distance_between(task_list, task)
        dist_thresh = distance_thresh_greater(distances_from_task, thresh)
        if False in dist_thresh:
            pass
        else:
            task_list.append(x.pop(list_sub))
        if i == 1000:
            break
        i += 1

    task_data = pd.DataFrame({'Task Coordinates': task_list,
                              'Dist Greater Than Threshold': (([False] * n_tasks_lesser) +
                                                              ([True] * n_tasks_greater))})
    return task_data

# User input and results


path = input("Please copy paste the path to the task csv file (format C:\\Windows... or C:/Windows): \n")
export = input("Please input directory where you want you table saved. Include the name of the csv. \nFor example C:\\..\\Documents\\final.csv \n")
threshold = input("What is the threshold distance \n ")
n_greater = input("How many tasks should be greater than the threshold \n")
n_lesser = input("How many tasks should be lesser than the threshold \n")


# Importing tasks
tasks = pd.read_csv(str(path))
loc_list = list(zip(tasks.iloc[:, 0], tasks.iloc[:, 1]))

task_list = task_gen(loc_list, int(threshold), int(n_greater), int(n_greater))

print(task_list)
print("Number of tasks generated: " + str(len(task_list)))

task_list.to_csv(str(export))
print('Table exported to same directory as input csv directory')

dist_matrix_inp = input("Do you want to generate a distance matrix? (y/n)\n")

if dist_matrix_inp == 'y':
    dist_matrix_path = input('Please give the path to where you want to save the distance matrix. Include the final file name \n')

    coordinates = list(task_list.iloc[:, 1])

    distance_matrix_final = []

    for i in range(len(coordinates)):
        distance_matrix = []
        coordinate_i = coordinates[i]
        for j in range(len(coordinates)):
            dist = geopy.distance.vincenty(coordinate_i, coordinates[j]).km
            distance_matrix.append(dist)
        distance_matrix_final.append(distance_matrix)

    dist_matr = pd.DataFrame(distance_matrix_final, index=coordinates, columns=coordinates)
    dist_matr.to_csv(str(dist_matrix_path))
    print('Distance matrix exported to same directory as input csv directory')


input('Press any button to exit')
