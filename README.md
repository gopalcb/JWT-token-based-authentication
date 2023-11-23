## JSON Web Token (JWT) based authentication of Flask REST API/Microservice API
<hr>

##### JWT Use Cases:

* Authorization: This is the most common use cases of JWT token. Once the user is logged in, each subsequent request will include the JWT, allowing the user to access routes, services, and resources that are permitted with that token.
* Information Exchange: JSON Web Tokens are a good way of securely transmitting information between parties.

We will test the Flask API in this repository using requests library and making HTTP get and post calls to localhost (http://localhost:2000).


```python
import requests
```

### Check Flask REST API connection:


```python
url = 'http://localhost:2000/'
resp = requests.get(url)
print(resp.text)
```

    flask rest connected


### Dummy user signup:


```python
url = 'http://localhost:2000/signup'
myobj = {
    'name': 'Test User',
    'email': 'test@gmail.com',
    'password': 'test123'
}

resp = requests.post(url, json = myobj)
print(resp.text)
```

    {
      "code": 201,
      "data": {
        "email": "test@gmail.com",
        "name": "Test User",
        "password": "scrypt:32768:8:1$KNTfrQV4SHtEuCTp$eefb9c985a99e315f6e1451b3bec49a607fac995f65dc5e568d8d7164c4a3e75b9bb2492b73d6297f058cbf9f10501cddb01b49e9364ab0fa5864b64f5f4ea4d"
      },
      "message": "successfully registered",
      "status": true
    }
    


### Dummy user login with invalid password (failed login):


```python
url = 'http://localhost:2000/login'
myobj = {
    'email': 'test1@gmail.com',
    'password': 'test123-'
}

resp = requests.post(url, json = myobj)
print(resp.text)
```

    {
      "code": 403,
      "data": {
        "email": "test1@gmail.com",
        "password": "test123-"
      },
      "message": "verification failed - incorrect user email or password",
      "status": false
    }
    


### Successfull user login: 


```python
url = 'http://localhost:2000/login'
myobj = {
    'email': 'test@gmail.com',
    'password': 'test123'
}

resp = requests.post(url, json = myobj)
print(resp.text)
```

    {
      "code": 201,
      "data": {
        "email": "test@gmail.com",
        "password": "test123"
      },
      "message": "verification success",
      "status": true,
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZ21haWwuY29tIiwicGFzc3dvcmQiOiJ0ZXN0MTIzIiwiZXhwIjoxNzAwNjcwMTIzfQ.W8mlPzDXb9IGBwl5txG3F3n1k0_3hmnVyursv4J9XXo"
    }
    


### Authinticate using JWT token and fetch dummy user list:

The JWT token should be attached to the request header using x-access-token key. In the Python backend, the same key will be used to retrieve the token form request header and use it for user authentication.


```python
import json
token = json.loads(resp.text)['token']
token
```




    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZ21haWwuY29tIiwicGFzc3dvcmQiOiJ0ZXN0MTIzIiwiZXhwIjoxNzAwNjcwMTIzfQ.W8mlPzDXb9IGBwl5txG3F3n1k0_3hmnVyursv4J9XXo'



#### Attempt with invalid JWT token:


```python
r = requests.get("http://localhost:2000/users", headers={"x-access-token":'invalid-token'})
print(r.text)
```

    {
      "code": 401,
      "data": null,
      "message": "auth failed - token is invalid",
      "status": false
    }
    


#### Attempt with correct JWT token:


```python
r = requests.get("http://localhost:2000/users", headers={"x-access-token": token})
print(r.text)
```

    {
      "users": [
        {
          "email": "user1@gmail.com",
          "id": 1
        },
        {
          "email": "user2@gmail.com",
          "id": 2
        }
      ]
    }
    

