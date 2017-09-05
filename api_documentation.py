# /api_documentation.py

"""Documentation for the API
"""
from flask import Flask
from flasgger import Swagger

from app.app import create_app
import os

app = create_app('production')
swagger = Swagger(app)

@app.route('/auth/register', methods=['POST'])
def auth_register():
    """Endpoint for creating a new user account.
    Create a new user account
    ---
    parameters:
      - name: email
        in: formData
        type: string
        description: Email address with valid format
        required: true
      - name: name
        in: formData
        type: string
        description: Username of any length with any combination of characters
        required: true
      - name: password
        in: formData
        type: string
        description: Password of any length with any combination of characters
        required: true
    responses:
      201:
        description: User account created successfully
      202:
        description: User account for the given email already exists
      400:
        description: Invalid email address used
      401:
        description: Invalid request
    """
    pass

@app.route('/auth/login', methods=['POST'])
def auth_login():
    """Endpoint for user login
    Return a token for authenticating operations with the API
    ---
    parameters:
      - name: email
        in: formData
        type: string
        description: Email address for existing account
        required: true
      - name: password
        in: formData
        type: string
        description: Password for the entered email address
        required: true
    responses:
      200:
        description: User login was successful
      401:
        description: Either the username or the password was invalid
      500:
        description: Unspecified server error
    """
    pass

@app.route('/auth/logout', methods=['POST'])
def auth_logout():
    """Endpoint for user logout
    Revoke the authorization of the user token in the header
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
    responses:
      200:
        description: User logout successful
      401:
        description: Invalid token passed
      500:
        description:: Unspecified server error
    """
    pass

@app.route('/auth/reset-password', methods=['POST'])
def auth_reset_password():
    """Endpoint for the user to reset their password
    Update the user's password with a new one
    ---
    parameters:
      - name: email
        in: formData
        type: string
        description: User's email address which has a registered account
        required: true
      - name: oldpassword
        in: formData
        type: string
        description: User's current password for the registered account
        required: true
      - name: newpassword
        in: formData
        type: string
        description: Password the user desires to replace their current one
        required: true
    responses:
      200:
        description: The password was reset successfully
      501:
        description: Server could not complete the request
    """
    pass

@app.route('/bucketlists/', methods=['GET'])
def bucketlists_get():
    """Endpoint for a logged in user to retrieve their bucketlists
    Return all bucketlists that belong to the user
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: q
        in: query
        type: string
        description: The API will search for all bucketlists that have the string in their name
      - name: limit
        in: query
        type: integer
        description: The API will return a maximum number of results defined by the number of limit
      - name: page
        in: query
        type: integer
        description: A number to navigate between all the results that have been divided by limit
    responses:
      200:
        description: API successfully returns the bucketlists
      401:
        description: The authorization token cannot be used to access bucketlists
      404:
        description: The requested resource does not exist 
    """
    pass

@app.route('/bucketlists/', methods=['POST'])
def bucketlists_post():
    """Endpoint for a logged in user to create a new bucketlist
    Return the created bucketlist
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: name
        in: formData
        type: string
        description: The name of the new bucketlist
        required: true
      - name: date
        in: formData
        type: string
        description: The date by which the bucketlist is meant to be completed
        required: false
      - name: description
        in: formData
        type: string
        description: A brief summary of the bucketlist's content or context
        required: false
    responses:
      201:
        description: API successfully creates the bucketlist
      401:
        description: The authorization token cannot be used to create bucketlists
    """
    pass

@app.route('/bucketlists/<int:list_id>', methods=['PUT'])
def bucketlist_update():
    """Endpoint for a logged in user to update a specific bucketlist
    Return the edited bucketlist
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist to be updated
        required: true
      - name: name
        in: formData
        type: string
        description: The new name for the bucketlist
      - name: date
        in: formData
        type: string
        description: The new date for the bucketlist
      - name: description
        in: formData
        type: string
        description: The new description for the bucketlist
    responses:
      200:
        description: API successfully updates the bucketlist
      401:
        description: The authorization token cannot be used to update bucketlists
      404:
        description: The expected bucketlist to update was not found
    """
    pass

