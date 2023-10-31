import requests

data = {'email': "varundivitest@gmail.com", 'password': "avoltapassword1234"}

person = {
    'email': 'varun.divi@avoltacanada.com',
    'password': 'avoltapassword321',
    'first_name': 'Varun4',
    'last_name': 'Divi4',
    'birthdate': '1969-1-1',
    'avolta_licence': '12345678',
    'question1': 'What is your favorite color?',
    'answer1': 'yellow',
    'question2': 'What is your first car?',
    'answer2': 'prius',
    'question3': 'Where were you born?',
    'answer3': 'va',
}


response1 = requests.post('http://localhost:5000/login', json=data)

response3 = requests.post('http://localhost:5000/register', json=person)


print(response1.status_code)
print(response1.json())
print(response3.status_code)
print(response3.json())
