import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

response_1 = requests.get(url)
print(f'1. {response_1.text}')

response_2 = requests.head(url)
print(f'2. {response_2.text}')

response_3 = requests.get(url, params={"method": "GET"})
print(f'3. {response_3.text}')

print("4. Results:")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
for req_method in methods:
    for params_method in methods:
        if req_method == "GET":
            response = requests.request(method=req_method, url=url, params={"method": params_method})
        else:
            response = requests.request(method=req_method, url=url, data={"method": params_method})

        if req_method == params_method and response.text != response_3.text:
            print(f"\tBug in request method {req_method} and params/data method {params_method}")
            print(f"\tExpected: {response_3.text}")
            print(f"\tReceived: {response_1.text}", end="\n\n")
        elif req_method != params_method and response.text == response_3.text:
            print(f"\tBug in request method {req_method} and params/data method {params_method}")
            print(f"\tExpected result: {response_1.text}")
            print(f"\tActual result: {response_3.text}", end="\n\n")
