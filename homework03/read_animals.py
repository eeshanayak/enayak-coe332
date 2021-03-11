#!/usr/bin/env python3
import json
import random
import sys

def breed(parent1, parent2):
    
    child = {'head':parent1['head'], 'body':parent2['body'], 'arms':parent1['arms'], 
	     'legs':parent2['legs'], 'tail':parent1['arms'] + parent2['legs']}

    return child


def main():

    with open(sys.argv[1], 'r') as f:
        animal_dict = json.load(f)

    parent1 = random.choice(animal_dict['animals'])
    parent2 = random.choice(animal_dict['animals'])

    child = breed(parent1, parent2)

    print('Parent 1: ' , parent1, '\nParent 2: ' , parent2 , '\nChild: ', child)

if __name__ == '__main__':
    main()
