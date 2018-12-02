from LoginDemoApp import app, db, bcrypt, serializer
from LoginDemoApp.database_tables import load_user, User
from flask import render_template, url_for, flash, Markup, redirect, request, make_response
from flask_login import login_user, current_user, logout_user, login_required
from pymysql.err import IntegrityError
from LoginDemoApp.table import *
import hashlib


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


@login_required
@app.route("/exhibit_detail/<string:id>", methods=['GET', 'POST'])
def exhibit_detail(id):
    form = ExhibitDetail()
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM Exhibit WHERE Name = "%s"' % id)
    fetch = cur.fetchone()
    name, is_water, size = fetch
    cur.execute('SELECT * FROM Animal WHERE Place = "%s"' % id)
    animals = cur.fetchall()
    num_animals = len(animals)
    form.name.data = name
    form.size.data = size
    form.water_feature.data = "YES" if int(is_water) else "NO"
    form.num_animals.data = num_animals
    print(animals)
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
        name = form.name.data
        size_min = form.size_min.data
        size_max = form.size_max.data
        animal_max = form.animal_max.data
        animal_min = form.animal_min.data
        water_feature = 1 if form.water_feature.data else 0
        print(size_min, size_max, animal_max, animal_min, water_feature)
        cur = db.get_db().cursor()
        cur.execute(
            'SELECT Exhibit.Name, Exhibit.Size, COUNT(*) as count, Exhibit.WaterFeature FROM Exhibit, Animal WHERE Exhibit.Size <= %s AND Exhibit.Size >= %s AND Exhibit.WaterFeature = %s AND Animal.Place = Exhibit.Name GROUP BY Animal.Place HAVING COUNT(*) >= %s AND COUNT(*) <= %s',
            (size_max, size_min, water_feature, animal_min, animal_max))
        fetch = cur.fetchall()
        print(fetch)
        table = ExhibitsTable(
            [Exhibit(name, size, num_animals, ("YES" if int(water) else "NO")) for name, size, num_animals, water in
             fetch])
        return render_template('visitor_search_exhibit.html', form=form, table=table)
    return render_template("visitor_search_exhibit.html", form=form, table=table)


# good
@login_required
@app.route("/visitor_search_animal", methods=['GET', 'POST'])
def visitor_search_animal():
    form = SearchAnimalForm()
    if form.is_submitted():
        if form.sort.data:
            if request.cookies.get("animal_name"):
                form.name.data = request.cookies.get("animal_name")
            if request.cookies.get("animal_species"):
                form.species.data = request.cookies.get("animal_species")
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
            query += "ORDER BY Age ASC"
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
            res.set_cookie("animal_name", name)
            res.set_cookie("animal_species", species)
            return res
    return render_template("visitor_search_animal.html", form=form)


@login_required
@app.route("/visitor_search_show", methods=['GET', 'POST'])
def visitor_search_show():
    form = SearchShowsForm()
    if form.is_submitted():
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
        print(fetch)
        table = ShowsTable1([Show1(name, str(date), ex) for name, date, ex, _ in fetch])
        return render_template('visitor_search_show.html', form=form, table=table)
    return render_template("visitor_search_show.html", form=form)


@login_required
@app.route("/visitor_exhibit_history", methods=['GET', 'POST'])
def visitor_exhibit_history():
    form = SearchExhibitsHistoryForm()
    table = ExhibitsTable([])
    if form.is_submitted():
        name = form.name.data
        date = form.date.data
        visit_num_max = form.visit_num_max.data
        visit_num_min = form.visit_num_min.data
        # print(visit_num_max)
        # print(visit_num_min)
        cur = db.get_db().cursor()
        cur.execute(
            'SELECT VisitExhibit.Exhibitname, VisitExhibit.Datetime, COUNT(*) as count FROM VisitExhibit WHERE Datetime = %s GROUP BY Exhibitname HAVING COUNT(*) <= %s AND COUNT(*) >= %s',
            (date, visit_num_max, visit_num_min))
        fetch = cur.fetchall()
        table = ExhibitHistoryTable(
            [ExhibitHistoryTable(name, time, num_of_visits) for name, time, num_of_visits in fetch])
        return render_template('visitor_exhibit_history.html', form=form, table=table)
    return render_template("visitor_exhibit_history.html", form=form, table=table)


@login_required
@app.route("/visitor_show_history", methods=['GET', 'POST'])
def visitor_show_history():
    form = SearchShowsForm()
    table = ShowsTable([])
    if form.is_submitted():
        name = form.name.data
        time = form.date.data
        exhibit = form.exhibit.data
        cur = db.get_db().cursor()
        cur.execute(
            'SELECT VisitShow.Showname, VisitShow.Showdate, Shows.LocateAt FROM VisitShow, Shows WHERE VisitShow.Showname = %s AND Shows.LocateAt = %s AND VisitShow.Showname = Shows.Name',
            (name, exhibit))
        fetch = cur.fetchall()
        table = ShowHistoryTable([ShowHistory(name, time, exhibit) for name, time, exhibit in fetch])
        return render_template('visitor_show_history.html', form=form, table=table)
    return render_template("visitor_show_history.html", form=form, table=table)


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
    table = ShowsTable1([Show1(n, d, e) for n, d, e, _ in fetch])
    return render_template('staff_view_shows.html', table=table)