@app.route('/bucketlists/<int:list_id>', methods=['GET'])
def bucketlist_get():
    """Endpoint for a logged in user to retrieve a specific bucketlist
    Return the requested bucketlist
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist to be updated
        required: true
    responses:
      200:
        description: API successfully updates the bucketlist
      401:
        description: The authorization token cannot be used to update bucketlists
      404:
        description: The expected bucketlist to update was not found
    """
    pass

@app.route('/bucketlists/<int:list_id>', methods=['DELETE'])
def bucketlist_delete():
    """Endpoint for a logged in user to delete a specific bucketlist
    Delete the specified bucketlist
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist to be deleted
        required: true
    responses:
      200:
        description: API successfully deletes the bucketlist
      401:
        description: The authorization token cannot be used to delete bucketlists
      404:
        description: The expected bucketlist to delete was not found
    """
    pass

@app.route('/bucketlists/<int:list_id>/items/', methods=['GET'])
def bucketlist_items_get():
    """Endpoint for a logged in user to retrieve all items in a bucketlist
    Retrieve the items of the specified bucketlist
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist to be retrieve items from
        required: true
      - name: q
        in: query
        type: string
        description: The API will search for all bucketlist items that have the string in their name
      - name: limit
        in: query
        type: integer
        description: The API will return a maximum number of results defined by the number of limit
      - name: page
        in: query
        type: integer
        description: A number to navigate between all the results that have been divided by limit
    responses:
      200:
        description: API successfully returns the bucketlist items
      401:
        description: The authorization token cannot be used to retrieve the bucketlist items
      404:
        description: The expected bucketlist to retrieve items from was not found
    """
    pass

@app.route('/bucketlists/<int:list_id>/items/', methods=['POST'])
def bucketlist_items_post():
    """Endpoint for a logged in user to create new items in a bucketlist
    Return the item created
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist to be create items in
        required: true
      - name: name
        in: formData
        type: string
        description: The name of the new bucketlist item
        required: true
      - name: description
        in: formData
        type: string
        description: A description for the new bucketlist item
    responses:
      200:
        description: API successfully creates the bucketlist item
      401:
        description: The authorization token cannot be used to create the bucketlist item
      404:
        description: The expected bucketlist to create the item in was not found
    """
    pass

@app.route('/bucketlists/<int:list_id>/items/<int:item_id>', methods=['PUT'])
def bucketlist_item_update():
    """Endpoint for a logged in user to update an item in a bucketlist
    Return the updated item
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist to update items in
        required: true
      - name: item_id
        in: path
        type: integer
        description: The id of the bucketlist item to be updated
        required: true
      - name: name
        in: formData
        type: string
        description: A new name for the bucketlist item
      - name: description
        in: formData
        type: string
        description: A new description for the bucketlist
    responses:
      200:
        description: API successfully creates the bucketlist item
      401:
        description: The authorization token cannot be used to create the bucketlist item
      404:
        description: The expected bucketlist to update the item in was not found
    """
    pass

@app.route('/bucketlists/<int:list_id>/items/<int:item_id>', methods=['DELETE'])
def bucketlist_item_delete():
    """Endpoint for a logged in user to delete an item in a bucketlist
    Delete a specific item for a specific bucketlist
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        description: Has two parts, a string "Bearer " and a string for the authorization token
        required: true
      - name: list_id
        in: path
        type: integer
        description: The id of the bucketlist which has the item to be deleted
        required: true
      - name: item_id
        in: path
        type: integer
        description: The id of the bucketlist item to be deleted
        required: true
    responses:
      200:
        description: API successfully deleted the bucketlist item
      401:
        description: The authorization token cannot be used to delete the bucketlist item
      404:
        description: The expected bucketlist to delete the item from was not found
    """
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
