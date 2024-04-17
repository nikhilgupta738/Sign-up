from flask_pymongo import PyMongo 
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "testing"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/UserHandlingSystem'
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('Signup.html')

@app.route('/signup_new_user', methods=['POST'])
def signup_new_user():
    users_collection = mongo.db.signup

    username = request.form.get('username')
    password = request.form.get('password')
    conf_password = request.form.get('confirmpassword')
    if password == conf_password:

        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return "Username already taken. Choose another username."

        users_collection.insert_one({
            'username': username,
            'password': password
        })

        return "Registration successful"
    return "Unsucessful"

@app.route('/login', methods=['POST'])
def login():
    users_collection = mongo.db.signup

    username = request.form.get('username')

    user = users_collection.find_one({'username': username})

    if user:
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return 'Invalid username or password'


if __name__ == '__main__':
    app.run(debug=True)