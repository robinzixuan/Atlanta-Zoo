from LoginDemoApp import app, db, bcrypt, serializer
from LoginDemoApp.database_tables import load_user, User
from LoginDemoApp.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, Markup, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from itsdangerous import SignatureExpired, BadTimeSignature


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/signUp", methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Extract user inputs
        username = form.username.data.lower()
        email = form.email.data.lower()
        password = form.password.data

        # Hash password
        # password = bcrypt.generate_password_hash(password)
        # Store user inputs in database
        cur = db.get_db().cursor()
        try:
            cur.execute('SELECT * FROM User WHERE Email = "%s"' % email)
            rv = cur.fetchone()
            if rv is None:
                cur.execute('SELECT * FROM User WHERE Username = "%s"' % username)
                rv = cur.fetchone()
                if rv is None:
                    cur.execute('INSERT INTO User (Username, Email, Password) VALUES (%s, %s, %s)', (username, email, password))
                    # todo: visitor sign up and staff signup
                    flash('Sign up successful')
                    return redirect(url_for('home'))
                else:
                    raise ValueError("The Username already exist")
            else:
                raise ValueError("The Email already exist")
        except Exception as e:
             # raise ValueError("The Value is not right")
             raise e
    return render_template('sign_up.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # If user is already logged in redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Create LoginForm() object to validate user input when its submitted as a POST request
    form = LoginForm()
    # If user input has been submitted and been validated log the user in
    if form.validate_on_submit():
        # Extract user inputs
        email = form.email.data.lower()
        password = form.password.data
        # print(email, password)

        # Search for user in database
        cur = db.get_db().cursor()
        cur.execute('SELECT * FROM User WHERE Email = "%s"' % email)
        fetch = cur.fetchone()
        if fetch:
            # print(fetch)
            u, e, p = fetch
            if p == password:
                user = User(u, e, p)

                # check use type
                cur = db.get_db().cursor()
                cur.execute('SELECT * FROM Visitor WHERE Username = "%s"' % u)
                if cur.fetchone():
                    user.set_type("visitor")
                    login_user(user)
                    return redirect(url_for('visitormain'))
                cur.execute('SELECT * FROM Staff WHERE Username = "%s"' % u)
                if cur.fetchone():
                    # print("staff")
                    user.set_type("staff")
                    login_user(user)
                    return redirect(url_for('staff'))
                # print("admin")
                user.set_type("admin")
                login_user(user)
                return redirect(url_for('visitormain'))
            else:
                flash('Wrong password. Please check your credentials')
        else:
            flash('User does not exist')

    # If user is not already logged in redirect to login page
    return render_template('login.html', form=form)


# This route can only be accessed if user is already logged in
@login_required
@app.route("/logout")
def logout():
    # Log out user and redirect to home page
    logout_user()
    return redirect(url_for('home'))


# This route can only be accessed with a valid token
# When accessed it confirms the email the token is associated with
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        # Extract email address from token
        email = serializer.loads(token, salt='email', max_age=1800)

        # Update confirmed email flag to true
        user = User.query.filter_by(email=email).first()
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()

        # Notify user with success message
        flash('Your account has been created! You are now able to log in')

    # If token is expired or invalid notify user
    except (SignatureExpired, BadTimeSignature):
        if SignatureExpired:
            return 'Token expired'
        elif BadTimeSignature:
            return 'Invalid token'

    # If email confirmation was successful return to login page so user can login
    return redirect(url_for('login'))


@app.route("/visitormain", methods=['GET', 'POST'])
@login_required
def visitormain():
    # print(type(current_user), dir(current_user))
    return render_template('visitormain.html')


@app.route("/staff", methods=['GET', 'POST'])
@login_required
def staff():
    # print(type(current_user), dir(current_user))
    return render_template('staff.html')

@app.route("/staff_view_shows", methods=['GET', 'POST'])
@login_required
def staff_view_shows():
    return render_template('show.html')

@app.route("/staff_search_animal", methods=['GET', 'POST'])
@login_required
def staff_search_animal():
    return render_template('show.html')
