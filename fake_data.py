from faker import Faker
import json
import pandas as pd
import random_time
import random
import sys

fake = Faker('de_DE')

# import of real addresses from cologne including location
df = pd.read_csv('Adressenverzeichnis_Koeln.csv')
df = df[['Adresse', 'X-Koordinate', 'Y-Koordinate']]
# write addresses in a dictionary (key=address, values = X and Y)
address_dict = df.set_index('Adresse')[['X-Koordinate', 'Y-Koordinate']].T.to_dict('list')



# function that produces a list of dictionaries filled with a fake name, a real cologne address and a fake date
def simulate_user_input(n):
    sundays, probabilities, _ = random_time.next_4_saturdays()     # import the sundays and their probabilities (upcoming_sunday (_) is not needed here but in main.py)
    fake_data_list = []                 # in the end this will be the list of dictionaries
    loop_counter = 0                
    for _ in range(n):
        random_row = df.sample(1).iloc[0]    # Take randomly 1 address out of the df
        fake_name = fake.name()              # define a fake name
        titles = ['Dr.', 'Prof.', 'B.Eng.', 'Univ.', 'B.Sc.', 'MBA.', 'B.A.', 'Dipl.-', 'Ing.', 'Frau ', 'Herr ']
        for title in titles:                    # iterate through titles to find and than remove them
            if title in fake_name:
                fake_name = fake_name.replace(title, '').strip()
        fake_data_dictionary = {
            "name": fake_name,
            "address": random_row['Adresse'],
            "date": random.choices(sundays, weights=probabilities, k=1)[0]       # choose one of the next sundays according to the probabilities
            }
        fake_data_list.append(fake_data_dictionary)     # fill list with a new dictionary each loop
        loop_counter += 1                   
        if loop_counter >= n:                           # if loop counter reaches n return the list
            return fake_data_list       # return the list, if it reaches n loops
    return fake_data_list               # return back the list, if it runs all entries of df['Adresse']    
    


