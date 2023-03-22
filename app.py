import os
from flask import Flask, redirect, url_for, session, request, jsonify
from flask_restful import Resource, Api
from flask_oauthlib.client import OAuth

# Create a Flask app instance
app = Flask(__name__)
app.secret_key = '<your-api-key>'
api = Api(app)

# Set the scopes of the API you want to access
SCOPES = ['https://www.googleapis.com/auth/userinfo.email']


# Set up OAuth
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='<your-consumer-key>',
    consumer_secret='<your-secret-key>',
    request_token_params={
        'scope': SCOPES
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)


class Authorized(Resource):
    def get(self, provider):
        resp = google.authorized_response()
        if resp is None:
            return 'Access denied: reason={0} error={1}'.format(
                request.args['error_reason'],
                request.args['error_description'],
            )
        session['google_token'] = (resp['access_token'], '')
        me = google.get('userinfo')
        return jsonify(me.data)

    @app.route('/login/google')
    def google_login():
        callback_url = url_for('google_auth', _external=True)
        return google.authorize(callback=callback_url)

    @app.route('/google-auth')
    def google_auth():
        resp = google.authorized_response()
        if resp is None:
            return 'Access denied: reason={0} error={1}'.format(
                request.args['error_reason'],
                request.args['error_description']
            )
        access_token = resp['access_token']
        user_info = google.get('userinfo').data
        return jsonify(user_info)

    @google.tokengetter
    def get_google_token():
        return session.get('google_token')


class Login(Resource):
    def get(self, provider):
        callback = url_for(
            'authorized',
            provider=provider,
            _external=True,
        )
        return google.authorize(callback=callback)


# Index
@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the TODO list!'
todos = {}


class TodoList(Resource):
    def get(self):
        return jsonify(todos)

    def post(self):
        todo_id = len(todos) + 1
        todo = request.get_json()
        todo['id'] = todo_id
        todo['completed'] = False
        todos[todo_id] = todo
        return jsonify({todo_id: todo})


class TodoItem(Resource):
    def get(self, todo_id):
        return jsonify(todos.get(todo_id))

    def put(self, todo_id):
        todo = todos.get(todo_id)
        if not todo:
            return {'error': 'Todo not found'}, 404
        todo['completed'] = True
        return jsonify({todo_id: todo})

    def delete(self, todo_id):
        todo = todos.pop(todo_id, None)
        if not todo:
            return {'error': 'Todo not found'}, 404
        return '', 204


# Add the resource routes
api.add_resource(TodoList, '/todos')
api.add_resource(TodoItem, '/todos/<int:todo_id>')
api.add_resource(Login, '/login/<string:provider>')
api.add_resource(Authorized, '/authorized/<string:provider>')


# Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
