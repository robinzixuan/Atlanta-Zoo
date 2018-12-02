from LoginDemoApp import app, db, bcrypt, serializer
from LoginDemoApp.database_tables import load_user, User
from flask import render_template, url_for, flash, Markup, redirect, request, make_response
from flask_login import login_user, current_user, logout_user, login_required
from pymysql.err import IntegrityError
from LoginDemoApp.table import *
import hashlib
import datetime

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
        password = hashlib.sha1(password.encode()).hexdigest()
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
        password = hashlib.sha1(password.encode()).hexdigest()

        cur = db.get_db().cursor()

        cur.execute('SELECT * FROM User WHERE Email = "%s"' % email)
        rv = cur.fetchone()
        if rv is None:
            cur.execute('SELECT * FROM User WHERE Username = "%s"' % username)
            rv = cur.fetchone()
            if rv is None:
                cur.execute('INSERT INTO User (Username, Email, Password) VALUES (%s, %s, %s)',
                            (username, email, password))
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
        password = hashlib.sha1(password.encode()).hexdigest()

        # print(email, password)

        # Search for user in database
        cur = db.get_db().cursor()
        cur.execute('SELECT * FROM User WHERE Email = "%s"' % email)
        fetch = cur.fetchone()

        cur.execute('SELECT Username FROM Staff')

        # print(forms.staff_choices)
        staff_choices = [(i[0], i[0]) for i in cur.fetchall()]
        # print(forms.staff_choices)
        print(dir(AddShowForm))
        AddShowForm.staff = SelectField('Staff', choices=staff_choices)
        if fetch:
            # print(fetch)
            u, e, p = fetch
            if p == password:
                user = User(u, e, p, "")

                # check use type
                cur = db.get_db().cursor()
                cur.execute('SELECT * FROM Visitor WHERE Username = "%s"' % u)
                if cur.fetchone():
                    user.set_type("visitor")
                    login_user(user)
                    return redirect(url_for('visitor'))
                cur.execute('SELECT * FROM Staff WHERE Username = "%s"' % u)
                if cur.fetchone():
                    # print("staff")
                    user.set_type("staff")
                    login_user(user)
                    return redirect(url_for('staff'))
                # print("admin")
                user.set_type("admin")
                login_user(user)
                return redirect(url_for('admin'))
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


# no need cookies
@login_required
@app.route("/animal_detail/<string:name>/<string:species>", methods=['GET', 'POST'])
def animal_detail(name, species):
    form = AnimalDetail()
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM Animal WHERE Name = "%s" AND Species = "%s"' % (name, species))
    name, sp, type, age, place = cur.fetchone()
    form.name.data = name
    form.species.data = species
    form.exhibit.data = place
    form.age.data = age
    form.type.data = type
    return render_template("animal_detail.html", form=form)


# cookies good
@login_required
@app.route("/exhibit_detail/<string:id>", methods=['GET', 'POST'])
def exhibit_detail(id):
    form = ExhibitDetail()
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM Exhibit WHERE Name = "%s"' % id)
    fetch = cur.fetchone()
    name, is_water, size = fetch
    # todo: merge into one sql query
    form.name.data = name
    form.size.data = size
    form.water_feature.data = "YES" if int(is_water) else "NO"
    if form.is_submitted():
        cur.execute('SELECT * FROM Animal WHERE Place = "%s" ORDER BY %s %s' % (id, form.by.data, form.direction.data))
        animals = cur.fetchall()
    else:
        cur.execute('SELECT * FROM Animal WHERE Place = "%s"' % id)
        animals = cur.fetchall()
    num_animals = len(animals)
    form.num_animals.data = num_animals
    # print(animals)
    table = ExhibitsTable1([Exhibit1(name, sp) for name, sp, _, _, _ in animals])

    return render_template("exhibit_detail.html", form=form, table=table)


# ### visitor stuff
@app.route("/visitor", methods=['GET', 'POST'])
@login_required
def visitor():
    return render_template('visitor.html')


