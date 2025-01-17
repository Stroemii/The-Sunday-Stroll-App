import time
import fake_data
import pandas as pd
import random_time
import numpy as np
from itertools import combinations

data = fake_data.simulate_user_input(100)
df = pd.DataFrame(data)

def get_coordinates(address):
    return fake_data.address_dict.get(address, [None, None])  # Gibt [None, None] zurück, wenn die Adresse nicht gefunden wird

# Koordinaten hinzufügen
df[['x-coordinate', 'y-coordinate']] = df['address'].apply(get_coordinates).apply(pd.Series)

# here we only need upcoming sunday (we want to filter our dataframe on the people who chose the upcoming sunday)
_, _, upcoming_sunday = random_time.next_4_saturdays()

# filter on the participants who chose the upcoming sunday to take a sunday stroll
df_upcoming_sunday = df[df['date'] == upcoming_sunday]
print(df_upcoming_sunday)


# Funktion zur Berechnung der Distanz zwischen zwei Punkten
def calculate_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord1[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# Alle Kombinationen von Namen
name_combinations = list(combinations(df_upcoming_sunday.index, 2))

# Distanzen speichern
distances = []

for (i, j) in name_combinations:
    dist = calculate_distance((df_upcoming_sunday.loc[i, 'x-coordinate'], df_upcoming_sunday.loc[i, 'y-coordinate']),
                              (df_upcoming_sunday.loc[j, 'x-coordinate'], df_upcoming_sunday.loc[j, 'y-coordinate']))
    distances.append((df_upcoming_sunday.loc[i, 'name'], df_upcoming_sunday.loc[j, 'name'], dist))

# Sortiere die Paare nach Distanz
distances.sort(key=lambda x: x[2])

# Paare erstellen, sodass jede Person nur einmal zugeordnet wird
paired_indices = set()
pairs = []
total_distance = 0  # Variable zur Speicherung der Gesamtdistanz

for name1, name2, distance in distances:
    index1 = df_upcoming_sunday[df_upcoming_sunday['name'] == name1].index[0]
    index2 = df_upcoming_sunday[df_upcoming_sunday['name'] == name2].index[0]
    
    if index1 not in paired_indices and index2 not in paired_indices:
        pairs.append((name1, name2, distance))
        paired_indices.add(index1)
        paired_indices.add(index2)
        total_distance += distance  # Gesamtdistanz aktualisieren

# Ausgabe der Paare mit minimaler Distanz
for name1, name2, distance in pairs:
    print(f"Pair: {name1} & {name2}, Distance: {distance:.2f}")

# Berechnung der durchschnittlichen Distanz
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
### Der Algorithmus muss beschriftet werden
### der Algorithmus muss nochmal so angepasst werden, dass Ausreißer geglättet werden
### Was mach ich jetzt mit der Ausgabe?
### Die Information muss an die User zurückgespielt werden. Wie kann ich das machen? Mit einer User-ID?