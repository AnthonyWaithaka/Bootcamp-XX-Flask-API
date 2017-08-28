# Bootcamp-XX-Flask-API
Challenge 3 project for Andela Bootcamp XX

#
[![Build Status](https://travis-ci.org/AnthonyGW/Bootcamp-XX-Flask-API.svg?branch=feedback)](https://travis-ci.org/AnthonyGW/Bootcamp-XX-Flask-API) 
[![Coverage Status](https://coveralls.io/repos/github/AnthonyGW/Bootcamp-XX-Flask-API/badge.svg?branch=feedback)](https://coveralls.io/github/AnthonyGW/Bootcamp-XX-Flask-API?branch=feedback)


The API can be run on a flask server
Set the flask app environment variable to `run.py` using `set FLASK_APP=run.py` or `export FLASK_APP=run.py`
Set the default configurations environment variable `APP_SETTINGS` to any of `development`, `testing`, `staging`, `production`.
The `testing` configuration uses a test database server with:
Username `postgres`
password `None`
database name `test_db`
host `localhost`
port `5432`

## Current Features:
1. Register a new user account
`/auth/register/` `[POST]`
Data: name, email, password
2. Log in with the registered user account
`/auth/login/` `[POST]`
Data: email, password
3. View all bucketlists on the logged in user account
`/bucketlists/` `[GET]`
4. Create a bucketlist
`/bucketlists/` `[POST]`
Data: name, date, description
5. Update a bucketlist
`/bucketlists/<int:id>` `[PUT]`
Data: name, date, description
6. Delete a bucketlist
`/bucketlists/<int:id>` `[DELETE]`
7. View all items for a specific bucketlist
`/bucketlists/<int:id>/items/` `[GET]`
8. Create an item for a specific bucketlist
`/bucketlists/<int:id>/items/` `[POST]`
Data: name, description
9. Update a bucketlist item
`/bucketlists/<int:id>/items/<int:item_id>` `[PUT]`
Data: name, description
10. Delete a bucketlist item
`/bucketlists/<int:id>/items/<int:item_id` `[DELETE]`