@app.route("/visitor_search_exhibit", methods=['GET', 'POST'])
@login_required
def visitor_search_exhibit():
    form = SearchExhibitsForm()
    table = ExhibitsTable([])
    if form.is_submitted():
        if form.sort.data:
            name = request.cookies.get("visitor_search_exhibit_name") if request.cookies.get("visitor_search_exhibit_name") else None
            size_min = request.cookies.get("visitor_search_exhibit_size_min") if request.cookies.get("visitor_search_exhibit_size_min") else None
            size_max = request.cookies.get("visitor_search_exhibit_size_max") if request.cookies.get("visitor_search_exhibit_size_max") else None
            animal_min = request.cookies.get("visitor_search_exhibit_animal_min") if request.cookies.get("visitor_search_exhibit_animal_min") else None
            animal_max = request.cookies.get("visitor_search_exhibit_animal_max") if request.cookies.get("visitor_search_exhibit_animal_max") else None
            water_feature = 1 if form.water_feature.data else 0
            query = ['SELECT Exhibit.Name, Exhibit.Size, COUNT(*) as count, Exhibit.WaterFeature FROM Exhibit, Animal WHERE Exhibit.WaterFeature = "%s"' %
            (water_feature)]
            if name:
                query.append('Exhibit.Name = "%s"' % name)
            if size_min:
                query.append('Exhibit.Size >= "%s"' % size_min)
            if size_max:
                query.append('Exhibit.Size <= "%s"' % size_max)
            if animal_min and animal_max:
                query.append('GROUP BY Animal.Place = Exhibit.Name HAVING COUNT(*) <= "%s" AND COUNT(*) >= "%s"' %(animal_max, animal_min))
            query = " AND ".join(query)
            query += " ORDER BY %s %s" %(form.by.data, form.direction.data)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ExhibitsTable(
            [Exhibit(name, size, num_animals, ("YES" if int(water) else "NO")) for name, size, num_animals, water in
             fetch])
            res = make_response(render_template('visitor_search_exhibit.html', form=form, table=table))
            return res
        elif form.search.data:
            name = form.name.data
            size_min = form.size_min.data
            size_max = form.size_max.data
            animal_min = form.animal_min.data
            animal_max = form.animal_max.data
            water_feature = 1 if form.water_feature.data else 0
            query = ['SELECT Exhibit.Name, Exhibit.Size, COUNT(*) as count, Exhibit.WaterFeature FROM Exhibit, Animal WHERE Exhibit.WaterFeature = "%s"' %
            (water_feature)]
            if name:
                query.append('Exhibit.Name = "%s"' % name)
            if size_min:
                query.append('Exhibit.Size >= "%s"' % size_min)
            if size_max:
                query.append('Exhibit.Size <= "%s"' % size_max)
            if animal_min and animal_max:
                query.append('GROUP BY Animal.Place = Exhibit.Name HAVING COUNT(*) <= "%s" AND COUNT(*) >= "%s"' %(animal_max, animal_min))
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ExhibitsTable(
            [Exhibit(name, size, num_animals, ("YES" if int(water) else "NO")) for name, size, num_animals, water in
             fetch])
            res = make_response(render_template('visitor_search_exhibit.html', form=form, table=table))
            res.set_cookie("visitor_search_exhibit_name", name)
            res.set_cookie("visitor_search_exhibit_size_min",size_min)
            res.set_cookie("visitor_search_exhibit_size_max",size_max)
            res.set_cookie("visitor_search_exhibit_animal_min",animal_min)
            res.set_cookie("visitor_search_exhibit_animal_max",animal_min)
            res.set_cookie("visitor_search_exhibit_water_feature",water_feature)
            return res
    return render_template("visitor_search_exhibit.html", form=form)


