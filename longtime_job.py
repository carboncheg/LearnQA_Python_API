import requests
import time

# Creates a task
response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
token = response.json()['token']
seconds = response.json()['seconds']
print(response.text)

# Sends a request with a token before the task is completed and print the status
response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={"token": token})
print(response.json()['status'])

# Waits {seconds} seconds
time.sleep(seconds)

# Sends a request with a token after the task is completed and print the status and result
response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={"token": token})
print(response.json()['status'])
print(f"Result: {response.json()['result']}")
