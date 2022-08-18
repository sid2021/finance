# Using the project in local environment

1. Clone the repository.
2. Run the following commands:

```bash
cd docker
docker-compose build
docker-compose up
docker-compose exec web python manage.py createsuperuser
```

3. Check if project is successfully running by going into `http://localhost:8001/admin/` (use username/password generated in step 2 above) or `http://localhost:8001/swagger/`.
4. We are using Django Rest Framework's `TokenAuthentication`. In order to generate token necessary to send correct header within each request use the following commnands:

```bash
docker-compose exec web python manage.py shell
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
u = get_user_model().objects.first()
token = Token.objects.create(user=u)
```

Copy the token obtained above to the authorization header which should look like that:

```
Authorization: Token a100c1059c3f103320c816df6661a0512dd1bdf3
```

5. After the process is complete send `POST` and `GET `requests to the following endpoints:

```
POST http://localhost:8001/api/v1/account/ # Create a new financial Account
POST http://localhost:8001/api/v1/transaction/ # Create a new Transaction
GET http://localhost:8001/api/v1/account/history/{pk}/ # Retrieve Account history
GET http://localhost:8001/api/v1/account/balance/{pk}/ # Retrieve Account balance together with history
GET http://localhost:8001/api/v1/account/ # Get list of all Accounts
GET http://localhost:8000/api/v1/users/{pk}/ # Retrieve User details
```

Make sure that you provide correct TokenAuthentication credentials (refer to step 4 above).

## Running tests locally

```
cd docker
docker-compose run --rm web test
```

# Main libraries used to build the project

- django
- djangorestframework
- drf-yasg
- psycopg2-binary
- dj-database-url
- pip-tools
- pytest

# API Documentation

API documentation is available at `http://localhost:8001/swagger/`.

# Requests examples

Create a new financial Account

```python
import requests
import json

url = "http://localhost:8001/api/v1/account/"

payload = json.dumps({
  "balance": "1000",
  "currency": "EUR"
})
headers = {
  'Authorization': 'Token 0d61306b2128faf375364fa48e997a0b96756d81',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

Create a new Transaction

```python
import requests
import json

url = "http://localhost:8001/api/v1/transaction/"

payload = json.dumps({
  "type": "Deposit",
  "account": "1",
  "amount": "40"
})
headers = {
  'Authorization': 'Token 0d61306b2128faf375364fa48e997a0b96756d81',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

Retrieve Account history

```python
import requests
import json

url = "http://localhost:8001/api/v1/account/history/1/"

payload = ""
headers = {
  'Authorization': 'Token 0d61306b2128faf375364fa48e997a0b96756d81',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

Retrieve Account balance together with history

```python
import requests
import json

url = "http://localhost:8001/api/v1/account/balance/1/"

payload = ""
headers = {
  'Authorization': 'Token 0d61306b2128faf375364fa48e997a0b96756d81',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

Retrieve User details

```python
import requests
import json

url = "http://localhost:8001/api/v1/users/1/"

payload = ""
headers = {
  'Authorization': 'Token 0d61306b2128faf375364fa48e997a0b96756d81',
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

# Postman collection

For conveniance a Postman collection was provided in the app's root directory (`postman_collection.json`).

# Production environment

No settings for production environment were implemented. App was configured for local development only.