# good
@login_required
@app.route("/visitor_search_animal", methods=['GET', 'POST'])
def visitor_search_animal():
    form = SearchAnimalForm()
    if form.is_submitted():
        if form.sort.data:
            name = request.cookies.get("visitor_search_animal_name") if request.cookies.get("visitor_search_animal_name") else None
            species = request.cookies.get("visitor_search_animal_species") if request.cookies.get("visitor_search_animal_species") else None

            age_min = request.cookies.get("visitor_search_animal_age_min") if request.cookies.get("visitor_search_animal_age_min") else None
            age_max = request.cookies.get("visitor_search_animal_age_max") if request.cookies.get("visitor_search_animal_age_max") else None
            exhibit = form.exhibit.data
            type = form.type.data
            query = ['SELECT * FROM Animal WHERE Type = "%s" AND Place = "%s"' % (type, exhibit)]
            if name:
                query.append('Name = "%s"' % name)
            if species:
                query.append('Species = "%s"' % species)
            if age_min:
                query.append('Age >= "%s"' % age_min)
            if age_max:
                query.append('Age <= "%s"' % age_max)
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            print(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTable([Animal(name, sp, ex, age, t) for name, sp, t, age, ex in fetch])
            res = make_response(render_template('visitor_search_animal.html', form=form, table=table))
            return res
        elif form.search.data:
            name = form.name.data
            species = form.species.data
            age_min = form.age_min.data
            age_max = form.age_max.data
            exhibit = form.exhibit.data
            type = form.type.data
            query = ['SELECT * FROM Animal WHERE Type = "%s" AND Place = "%s"' % (type, exhibit)]
            if name:
                query.append('Name = "%s"' % name)
            if species:
                query.append('Species = "%s"' % species)
            if age_min:
                query.append('Age >= "%s"' % age_min)
            if age_max:
                query.append('Age <= "%s"' % age_max)
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTable([Animal(name, sp, ex, age, t) for name, sp, t, age, ex in fetch])
            res = make_response(render_template('visitor_search_animal.html', form=form, table=table))
            res.set_cookie("visitor_search_animal_name", name)
            res.set_cookie("visitor_search_animal_species", species)
            res.set_cookie("visitor_search_animal_age_min", age_min)
            res.set_cookie("visitor_search_animal_age_max", age_max)
            res.set_cookie("visitor_search_animal_exhibit", exhibit)
            res.set_cookie("visitor_search_animal_type", type)
            return res
    return render_template("visitor_search_animal.html", form=form)


@login_required
@app.route("/visitor_search_show", methods=['GET', 'POST'])
def visitor_search_show():
    form = SearchShowsForm()
    if form.is_submitted():
        if form.sort.data:
            name = request.cookies.get("visitor_search_shows_name") if request.cookies.get("visitor_search_shows_name") else None
            exhibit = request.cookies.get("visitor_search_shows_exhibit") if request.cookies.get("visitor_search_shows_exhibit") else None
            date = request.cookies.get("visitor_search_shows_date") if request.cookies.get("visitor_search_shows_date") else None
            query = ['SELECT * FROM Shows WHERE LocateAt = "%s"' % exhibit]
            if name:
                query.append('Name = "%s"' % name)
            if date:
                query.append('DateAndTime = "%s"' % date)
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ShowsTable1([Show1(name, str(date), ex) for name, date, ex, _ in fetch])
            res = make_response(render_template('visitor_search_show.html', form=form, table=table))
            return res
        elif form.search.data:
            name = form.name.data
            exhibit = form.exhibit.data
            date = form.date.data
            query = ['SELECT * FROM Shows WHERE LocateAt = "%s"' % exhibit]
            if name:
                query.append('Name = "%s"' % name)
            if date:
                query.append('DateAndTime = "%s"' % date)
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ShowsTable1([Show1(name, str(date), ex) for name, date, ex, _ in fetch])
            res = make_response(render_template('visitor_search_show.html', form=form, table=table))
            res.set_cookie("visitor_search_shows_name", name)
            res.set_cookie("visitor_search_shows_exhibit", exhibit)
            res.set_cookie("visitor_search_shows_date", date)
            return res
    return render_template("visitor_search_show.html", form=form)


@login_required
@app.route("/visitor_exhibit_history", methods=['GET', 'POST'])
def visitor_exhibit_history():
    form = SearchExhibitsHistoryForm()
    table = ExhibitsTable([])
    if form.is_submitted():
        if form.sort.data:
            name = request.cookies.get("visitor_exhibit_history_name") if request.cookies.get("visitor_exhibit_history_name") else None
            date = request.cookies.get("visitor_exhibit_history_date") if request.cookies.get("visitor_exhibit_history_date") else None
            visit_num_max = request.cookies.get("visitor_exhibit_history_visit_num_max") if request.cookies.get("visitor_exhibit_history_visit_num_max") else None
            visit_num_min = request.cookies.get("visitor_exhibit_history_visit_num_min") if request.cookies.get("visitor_exhibit_history_visit_num_min") else None
            query = ['SELECT VisitExhibit.Exhibitname, VisitExhibit.Datetime, COUNT(*) as count FROM VisitExhibit WHERE Datetime = "%s"' % date]
            if name:
                query.append('Name = "%s"' % name)
            if visit_num_min and visit_num_max:
                query.append('GROUP BY Exhibitname HAVING COUNT(*) <= "%s" AND COUNT(*) >= "%s"' % (visit_num_max, visit_num_min))
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            cur = db.get_db().cursor()
            cur.execute()
            fetch = cur.fetchall()
            table = ExhibitHistoryTable(
                [ExhibitHistoryTable(name, time, num_of_visits) for name, time, num_of_visits in fetch])
            res = make_response(render_template('visitor_exhibit_history.html', form=form, table=table))
            return res
        elif form.sort.search:
            name = form.name.data
            date = date = form.date.data
            visit_num_max = form.visit_num_max.data
            visit_num_min = form.visit_num_min.data
            query = ['SELECT VisitExhibit.Exhibitname, VisitExhibit.Datetime, COUNT(*) as count FROM VisitExhibit WHERE Datetime = "%s"' % date]
            if name:
                query.append('Name = "%s"' % name)
            if visit_num_min and visit_num_max:
                query.append('GROUP BY Exhibitname HAVING COUNT(*) <= "%s" AND COUNT(*) >= "%s"' % (visit_num_max, visit_num_min))
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ExhibitHistoryTable(
                [ExhibitHistoryTable(name, time, num_of_visits) for name, time, num_of_visits in fetch])
            res = make_response(render_template('visitor_exhibit_history.html', form=form, table=table))
            res.set_cookie("visitor_exhibit_history_name", name)
            res.set_cookie("visitor_exhibit_history_date", date)
            res.set_cookie("visitor_exhibit_history_visit_num_max", visit_num_max)
            res.set_cookie("visitor_exhibit_history_visit_num_min", visit_num_min)
            return res
    return render_template("visitor_exhibit_history.html", form=form)


@login_required
@app.route("/visitor_show_history", methods=['GET', 'POST'])
def visitor_show_history():
    form = SearchShowsForm()
    table = ShowsTable([])
    if form.is_submitted():
        if form.sort.data:
            name = request.cookies.get("visitor_show_history_name") if request.cookies.get("visitor_show_history_name") else None
            time = request.cookies.get("visitor_show_history_time") if request.cookies.get("visitor_show_history_time") else None
            exhibit = request.cookies.get("visitor_show_history_exhibit") if request.cookies.get("visitor_show_history_exhibit") else None
            query = ['SELECT VisitShow.Showname, VisitShow.Showdate, Shows.LocateAt FROM VisitShow, Shows WHERE VisitShow.Showname = "%s"' % name]
            if time:
                query.append('VisitShow.Showname = Shows.Name')
            if exhibit:
                query.append('Shows.LocateAt = "%s"' % exhibit)
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            cur = db.get_db().cursor()
            cur.execute()
            fetch = cur.fetchall()
            table = ShowHistoryTable([ShowHistory(name, time, exhibit) for name, time, exhibit in fetch])
            res = make_response(render_template('visitor_show_history.html', form=form, table=table))
            return res
        elif form.search.data:
            name = form.name.data
            time = form.date.data
            exhibit = form.exhibit.data
            query = ['SELECT VisitShow.Showname, VisitShow.Showdate, Shows.LocateAt FROM VisitShow, Shows WHERE VisitShow.Showname = "%s"' % name]
            if time:
                query.append('VisitShow.Showname = Shows.Name')
            if exhibit:
                query.append('Shows.LocateAt = "%s"' % exhibit)
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute()
            fetch = cur.fetchall()
            table = ShowHistoryTable([ShowHistory(name, time, exhibit) for name, time, exhibit in fetch])
            res = make_response(render_template('visitor_show_history.html', form=form, table=table))
            res.set_cookie("visitor_show_history_name", name)
            res.set_cookie("visitor_show_history_date", time)
            res.set_cookie("visitor_show_history_exhibit", exhibit)
            return res
    return render_template("visitor_show_history.html", form=form)



### staff stuff
@app.route("/staff", methods=['GET', 'POST'])
@login_required
def staff():
    # print(type(current_user), dir(current_user))
    return render_template('staff.html')

# cookie good
@app.route("/staff_view_shows", methods=['GET', 'POST'])
@login_required
def staff_view_shows():
    form=StaffSearchShowsForm()
    if form.is_submitted():
        by=form.by.data
        direction=form.direction.data
        query = 'SELECT * FROM Shows WHERE Hostby = "%s"' % current_user.username
        query += " ORDER BY %s %s " % (by, direction)
    else:
        query = 'SELECT * FROM Shows WHERE Hostby = "%s"' % current_user.username
    cur = db.get_db().cursor()
    cur.execute(query)
    fetch = cur.fetchall()
    table = ShowsTable1([Show1(n, d, e) for n, d, e, _ in fetch])
    return render_template('staff_view_shows.html', form=form, table=table)

# cookie good
@app.route("/staff_search_animal", methods=['GET', 'POST'])
@login_required
def staff_search_animal():
    form = SearchAnimalForm()
    table = AnimalTable([])
    if form.is_submitted():
        if form.sort.data:
            if request.cookies.get("animal_name_staff"):
                form.name.data = request.cookies.get("animal_name_staff")
            if request.cookies.get("animal_species_staff"):
                form.species.data = request.cookies.get("animal_species_staff")
            name = form.name.data
            species = form.species.data
            age_min = form.age_min.data
            age_max = form.age_max.data
            exhibit = form.exhibit.data
            type = form.type.data
            by=form.by.data
            direction=form.direction.data
            query = ['SELECT * FROM Animal WHERE Type = "%s" AND Place = "%s"' % (type, exhibit)]
            if name:
                query.append('Name = "%s"' % name)
            if species:
                query.append('Species = "%s"' % species)
            if age_min:
                query.append('Age >= "%s"' % age_min)
            if age_max:
                query.append('Age <= "%s"' % age_max)
            query = " AND ".join(query)
            query += " ORDER BY %s %s " % (by, direction)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTable1([Animal(name, sp, t, age, ex) for name, sp, t, age, ex in fetch])
            res = make_response(render_template('staff_search_animal.html', form=form, table=table))
            return res
        elif form.search.data:
            name = form.name.data
            species = form.species.data
            age_min = form.age_min.data
            age_max = form.age_max.data
            exhibit = form.exhibit.data
            type = form.type.data
            query = ['SELECT * FROM Animal WHERE Type = "%s" AND Place = "%s"' % (type, exhibit)]
            if name:
                query.append('Name = "%s"' % name)
            if species:
                query.append('Species = "%s"' % species)
            if age_min:
                query.append('Age >= "%s"' % age_min)
            if age_max:
                query.append('Age <= "%s"' % age_max)
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTable1([Animal(name, sp, ex, age, t) for name, sp, t, age, ex in fetch])
            res = make_response(render_template('staff_search_animal.html', form=form, table=table))
            res.set_cookie("animal_name_staff", name)
            res.set_cookie("animal_species_staff", species)
            return res
        return render_template('staff_search_animal.html', form=form, table=table)
    return render_template('staff_search_animal.html', form=form, table=table)

# good
@app.route("/staff_animal_care/<string:name>/<string:species>", methods=['GET', 'POST'])
@login_required
def staff_animal_care(name, species):
    form = AnimalCareForm()
    table=AnimalCareTable([])
    cur = db.get_db().cursor()
    cur.execute("SELECT * FROM Animal WHERE Name = %s AND Species = %s", (name, species))
    fetch = cur.fetchone()
    name, species, type, age, exhibit = fetch
    if form.is_submitted():
        if form.sort.data:
            by = form.by.data
            direction = form.direction.data
            query = ['SELECT * FROM Note WHERE AnimalName = "%s" AND AnimalSpecies = "%s"' % (name, species)]
            query = " AND ".join(query)
            query += " ORDER BY %s %s " % (by, direction)
            print(query)
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalCareTable([AnimalCare(staff, time, note) for staff, _, _, time, note in fetch])
            form.name.data = name
            form.species.data = species
            form.type.data = type
            form.age.data = age
            form.exhibit.data = exhibit
            return render_template('staff_animal_care.html', form=form, table=table)
        elif form.log_notes.data:
            cur.execute("SELECT * FROM Animal WHERE Name = %s AND Species = %s", (name, species))
            fetch = cur.fetchone()
            name, species, type, age, exhibit = fetch
            note = form.notes.data
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                cur.execute('INSERT INTO Note VALUES(%s, %s, %s, %s, %s)', (current_user.username, name, species, time, note))
                flash("Add Note successful")
                print("successful")
            except IntegrityError as e:
                flash("Add show Failed!\n" + str(e.args[1]))
    form.name.data = name
    form.species.data = species
    form.type.data = type
    form.age.data = age
    form.exhibit.data = exhibit
    cur.execute("SELECT * FROM Note WHERE AnimalName = %s AND AnimalSpecies = %s", (name, species))
    fetch = cur.fetchall()
    print(fetch)
    table = AnimalCareTable([AnimalCare(staff,  time, note) for staff, _, _, time, note in fetch])
    return render_template('staff_animal_care.html', form=form, table=table)


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')


## admin stuff
@login_required
@app.route("/admin_view_staff", methods=['GET', 'POST'])
def admin_view_staff():
    table = StaffsTable([])
    form = AdminViewStaffForm()
    cur = db.get_db().cursor()
    if form.is_submitted():
        if form.sort.data:
            query = ['SELECT * FROM User WHERE Username in (select * from Staff)']
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            fetch = cur.fetchall()
            table = StaffsTable([Visitors(u, e) for u, e, _ in fetch])
            res = make_response(render_template("admin_view_staff.html", table=table, form=form))
            return res
    return render_template("admin_view_staff.html", table=table, form=form)


@login_required
@app.route("/admin_view_visitor", methods=['GET', 'POST'])
def admin_view_visitor():
    table = VisitorsTable([])
    form = AdminViewVisitorForm()
    cur = db.get_db().cursor()
    if form.is_submitted():
        if form.sort.data:
            query = ['SELECT * FROM User WHERE Username in (select * from Visitor)']
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            fetch = cur.fetchall()
            table = VisitorsTable([Visitors(u, e) for u, e, _ in fetch])
            res = make_response(render_template("admin_view_visitor.html", table=table, form=form))
            return res
    return render_template("admin_view_visitor.html", table=table, form=form)


@login_required
@app.route("/admin_view_show", methods=['GET', 'POST'])
def admin_view_show():
    table = ShowsTable([])
    form = AdminRemoveShowsForm()
    cur = db.get_db().cursor()
    if form.is_submitted():
        if form.sort.data:
            # print(form.search.data, form.remove.data)
            name = request.cookies.get("admin_view_show_name") if request.cookies.get("admin_view_show_name") else None
            exhibit = form.exhibit.data
            date = request.cookies.get("admin_view_show_date") if request.cookies.get("admin_view_show_date") else None
            print(name, type(name), len(name))

            query = ['SELECT Name, DateAndTime, LocateAt FROM Shows WHERE LocateAt = "%s"' % exhibit]
            if name:
                query.append('Name = "%s"' % name)
            if date:
                query.append('DateAndTime = "%s"' % date)
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            print(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ShowsTable([Show(a, b, c) for a, b, c in fetch])
            res = make_response(render_template('admin_view_show.html', form=form, table=table))
            return res

        elif form.search.data:
            name = form.name.data
            exhibit = form.exhibit.data
            date = form.date.data
            query = ['SELECT Name, DateAndTime, LocateAt FROM Shows WHERE LocateAt = "%s"' % exhibit]
            if name:
                query.append('Name = "%s"' % name)
            if date:
                query.append('DateAndTime = "%s"' % date)
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            print(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = ShowsTable([Show(a, b, c) for a, b, c in fetch])
            res = make_response(render_template('admin_view_show.html', form=form, table=table))
            res.set_cookie("admin_view_show_name", name)
            res.set_cookie("admin_view_show_date", date)
            res.set_cookie("admin_view_show_exhibit", exhibit)
            return res
    return render_template("admin_view_show.html", table=table, form=form)


@login_required
@app.route("/admin_view_animal", methods=['GET', 'POST'])
def admin_view_animal():
    form = SearchAnimalForm()
    table = AnimalTable([])
    if form.is_submitted():
        print(form.search.data)
        if form.sort.data:
            name = request.cookies.get("admin_view_animal_name") if request.cookies.get("admin_view_animal_name") else None
            species = request.cookies.get("admin_view_animal_species") if request.cookies.get("admin_view_animal_species") else None

            age_min = request.cookies.get("admin_view_animal_age_min") if request.cookies.get("admin_view_animal_age_min") else None
            age_max = request.cookies.get("admin_view_animal_age_max") if request.cookies.get("admin_view_animal_age_max") else None
            exhibit = form.exhibit.data
            type = form.type.data
            query = ['SELECT * FROM Animal WHERE Type = "%s" AND Place = "%s"' % (type, exhibit)]
            if name:
                query.append('Name = "%s"' % name)
            if species:
                query.append('Species = "%s"' % species)
            if age_min:
                query.append('Age >= "%s"' % age_min)
            if age_max:
                query.append('Age <= "%s"' % age_max)
            query = " AND ".join(query)
            query += " ORDER BY %s %s" % (form.by.data, form.direction.data)
            print(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTable([Animal(name, sp, ex, age, t) for name, sp, t, age, ex in fetch])
            res = make_response(render_template('admin_view_animal.html', form=form, table=table))
            return res
        elif form.search.data:
            name = form.name.data
            species = form.species.data
            age_min = form.age_min.data
            age_max = form.age_max.data
            exhibit = form.exhibit.data
            type = form.type.data
            query = ['SELECT * FROM Animal WHERE Type = "%s" AND Place = "%s"' % (type, exhibit)]
            if name:
                query.append('Name = "%s"' % name)
            if species:
                query.append('Species = "%s"' % species)
            if age_min:
                query.append('Age >= "%s"' % age_min)
            if age_max:
                query.append('Age <= "%s"' % age_max)
            query = " AND ".join(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTable([Animal(name, sp, ex, age, t) for name, sp, t, age, ex in fetch])
            res = make_response(render_template('admin_view_animal.html', form=form, table=table))
            res.set_cookie("admin_view_animal_name", name)
            res.set_cookie("admin_view_animal_species", species)
            res.set_cookie("admin_view_animal_age_min", age_min)
            res.set_cookie("admin_view_animal_age_max", age_max)
            res.set_cookie("admin_view_animal_exhibit", exhibit)
            res.set_cookie("admin_view_animal_type", type)
            return res
    return render_template("admin_view_animal.html", form=form)


# done
@login_required
@app.route("/admin_add_animal", methods=['GET', 'POST'])
def admin_add_animal():
    animal_form = AddAnimalForm()
    if animal_form.is_submitted():
        name = animal_form.name.data
        exhibit = animal_form.exhibit.data
        types = animal_form.type.data
        species = animal_form.species.data
        age = animal_form.age.data
        try:
            cur = db.get_db().cursor()
            cur.execute('INSERT INTO Animal VALUES(%s, %s, %s, %s, %s)', (name, species, types, age, exhibit))
        except Exception as e:
            flash("Add animal Failed!\n" + str(e.args[1]))
        return redirect(url_for('admin'))
    return render_template("admin_add_animal.html", form=animal_form)


# done
@login_required
@app.route("/admin_add_show", methods=['GET', 'POST'])
def admin_add_show():
    form = AddShowForm()
    if form.is_submitted():
        name = form.name.data
        staff = form.staff.data
        exhibit = form.exhibit.data
        date = form.date.data
        try:
            cur = db.get_db().cursor()
            cur.execute('INSERT INTO Shows VALUES(%s, %s, %s, %s)', (name, date, exhibit, staff))
            flash("Add show successful")
        except IntegrityError as e:
            flash("Add show Failed!\n" + str(e.args[1]))
        return redirect(url_for('admin'))
    return render_template("admin_add_show.html", form=form)


@login_required
@app.route("/showdelete/<string:id>/<string:id1>", methods=['GET', 'POST'])
def showdelete(id, id1):
     cur = db.get_db().cursor()
     cur.execute('Delete FROM Shows where Name=%s and DateAndTime=%s',(id, id1))
     # flash("Delete successful")
     return redirect(url_for("admin_view_show"))

@login_required
@app.route("/delete_animal/<string:id>/<string:id1>", methods=['GET', 'POST'])
def delete_animal(id,id1):
     cur = db.get_db().cursor()
     cur.execute('Delete FROM Animal where Name=%s and Species=%s', (id, id1))
     return redirect(url_for("admin_view_animal"))

@login_required
@app.route("/visitordelete/<string:id>", methods=['GET', 'POST'])
def visitordelete(id):
    cur = db.get_db().cursor()
    cur.execute('Delete FROM Visitor where Username=%s', id)
    cur.execute('Delete FROM User where Username=%s', id)
    return redirect(url_for('admin_view_visitor'))

@login_required
@app.route("/staffdelete/<string:id>", methods=['GET', 'POST'])
def staffdelete(id):
    cur = db.get_db().cursor()
    cur.execute('Delete FROM Staff where Username=%s', id)
    cur.execute('Delete FROM User where Username=%s', id)
    return redirect(url_for('admin_view_staff'))
