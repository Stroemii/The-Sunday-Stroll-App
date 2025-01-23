import time
import fake_data
import pandas as pd
import random_time
import numpy as np
from itertools import combinations

# import data from fake data script
data = fake_data.simulate_user_input(101)
df = pd.DataFrame(data)

# create a function that pulls the coordinates to a given address
def get_coordinates(address):
    return fake_data.address_dict.get(address, [None, None])  # Gibt [None, None] zurück, wenn die Adresse nicht gefunden wird

# add the coordinates to the df
df[['x-coordinate', 'y-coordinate']] = df['address'].apply(get_coordinates).apply(pd.Series)

# here we only need upcoming sunday (we want to filter our dataframe on the people who have chosen the upcoming sunday)
_, _, upcoming_sunday = random_time.next_4_saturdays()

# filter on the participants who have chosen the upcoming sunday to take a sunday stroll
df_upcoming_sunday = df[df['date'] == upcoming_sunday]


# function to calculate the distance between coord1 and coord2
def calculate_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# write all possible combinations of index entries in a list (if [1, 2, 3] is given than [(1, 2), (1, 3), (2, 3)] is the output)
name_combinations = list(combinations(df_upcoming_sunday.index, 2))

# create a list where we can save all distances
distances = []

# for each combination calculate the distance between the two coordinates and append it and the names of the two persons to the created list
for (i, j) in name_combinations:
    dist = calculate_distance((df_upcoming_sunday.loc[i, 'x-coordinate'], df_upcoming_sunday.loc[i, 'y-coordinate']),
                              (df_upcoming_sunday.loc[j, 'x-coordinate'], df_upcoming_sunday.loc[j, 'y-coordinate']))
    distances.append((df_upcoming_sunday.loc[i, 'name'], df_upcoming_sunday.loc[j, 'name'], dist))

# Sort the couples by distance
distances.sort(key=lambda x: x[2])

# create pairs so that each person is assigned only once.
paired_indices = set()      # A set for storing the indices that have already been used in a pair. This set is used to avoid duplicates and to speed up the search for previously used indices.
pairs = []                  # save couples and distances
total_distance = 0          # save total distance


# This line identifies and stores all names from df_upcoming_sunday that are not included in the list 'pairs', and saves them in the variable unpaired_names (necessary when the amount of participants is odd).
unpaired_names = df_upcoming_sunday[~df_upcoming_sunday['name'].isin([name for name1, name2, distance in pairs for name in (name1, name2)])]

# if unpaired_names is not empty then store the name into a list
pairs_without_partner = []
if not unpaired_names.empty:
    pairs_without_partner.append(unpaired_names.iloc[0]['name'])
    print(f"Sorry, our algorithm could not find a pair for this person: {unpaired_names.iloc[0]['name']}")


# the following algorithm runs through the list 'distance' and searches the indices of the matching names in df_upcoming_sunday
for name1, name2, distance in distances:
    index1 = df_upcoming_sunday[df_upcoming_sunday['name'] == name1].index[0]
    index2 = df_upcoming_sunday[df_upcoming_sunday['name'] == name2].index[0]

# if both indices aren´t yet saved in 'paired_indices' it will be added to the list 'pairs'
# 'paired_indices' and total distance will be updated
    if index1 not in paired_indices and index2 not in paired_indices:
        pairs.append((name1, name2, distance))
        paired_indices.add(index1)
        paired_indices.add(index2)
        total_distance += distance

# all couples with their distances to each other will be printed
for name1, name2, distance in pairs:
    print(f"Pair: {name1} & {name2}, Distance: {distance:.2f}")

# calculate and print the average distance
if pairs:
    average_distance = total_distance / len(pairs)
    print(f"Average Distance: {average_distance:.2f}")
else:
    print("No pairs were formed.")



# measure execution time:
# start_time = time.time()  # Zeit zu Beginn erfassen
# end_time = time.time()  # Zeit nach der Ausführung erfassen
# execution_time = end_time - start_time  # Berechne die Laufzeit
# print(f"Die Ausführung dauerte {execution_time} Sekunden.")

### Wie geht´s weiter?
### der Algorithmus muss nochmal so angepasst werden, dass Ausreißer geglättet werden
### Was passiert bei einer ungeraden Anzahl an Teilnehmern?
### Was mach ich jetzt mit der Ausgabe?
### Die Information muss an die User zurückgespielt werden. Wie kann ich das machen? Mit einer User-ID?