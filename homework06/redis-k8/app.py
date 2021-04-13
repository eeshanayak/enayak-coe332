import json
import datetime
from flask import Flask, request
import redis
import random
import petname
import datetime
import uuid


rd = redis.StrictRedis(host='10.106.219.157', port=6379, db=0)
app = Flask(__name__)

@app.route('/helloworld', methods = ['GET'])
def hello_world():
    return 'hello world'

@app.route('/update', methods=['GET'])
def update():
    uuid = request.args.get('uuid')
  
    head = request.args.get('head')
    body = request.args.get('body')
    arms = request.args.get('arms')
    legs = request.args.get('legs')
    tails = request.args.get('tails')

    if head is not None:
        rd.hset(uuid, 'head', head)
    if body is not None:
        rd.hser(uuid, 'body', body)
    if arms is not None:
        rd.hset(uuid, 'arms', arms)
    if legs is not None:
        rd.hset(uuid, 'legs', legs)
    if tails is not None:
        rd.hset(uuid, 'tails', tails)    

    return str(uuid + 'has been updated')


@app.route('/generate', methods=['GET'])
def generate():
     
    for i in range(20):
        this_animal = {}
        this_animal['head'] = random.choice(['snake', 'bull', 'lion', 'raven', 'bunny'])
        this_animal['body'] = petname.name() + '-' + petname.name()
        this_animal['arms'] = random.randint(1,5) * 2
        this_animal['legs'] = random.randint(1,4) * 3
        this_animal['tail'] = this_animal['legs'] + this_animal['arms']
        this_animal['created_on'] = str(datetime.datetime.now())
 
        rd.hmset(str(uuid.uuid4()), this_animal)
  
    return '20 animals have been generated'

@app.route('/animals', methods=['GET'])
def get_animals():
    animals = []
    keys = rd.keys()

    for key in keys:
        animals.append(rd.hgetall(key))
    
    return str(animals)

@app.route('/select', methods=['GET'])
def get_uuid():
    uuid = request.args.get('uuid')
    return rd.hgetall(uuid)

    return 'No animals with given uuid'

@app.route('/avg_legs', methods=['GET'])
def get_avg_legs():
    keys = rd.keys()
    legs = 0

    for key in keys:
        legs += int(rd.hget(key, 'legs'))

    return str(legs / rd.dbsize())

@app.route('/total_count', methods=['GET'])
def get_total():   
    return str(rd.dbsize())

@app.route('/dates', methods=['GET'])
def query_dates():
    start = request.args.get('start')
    end = request.args.get('end')

    startdate = datetime.datetime.strptime(start, '%Y-%m-%d_%H:%M:%S.%f')
    enddate = datetime.datetime.strptime(end, '%Y-%m-%d_%H:%M:%S.%f')

    date_query = []

    keys = rd.keys()

    for key in keys:
        created_on = datetime.datetime.strptime(rd.hget(key, 'created_on'), '%Y-%m-%d %H:%M:%S.%f')

        if(created_on > startdate and created_on < enddate):
            date_query.append(rd.hgetall(key))

    return str(date_query)


@app.route('/delete', methods=['GET'])
def delete():
    start = request.args.get('start')
    end = request.args.get('end')
    
    startdate = datetime.datetime.strptime(start, '%Y-%m-%d_%H:%M:%S.%f')
    enddate = datetime.datetime.strptime(end, '%Y-%m-%d_%H:%M:%S.%f')

    keys = rd.keys()   

    for key in keys:
        created_on = datetime.datetime.strptime(rd.hget(key, 'created_on'), '%Y-%m-%d %H:%M:%S.%f')
        if(created_on > startdate or created_on < enddate):
            rd.delete(key)

    return 'Animals created between ' + start + ' and ' + end + ' have been deleted'


@app.route('/reset', methods=['GET'])
def reset():
    rd.flushall()
    return 'Database is reset'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
