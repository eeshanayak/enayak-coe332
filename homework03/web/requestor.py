import requests

response = requests.get(url='http://localhost:5021/animals')

response2 = requests.get(url='http://localhost:5021/animals/head/bunny')

print(response2)
print(response.status_code)
print(response.json())
print(response.headers)
