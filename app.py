# app.py
from flask import Flask, render_template, request, jsonify
import joblib
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Load the trained model
model = joblib.load('diabetes_model.joblib')

# connect to the database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# create a table
cursor.execute(''' CREATE TABLE IF NOT EXISTS users 
               ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL)''')

connection.commit()
connection.close()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods =[ 'POST' , 'GET'])



def login():
    username = request.form.get('username')
    password = request.form.get('password')

    #  check if the user exists
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM users WHERE username = ?''', (username,))
    user = cursor.fetchone()
    connection.close()


    if user and check_password_hash(user[2], password):
        return render_template('predict.html')
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'})
    
    return render_template('login.html')



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'status': 'error', 'message': 'Username already exists'})

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, hashed_password))
        connection.commit()
        connection.close()

        return jsonify({'status': 'success', 'message': 'User registered successfully'})

    return render_template('register.html')
    

@app.route('/predict', methods=['POST'])
def predict():
   if request.method == 'POST':
       preg = request.form['preg']
       glucose = request.form['glucose']
       bp = request.form['bp']
       skin = request.form['skin']
       insulin = request.form['insulin']
       bmi = request.form['bmi']
       dpf = request.form['dpf']
       age = request.form['age']

       # Make prediction
       prediction = model.predict([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])[0]
       if prediction == 1:
           result = 'diabetic'
       else:
           result = 'not diabetic'
       return render_template('result.html', result=result)
   
        

if __name__ == '__main__':
    app.run(debug=True)
