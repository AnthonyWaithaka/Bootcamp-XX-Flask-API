# Bootcamp-XX-Flask-API
Challenge 3 project for Andela Bootcamp XX

#
[![Build Status](https://travis-ci.org/AnthonyGW/Bootcamp-XX-Flask-API.svg?branch=feedback)](https://travis-ci.org/AnthonyGW/Bootcamp-XX-Flask-API) 
[![Coverage Status](https://coveralls.io/repos/github/AnthonyGW/Bootcamp-XX-Flask-API/badge.svg?branch=feedback)](https://coveralls.io/github/AnthonyGW/Bootcamp-XX-Flask-API?branch=feedback)


The API can be run on a flask server
Set the flask app environment variable to `run.py` using `set FLASK_APP=run.py` or `export FLASK_APP=run.py`\
Set the default configurations environment variable `APP_SETTINGS` to any of `development`, `testing`, `staging`, `production`. \
The `testing` configuration uses a test database server with:
Username `postgres`\
password `None`\
database name `test_db`\
host `localhost`\
port `5432`

The complete documentation is available on the endpoint, `/apidocs`

## Current Features:
| Feature | Endpoint | Method | Data 
| --- | --- | --- | --- |
1. Register a new user account | `/auth/register` | `[POST]` | name, email, password
2. Log in with the registered user account | `/auth/login` | `[POST]` | email, password
3. Log out from the current user account | `/auth/logout` | `[POST]` | Authentication Header
4. Reset password | `/auth/reset-password` | `[POST]` | Authentication Header
5. View all bucketlists on the logged in user account | `/bucketlists/` | `[GET]` | Authentication Header
6. Create a bucketlist | `/bucketlists/` | `[POST]` | name, date, description, Authentication Header
7. Update a bucketlist | `/bucketlists/<int:list_id>` | `[PUT]` | name, date, description, Authentication Header
8. Delete a bucketlist  | `/bucketlists/<int:list_id>` | `[DELETE]` | Authentication Header
9. View all items for a specific bucketlist | `/bucketlists/<int:list_id>/items/` | `[GET]` | Authentication Header
10. Create an item for a specific bucketlist | `/bucketlists/<int:list_id>/items/` | `[POST]` | name, description, Authentication Header
11. Update a bucketlist item | `/bucketlists/<int:list_id>/items/<int:item_id>` | `[PUT]` | name, description. Authentication Header
12. Delete a bucketlist item | `/bucketlists/<int:list_id>/items/<int:item_id` | `[DELETE]` | Authentication Header
