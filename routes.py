from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SignupForm, LoginForm, AddressForm

# Initiate Flask object
app = Flask(__name__)

# Load database into app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
db.init_app(app)

# Load secret key (?)
app.secret_key = "development-key"

# ---- Template routing

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

# Detects 'GET' and/or 'POST' method when signup page loads
@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))
	form = SignupForm() #SignupForm class imported from forms.py
	if request.method == 'POST': 
		if form.validate() == False: # Check if any validation errors were captured
			return render_template("signup.html", form=form) # Will return form with errors 
		else: # If no errors are found, user is added to database
			newuser = User(form.first_name.data, form.last_name.data, form.email_unique.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email # Initiate session object with 'email key'
			return redirect(url_for('home')) 


	elif request.method == 'GET':
		return render_template("signup.html", form=form) 

@app.route("/logout")
def logout():
	session.pop('email', None) # Ends session
	return redirect(url_for('index'))

@app.route("/home", methods=['GET', 'POST'])
def home():
	if 'email' not in session: # Allows access to 'home' page only if session object has 'email' key (i.e. a valid user is logged in)
		return redirect(url_for('login'))

	form= AddressForm()
	if request.method == 'POST':
		if form.validate() == False:
			return render_template("home.html", form=form)
		else:
			# handle the form submission
			pass
	elif request.method == 'GET':
		return render_template("home.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if 'email' in session:
		return redirect(url_for('home'))

	form =LoginForm() # Create instance of LoginForm() class from forms.py (this is used in the 'elif' below for '')**
	if request.method == 'POST':  
		if form.validate() == False:
			return render_template("login.html", form=form)
		else: # If form is filled out properly check database 
			email = form.email_unique.data
			password = form.password.data

			user = User.query.filter_by(email=email).first() # Query for user based on email
			if user is not None and user.check_password(password): # If the database query returns a value and the password is correct
				session['email'] = form.email_unique.data # Start a session object with the 'email' key set to to the user's unique email address
				return redirect(url_for('home'))
			else :
				return redirect(url_for('login'))

	elif request.method == 'GET':
		return render_template('login.html', form=form) # LoginForm() instance is passed to login.html**
		



if __name__ == "__main__":
	app.run(debug=True) 