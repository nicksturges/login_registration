from flask import Flask, render_template, request, redirect, session, flash
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = connectToMySQL('registration')
app.secret_key= "ThisIsSecret"
bcrypt = Bcrypt(app)

@app.route('/')
def friends():
    return render_template('index.html')
   
@app.route('/process', methods=['POST'])
def process():
    print('working')
    goodform = True
####################### CHECKS IF FIRST NAME IS FILLED OUT
    if len(request.form['firstName']) < 1:
        flash('First Name required')
   
    ##################### checks if last name if filled out
    if len(request.form['lastName']) < 1 and (request.form['firstName']) == True:
        flash('Last Name required')
   
  ###################### checks if email is filled out and valid
    if len(request.form['email']) < 1:
        flash('Email required')
        goodform = False 
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('Invalid Email')
    # elif request.form != True:
    #         flash('Email already used')   
        goodform = False 
   
    ############################ Checks if password is valid
    if len(request.form['password']) < 1:
        flash('Password required')
        goodform = False
    elif len(request.form['password']) < 4 or len(request.form['password']) > 8:
        flash("Pin must be 4-8 digits", 'password')
        goodform = False
    # if bcrypt.checkpw(password, hashed):
    #     print('yay')
    # else: 
    #     print('does not match')
    # pw_hash = bcrypt.generate_password_hash(request.form['password'])  
    # print("password:" + pw_hash) 
    mysql = connectToMySQL('registration')
    query = 'INSERT INTO `registration`.`users` (`firstName`, `lastName`, `email`, `password`) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password_hash)s);'
    data = {
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'email': request.form['email'],
            'password_hash': request.form['password']
            }
    new_friend_id = mysql.query_db(query, data)
    
    print('stored')
    if goodform == False:
        flash('Read the directions')
    else: 
        flash('thanks')   
    return redirect("/")
    
   

  

@app.route("/process", methods = ['POST'])
def login():
   
    print('logged')
    mysql = connectToMySQL("registration")
    query = 'SELECT * FROM `registration.users WHERE password` = %(password)s ;'
    mysql.query_db(query) 
    goodform = True
    
    if len(request.form['password']) < 1:
        flash('password required')
        goodform = False
    else: 
        flash('success')
    # if bcrypt.checkpw(password, hashed):
    #     print('yay')
    # else: 
    #     print('does not match')
    #######################
    if goodform == False:
        return redirect("/")
    else:
        return redirect('/success' )

@app.route('/success')
def success():
    return render_template('success.html')


# @app.route('/success', methods = ['POST'])
# def create():
#     return redirect('/')


if __name__ == "__main__":
    app.run(debug = True)
   

   




 
    
    
       
       
    
    
    
    
    
  
