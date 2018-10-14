from flask import Flask, request, redirect
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader
(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def display_form():
    template = jinja_env.get_template('form.html')
    return template.render()

@app.route("/", methods=["POST"])
def validate_form():
    username=request.form['username']
    password=request.form['password']
    verify=request.form['verify']
    email=request.form['email']
    username_error_1=''
    username_error_2=''
    username_error_3=''
    password_error_1=''
    password_error_2=''
    password_error_3=''
    verify_error_1=''
    verify_error_2=''
    verify_error_3=''
    email_error_1=''
    email_error_2=''
    email_error_3=''
    email_error_4=''
    
    #step one, if blank error
    if username=='':
        username_error_1 += 'please enter a username'
    if password=='':
        password_error_1 +='please enter a password'
    if verify=='':
        verify_error_1 +='please enter a password'
    
    #step 2, if there is a space in username, pwd, or verify
    if ' ' in username:
        username_error_2 += " no spaces please"
    if ' ' in password:
        password_error_2 += " no spaces please"
    if ' ' in verify:
        verify_error_2 += " no spaces please"

#it cant be less than 3 characters or more than 20 characters
    if len(username) < 3 or len(username)> 20:
        username_error_3 += " your username must be between 3 and 20 characters"
    if len(password) < 3 or len(password) > 20:
        password_error_3+= " your password must be between 3 and 20 characters"

# username and verify must match
    if password != verify:
        verify_error_3 += " passwords do not match"

#email must have 1 @, 1 ., and can't be less than 3 or more than 20 
    if email != '':
        if '@@' in email or '..' in email:
            email_error_1 += 'please enter a valid email'
        if ' ' in email:
            email_error_2 += ' no spaces please'
        if len(email) < 3 or len(email) > 20:
            email_error_3 += " your email can't be less than 3 characters or more than 20"
        if '@' not in email or '.' not in email:
            email_error_4 += " please enter a valid email"

    
    if username_error_1 != '' or username_error_2 != '' or username_error_3 !='' or password_error_1 !='' or password_error_2!= '' or password_error_3!='' or verify_error_1!='' or verify_error_2!='' or verify_error_3 !='' or email_error_1 !='' or email_error_2!='' or email_error_3!='' or email_error_4!='':
        template = jinja_env.get_template('form.html')
        return template.render(username=username, username_error=username_error_1 + username_error_2 + username_error_3, password_error=password_error_1+password_error_2+password_error_3, verify_error=verify_error_1+verify_error_2+verify_error_3, email=email, email_error=email_error_1+email_error_2+email_error_3+email_error_4)
    else:
        return redirect("/welcome?username={}".format(username))

@app.route("/welcome")
def welcome_user():
    username=request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(name=username)

app.run()