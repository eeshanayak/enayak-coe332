import json
import datetime
from flask import Flask, request
import redis
import random
import petname
import datetime
import uuid


rd = redis.StrictRedis(host='redis', port=6379, db=0)
app = Flask(__name__)

def get_data():
    userdata = json.loads(rd.get('animals').decode('utf-8'))
    return userdata

@app.route('/helloworld', methods = ['GET'])
def hello_world():
    return 'hello world'

@app.route('/update', methods=['GET'])
def update():
    uuid = request.args.get('uuid')
    animals = get_data()

    head = request.args.get('head')
    body = request.args.get('body')
    arms = request.args.get('arms')
    legs = request.args.get('legs')
    tails = request.args.get('tails')

    for x in animals['animals']:
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
    

    rd.set('animals', json.dumps(animals))
    return str(uuid + 'has been updated')


@app.route('/generate', methods=['GET'])
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
  
    rd.set('animals', json.dumps(animal_dict))

    return '20 animals have been generated'

@app.route('/animals', methods=['GET'])
def get_animals():
    return json.dumps(get_data())

@app.route('/select', methods=['GET'])
def get_uuid():
    uuid = request.args.get('uuid')
    animals = get_data()
   
    for x in animals['animals']:
       if(x['uuid'] == uuid):
           return x

    return 'No animals with given uuid'

@app.route('/avg_legs', methods=['GET'])
def get_avg_legs():
    animals = get_data()    

    legs = 0
    for x in animals['animals']:
        legs += x['legs']

    return str(legs / len(animals['animals']))

@app.route('/total_count', methods=['GET'])
def get_total():   
    animals = get_data()
    total_animals = len(animals['animals'])

    return str(total_animals)

@app.route('/dates', methods=['GET'])
def query_dates():
    start = request.args.get('start')
    end = request.args.get('end')

    startdate = datetime.datetime.strptime(start, '%Y-%m-%d_%H:%M:%S.%f')
    enddate = datetime.datetime.strptime(end, '%Y-%m-%d_%H:%M:%S.%f')

    animals = get_data()
   
    date_query = []

    for x in animals['animals']:
        created_on = datetime.datetime.strptime(x['created_on'], '%Y-%m-%d %H:%M:%S.%f')

        if(created_on > startdate and created_on < enddate):
            date_query.append(x)

    return str(date_query)


@app.route('/delete', methods=['GET'])
def delete():
    start = request.args.get('start')
    end = request.args.get('end')
    
    startdate = datetime.datetime.strptime(start, '%Y-%m-%d_%H:%M:%S.%f')
    enddate = datetime.datetime.strptime(end, '%Y-%m-%d_%H:%M:%S.%f')

    animals = get_data()
   
    for x in animals['animals']:
        created_on = datetime.datetime.strptime(x['created_on'], '%Y-%m-%d %H:%M:%S.%f')
        if(created_on > startdate or created_on < enddate):
            animals['animals'].remove(x)

    rd.set('animals', json.dumps(animals))

    return 'Animals created between ' + start + ' and ' + end + ' have been deleted'


@app.route('/reset', methods=['GET'])
def reset():
    rd.flushall()

    return 'Database is reset'


if __name__ == '__main__':
    rd = redis.StrictRedis(host='redis', port=6379, db=0)
    app.run(debug=True, host='0.0.0.0', port=5000)
