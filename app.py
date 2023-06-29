import mysql.connector
from mysql.connector import connect
from flask import Flask, render_template, request, redirect, session, url_for, flash, app, make_response
app = Flask(__name__)
app.secret_key = 'my_secret_key'


# LOCAL CONNECTION
try: 
    myConnection = mysql.connector.connect(host="localhost", user="root", passwd="Password123$", database="grocery_store")
    myCursor = myConnection.cursor()
    print("Connected to database")
except Exception as error:
    print("An error occurred while connecting: ", error)


@app.route("/")
def index():
    return render_template('admin_create_manager.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        try:
            # check to see if the username and password are in the database
            myCursor.execute("SELECT * FROM grocery_store.user WHERE username = %s AND password = %s", (username, password))
            user = myCursor.fetchone()
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the query: ", error)


        if user:
            session['user_ID'] = user[0]
            if user[3] == 'admin':
                return redirect(url_for('admin_home', user_ID=user[0]))
            elif user[3] == 'manager':
                return redirect(url_for('manager_home', user_ID=user[0]))
            elif user[3] == 'employee':
                return redirect(url_for('employee_home', user_ID=user[0]))
            elif user[3] == 'customer':
                return redirect(url_for('customer_home', user_ID=user[0]))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    else:
        return render_template('login.html')
    

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # gather information from the POST
        username = request.form['username']
        password = request.form['password']

        # check to see if the username is already in the database
        try:
            myCursor.execute("SELECT * FROM grocery_store.user WHERE username = %s", (username,))
            user = myCursor.fetchone()
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the query: ", error)

        if user:
            flash('Username already taken')
            return render_template('register.html')
        else:
            # add the user to the database
            try:
                myCursor.execute("INSERT INTO grocery_store.user (username, password, role) VALUES (%s, %s, 'customer')", (username, password))
                myConnection.commit()
            except Exception as error:
                print("An error occurred while executing the query: ", error)
        
            # redirect to the form
            return redirect(url_for('customer_form'))
    else:
        return render_template('register.html')


@app.route("/customer_form", methods=['POST', 'GET'])
def customer_form():
    if request.method == 'POST':
        # gather information from the POST
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']

        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        int_zip_code = int(zip_code)

        # changing the date format
        new_date_of_birth = date_of_birth[-4:] + "-" + date_of_birth[0:2] + "-" + date_of_birth[3:5]

        # getting user_ID 
        try:
            myCursor.execute("SELECT * FROM grocery_store.user ORDER BY user_ID DESC");
            users = myCursor.fetchall()
            user_ID = users[0][0]
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the query: ", error)


        try:
            # inserting the address into the database
            myCursor.execute("INSERT INTO grocery_store.address (street_address, city, state, zip) VALUES (%s, %s, %s, %s)", (street_address, city, state, int_zip_code))
            myConnection.commit()


            # getting addressID
            myCursor.execute("SELECT * FROM grocery_store.address ORDER BY address_ID DESC");
            addresses = myCursor.fetchall()
            addressID = addresses[0][0]
            myConnection.commit()


            # inserting personal information into the database
            myCursor.execute("INSERT INTO grocery_store.personal_information (address_ID, name, DOB, phone_number) VALUES (%s, %s, %s, %s)", (addressID, name, new_date_of_birth, phone_number))
            myConnection.commit()

            # # inserting customer into the database
            # myCursor.execute("INSERT INTO grocery_store.customer (user_ID, personal_information_ID)", (user_ID, PID))

            return redirect(url_for('customer_home'))
        except Exception as error:
            print("An error occurred while executing the query: ", error)
            
        return render_template('customer_form.html')
    else:
        return render_template('customer_form.html')


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    return render_template('login.html')


@app.route("/customer_home", methods=['POST', 'GET'])
def customer_home():
    user_ID = session['user_ID']
    return render_template('customer_home.html', user_ID=user_ID)


@app.route("/employee_home", methods=['POST', 'GET'])
def employee_home():
    return render_template('employee_home.html')


@app.route("/manager_home", methods=['POST', 'GET'])
def manager_home():
    return render_template('manager_home.html')


@app.route("/admin_home", methods=['POST', 'GET'])
def admin_home():
    return render_template('admin_home.html')


@app.route("/admin_create_manager", methods=['POST', 'GET'])
def admin_create_manager():
    if request.method == 'POST':
        # gather information 
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']
        phone_number = request.form['phone_number']
        street_address = request.form['street_address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        int_zip_code = int(zip_code)
        wage = request.form['wage']

        # changing the date format
        new_date_of_birth = date_of_birth[-4:] + "-" + date_of_birth[0:2] + "-" + date_of_birth[3:5]

        # creating user
        try:
            myCursor.execute("INSERT INTO grocery_store.user (username, password, role) VALUES (%s, %s, 'manager')", (username, password))
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the user query: ", error)

        # getting user_ID
        try:
            myCursor.execute("SELECT * FROM grocery_store.user ORDER BY user_ID DESC");
            users = myCursor.fetchall()
            user_ID = users[0][0]
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the userID query: ", error)

        # creating address
        try:
            myCursor.execute("INSERT INTO grocery_store.address (street_address, city, state, zip) VALUES (%s, %s, %s, %s)", (street_address, city, state, int_zip_code))
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the address query: ", error)

        # getting addressID
        try:
            myCursor.execute("SELECT * FROM grocery_store.address ORDER BY address_ID DESC");
            addresses = myCursor.fetchall()
            addressID = addresses[0][0]
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the addressID query: ", error)

        # creating personal information
        try:
            myCursor.execute("INSERT INTO grocery_store.personal_information (address_ID, name, DOB, phone_number) VALUES (%s, %s, %s, %s)", (addressID, name, new_date_of_birth, phone_number))
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the personal information query: ", error)

        # creating a schedule # FIX THIS
        try:
            myCursor.execute("INSERT INTO grocery_store.schedule (time) VALUES (%s)", (0))
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the schedule query: ", error)

        # creating an employee
        try:
            myCursor.execute("INSERT INTO grocery_store.employee (user_ID, personal_information_ID, schedule_ID, wage, title) VALUES (%s, %s, %s, %s)", (user_ID, addressID, 0, wage, 'manager'))
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the employee query: ", error)

    return render_template('admin_create_manager.html')


@app.route("/admin_create_employee", methods=['POST', 'GET'])
def admin_create_employee():
    return render_template('admin_create_employee.html')


@app.route("/admin_delete_manager", methods=['POST', 'GET'])
def admin_delete_manager():
    return render_template('admin_delete_manager.html')

@app.route("/admin_delete_employee", methods=['POST', 'GET'])
def admin_delete_employee():
    return render_template('admin_delete_employee.html')

if __name__ == '__main__':
    app.run(debug=True)
    myConnection.commit()
    myCursor.close()
    myConnection.close()