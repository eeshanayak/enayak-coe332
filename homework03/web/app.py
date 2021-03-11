import json
from flask import Flask

app = Flask(__name__)

def get_data():
    with open("animals.json", "r") as json_file:
        userdata = json.load(json_file)
    return userdata


test = get_data()
jsonList = test['animals']

@app.route('/animals', methods=['GET'])
def get_animals():
    return json.dumps(get_data())

@app.route('/animals/head/bunny', methods=['GET'])
def get_bunny():
    result = [x for x in jsonList if x['head'] == 'bunny']
    response = {}
    response['output'] = result
    return response  

@app.route('/animals/legs/6', methods=['GET'])
def get_legs_6():
    result = [x for x in jsonList if x['legs'] == 6]
    response = {}
    response['output'] = result
    return response


@app.route('/animals/arms/2', methods=['GET'])
def get_arms_2():
    result = [x for x in jsonList if ['arms'] == 2]
    response = {}
    response['output'] = result
    return response



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
