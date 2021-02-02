import json
import random
import petname

data = {}

# initialize empty list for all animals (will be populated by dictionaies)
all_animals = []

# create list of options for head attribute
head_list = ["snake", "bull", "lion", "raven", "bunny"]

for x in range (20):
    # initialize animal dict
    animal = {}

    # populate animal dict based on criteria  
    animal["head"] = random.choice(head_list)
    animal["body"] = f"{petname.name()}-{petname.name()}"
    animal["arms"] = random.randrange(2, 11, 2)
    animal["legs"] = random.randrange(3, 13, 3)
    animal["tails"] = animal["arms"] + animal["legs"] 
    all_animals.append(animal)

data["animals"] = all_animals

# dump the animals list into a json
with open('animals.json', 'w') as out:
    json.dump(data, out, indent = 2)



