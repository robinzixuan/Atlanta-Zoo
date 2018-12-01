from LoginDemoApp import app, db, bcrypt, serializer
from LoginDemoApp.database_tables import load_user, User
from LoginDemoApp.forms import *
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
    visitor_form = VisitorRegistrationForm()
    staff_form = StaffRegistrationForm()
    if visitor_form.submit1.data and visitor_form.validate_on_submit():
        username = visitor_form.username.data.lower()
        email = visitor_form.email.data.lower()
        password = visitor_form.password.data
        cur = db.get_db().cursor()
        cur.execute('SELECT * FROM User WHERE Email = "%s"' % email)
        rv = cur.fetchone()
        if rv is None:
            cur.execute('SELECT * FROM User WHERE Username = "%s"' % username)
            rv = cur.fetchone()
            if rv is None:
                cur.execute('INSERT INTO User (Username, Email, Password) VALUES (%s, %s, %s)',
                            (username, email, password))
                cur.execute('INSERT INTO Visitor VALUES (%s)', username)
                flash('Sign up successful')
                return redirect(url_for('home'))
            else:
                flash('The Username already exist')
        else:
            flash('The Email already exist')
    if staff_form.submit2.data and staff_form.validate_on_submit():
        username = visitor_form.username.data.lower()
        email = visitor_form.email.data.lower()
        password = visitor_form.password.data

        cur = db.get_db().cursor()

        cur.execute('SELECT * FROM User WHERE Email = "%s"' % email)
        rv = cur.fetchone()
        if rv is None:
            cur.execute('SELECT * FROM User WHERE Username = "%s"' % username)
            rv = cur.fetchone()
            if rv is None:
                cur.execute('INSERT INTO User (Username, Email, Password) VALUES (%s, %s, %s)', (username, email, password))
                cur.execute('INSERT INTO Staff VALUES (%s)', username)
                flash('Sign up successful')
                return redirect(url_for('home'))
            else:
                flash('The Username already exist')
        else:
            flash('The Email already exist')
    return render_template('sign_up.html', form=visitor_form)



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
#
# @login_required
# @app.route("/animal_detail")
# def animal_detail():
#     return render_template("animal_detail.html")
#
# @login_required
# @app.route("/exhibit_detail")
# def exhibit_detail():
#     return render_template("exhibit_detail.html")
#
#
#
#
# ### visitor stuff
@app.route("/visitor", methods=['GET', 'POST'])
@login_required
def visitor():
    return render_template('visitor.html')
#
# @app.route("/visitor_search_exhibit", methods=['GET', 'POST'])
# @login_required
# def visitor_search_exhibit():
#     return render_template("visitor_search_exhibit.html")
#
# @login_required
# @app.route("/visitor_search_animal")
# def visitor_search_animal():
#     return render_template("visitor_search_animal.html")
#
# @login_required
# @app.route("/visitor_search_show")
# def visitor_search_show():
#     return render_template("visitor_search_show.html")
#
# @login_required
# @app.route("/visitor_exhibit_history")
# def visitor_exhibit_history():
#     return render_template("visitor_exhibit_history.html")
#
# @login_required
# @app.route("/visitor_show_history")
# def visitor_show_history():
#     return render_template("visitor_show_history.html")
#
#
#
#
#

### staff stuff
@app.route("/staff", methods=['GET', 'POST'])
@login_required
def staff():
    # print(type(current_user), dir(current_user))
    return render_template('staff.html')

@app.route("/staff_view_shows", methods=['GET', 'POST'])
@login_required
def staff_view_shows():
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM Shows WHERE Hostby = %s', current_user.username)
    fetch = cur.fetchall()
    print(fetch)
    table = ShowsTable([Show(n, d, e) for n, d, e, _ in fetch])
    return render_template('staff_view_shows.html', table=table)

@app.route("/staff_search_animal", methods=['GET', 'POST'])
@login_required
def staff_search_animal():
    return render_template('show.html')
#
# @app.route("/staff_animal_care", methods=['GET', 'POST'])
# @login_required
# def staff_animal_care():
#     return render_template('show.html')

### admin stuff
# @login_required
# @app.route("/admin_view_staff")
# def admin_view_staff():
#     return render_template("admin_view_staff.html")
#
# @login_required
# @app.route("/admin_view_visitor")
# def admin_view_visitor():
#     return render_template("admin_view_visitor.html")
#
# @login_required
# @app.route("/admin_view_shows")
# def admin_view_shows():
#     return render_template("admin_view_shows.html")
#
# @login_required
# @app.route("/admin_view_animal")
# def admin_view_animal():
#     return render_template("admin_view_animal.html")
#
# @login_required
# @app.route("/admin_add_animal")
# def admin_add_animal():
#     return render_template("admin_add_animal.html")
#
# @login_required
# @app.route("/admin_add_shows")
# def admin_add_shows():
#     return render_template("admin_add_shows.html")






