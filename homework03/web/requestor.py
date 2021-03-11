import requests

response = requests.get(url='http://localhost:5021/animals')
response_bunny = requests.get(url='http://localhost:5021/animals/head/bunny')
response_legs_6 = requests.get(url='http://localhost:5021/animals/legs/6')
repsonse_arms_2 = requests.get(url='http://localhost:5021/animals/arms/2')


print(response.json())
print(response_bunny.json())
print(response_legs_6)
print(response_arms_2)
print(response.status_code)
print(response.headers)
