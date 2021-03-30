#!/usr/bin/env python3
import json
import petname
import random
import sys
import datetime
import uuid
import redis

def main():

    animal_dict = {}
    animal_dict['animals'] = []

    for i in range(20):
        this_animal = {}
        this_animal['head'] = random.choice(['snake', 'bull', 'lion', 'raven', 'bunny'])
        this_animal['body'] = petname.name() + '-' + petname.name()
        this_animal['arms'] = random.randint(1,5) * 2
        this_animal['legs'] = random.randint(1,4) * 3
        this_animal['tail'] = this_animal['legs'] + this_animal['arms']
        this_animal['created_on'] = str(datetime.datetime.now())
        this_animal['uuid'] = str(uuid.uuid4())        

        animal_dict['animals'].append(this_animal)

       
    rd = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    rd.set('animals', json.dumps(animal_dict, indent=2))

if __name__ == '__main__':
    main()
