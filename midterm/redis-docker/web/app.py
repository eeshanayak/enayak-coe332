import json
import datetime
from flask import Flask, request
import redis

app = Flask(__name__)

def get_data():
    #with open("animals.json", "r") as json_file:
     #   userdata = json.load(json_file)
 
    userdata = json.loads(rd.get('animals').decode('utf-8'))
    return userdata


# test = get_data()
# jsonList = test['animals']

@app.py('/update', methods=['GET'])
def update():
    uuid = request.args.get('uuid')
    animals = get_data()
    animals_list = animals['animals']

    head = request.args.get('head')
    body = request.args.get('body')
    arms = request.args.get('arms')
    legs = request.args.get('legs')
    tails = request.args.get('tails')

    for x in animals_list:
        if(x['uuid'] == uuid):
            if head is not None:
                x['head'] = head
            if body is not None:
                x['body'] = body
            if arms is not None:
                x['arms'] = arms
            if legs is not None:
                x['legs'] = legs
            if head is not None:
                x['tails'] = tails
    
     rd.set('animals', json.dumps(animals_list))

@app.py('/generate', methods=['GET'])
def generate():
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
  
    rd.set('animals', json.dumps(animal_dict, indent=2))

    return '20 animals have been generated'

@app.route('/animals', methods=['GET'])
def get_animals():
    return json.dumps(get_data())

@app.route('/select', methods=['GET'])
def get_uuid():
    uuid = request.args.get('uuid')
    animals = get_data()
    animals_list = animals['animals']

    for x in animals_list:
       if(x['uuid'] == uuid):
           return x 

    return 'No animals with given uuid'

@app.route('/avg_legs', methods=['GET'])
def get_avg_legs():
    animals = get_data()
    animals_list = animals['animals']

    legs = 0
    for x in animals_list:
        legs += x['legs']

    return str(legs / len(animals_list))

@app.route('/total_count', methods=['GET'])
def get_total():   
    animals = get_data()
    total_animals = len(animals['animals'])

    return str(total_animals)

@app.route('dates', methods=['GET'])
def query_dates():
    start = request.args.get('start')
    end = request.args.get('end')

    startdate = datetime.datetime.strptime(start, "'%Y-%m-%d_%H:%M:%S.%f'")
    enddate = datetime.datetime.strptime(end, "'%Y-%m-%d_%H:%M:%S.%f'")

    animals = get_data()
    animals_list = animals['animals']
 
    animal_dates = []

    for x in animals_list:
        if(x['created_on'] > startdate and x['created_on'] < enddate):
            animals_list.append(x)

    return animals_list


@app.route('/delete', methods=['GET'])
def delete():
    start = request.args.get('start')
    end = request.args.get('end')
    
    startdate = datetime.datetime.strptime(start, "'%Y-%m-%d_%H:%M:%S.%f'")
    enddate = datetime.datetime.strptime(end, "'%Y-%m-%d_%H:%M:%S.%f'")

    animals = get_data()
    animals_list = animals['animals']

    for x in animals_list:
        if(x['created_on'] < startdate or x['created_on'] > enddate)
            animals_list.remove(x)

    rd.set('animals', json.dumps(animals_list))


if __name__ == '__main__':
    rd = redis.StrictRedis(host='redis', port=6379, db=0)
    app.run(debug=True, host='0.0.0.0', port=5021)
