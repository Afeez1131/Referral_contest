import requests
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

url = "http://127.0.0.1:8000/api/v1/users/"
token_url = "http://127.0.0.1:8000/api/v1/api-token-auth/"
i = 0
url = "http://localhost:8000/api/v1/contest/create_referral/"


start_date = datetime.now()
end_date = start_date + timedelta(days=1)

data = {
            "refer_name": "Test Referral",
            "business_owner": 1,
            "phone_number": '08102202033',
        }
#
# data = {
#     "username": "admin",
#     "password": "password"
# }
# token_res = requests.post(token_url, data)
# token = token_res.json().get('token')
# print(token)
token = "8dc4c5d2f001325846ff96ee92679d8fca0eaced"
headers = {
    'Authorization': f'Token {token}'
}
response = requests.post(url, data=data, headers=headers)
print(response.json(), response.status_code)