@app.route("/staff_search_animal", methods=['GET', 'POST'])
@login_required
def staff_search_animal():
    form = SearchAnimalForm()
    table = AnimalTable([])
    if form.is_submitted():
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
        table = AnimalTable1([Animal(name, sp, t, age, ex) for name, sp, t, age, ex in fetch])
        return render_template('staff_search_animal.html', form=form, table=table)
    return render_template('staff_search_animal.html', form=form, table=table)


@app.route("/staff_animal_care/<string:name>/<string:species>", methods=['GET', 'POST'])
@login_required
def staff_animal_care(name, species):
    form = AnimalCareForm()

    cur = db.get_db().cursor()
    cur.execute("SELECT * FROM Animal WHERE Name = %s AND Species = %s", (name, species))
    fetch = cur.fetchone()
    name, species, type, age, exhibit = fetch
    form.name.data = name
    form.species.data = species
    form.type.data = type
    form.age.data = age
    form.exhibit.data = exhibit

    cur.execute("SELECT * FROM Note WHERE AnimalName = %s AND AnimalSpecies = %s", (name, species))
    fetch = cur.fetchall()
    print(fetch)
    table = AnimalCareTable([AnimalCareTable(staff, note, time) for staff, _, _, time, note in fetch])
    # table = AnimalCareTable([ExhibitsTable(name, size, num_animals, water) for name, size, num_animals, water in fetch])

    if form.is_submitted():
        flash('Log nothing')
    return render_template('staff_animal_care.html', form=form, table=table)


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html')


# @app.route("/hidden_back", methods=['GET', 'POST'])
# @login_required
# def hidden_back():
#     if current_user.usertype == "staff":
#         return redirect(url_for('staff.html'))


## admin stuff
@login_required
@app.route("/admin_view_staff", methods=['GET', 'POST'])
def admin_view_staff():
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM User WHERE Username in (select * from Staff)')
    fetch = cur.fetchall()
    table = StaffsTable([Staffs(u, e) for u, e, _ in fetch])
    form = RemoveForm()
    return render_template("admin_view_staff.html", table=table, form=form)


@login_required
@app.route("/admin_view_visitor", methods=['GET', 'POST'])
def admin_view_visitor():
    cur = db.get_db().cursor()
    cur.execute('SELECT * FROM User WHERE Username in (select * from Visitor)')
    fetch = cur.fetchall()
    table = VisitorsTable([Visitors(u, e) for u, e, _ in fetch])
    form = RemoveForm()
    return render_template("admin_view_visitor.html", table=table, form=form)


@login_required
@app.route("/admin_view_show", methods=['GET', 'POST'])
def admin_view_show():
    table = ShowsTable([])
    form = AdminRemoveShowsForm()
    cur = db.get_db().cursor()
    if form.is_submitted():
        # print(form.search.data, form.remove.data)
        name = form.name.data
        exhibit = form.exhibit.data
        date = form.date.data
        print(name, type(name), len(name))
        if form.search.data:
            if name == "" and date is None:
                cur.execute('SELECT Name, DateAndTime, LocateAt FROM Shows WHERE LocateAt = "%s"' % exhibit)
            elif name == "" and date is not None:
                cur.execute('SELECT Name, DateAndTime, LocateAt FROM Animal WHERE LocateAt = %s AND DateAndTime = %s', (exhibit, date))
            elif name != "" and date is None:
                cur.execute('SELECT Name, DateAndTime, LocateAt FROM Animal WHERE LocateAt = %s AND Name = %s', (exhibit, name))
            elif name != "" and date is not None:
                cur.execute('SELECT Name, DateAndTime, LocateAt FROM Animal WHERE LocateAt = %s AND Name = %s And DateAndTime = %s',(exhibit, name, date))
            fetch = cur.fetchall()
            print(fetch)
            table = ShowsTable([Show(a, b, c) for a, b, c in fetch])
    return render_template("admin_view_show.html", table=table, form=form)


@login_required
@app.route("/admin_view_animal", methods=['GET', 'POST'])
def admin_view_animal():
    form = SearchAnimalForm()
    table = AnimalTable([])
    if form.is_submitted():
        print(form.search.data)
        if form.search.data:
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
            print(query)
            cur = db.get_db().cursor()
            cur.execute(query)
            fetch = cur.fetchall()
            table = AnimalTabledelete([Animaldelete(name, sp, t, age, ex) for name, sp, t, age, ex in fetch])
            return render_template('admin_view_animal.html', form=form, table=table)
        elif form.remove.data:
            pass  # todo: remove data
    return render_template("admin_view_animal.html", form=form, table=table)


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
