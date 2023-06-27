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
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        try:
            myCursor.execute("SELECT * FROM grocery_store.user WHERE username = %s AND password = %s", (username, password))
            user = myCursor.fetchone()
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the query: ", error)


        if user:
            if user[3] == 'admin':
                return redirect(url_for('admin_home_page'))
            elif user[3] == 'manager':
                return redirect(url_for('manager_home_page'))
            elif user[3] == 'employee':
                return redirect(url_for('employee_home_page'))
            elif user[3] == 'customer':
                return redirect(url_for('customer_home_page'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
        return render_template('admin_home_page.html')
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

        # getting userID 
        try:
            myCursor.execute("SELECT * FROM grocery_store.user ORDER BY user_ID DESC");
            users = myCursor.fetchall()
            userID = users[0][0]
            myConnection.commit()
        except Exception as error:
            print("An error occurred while executing the FIRST query: ", error)


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
            # myCursor.execute("INSERT INTO grocery_store.customer (user_ID, personal_information_ID)", (userID, PID))

            return redirect(url_for('customer_home_page'))
        except Exception as error:
            print("An error occurred while executing the query: ", error)
            
        return render_template('customer_form.html')
    else:
        return render_template('customer_form.html')


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    return render_template('login.html')


@app.route("/customer_home_page", methods=['POST', 'GET'])
def customer_home_page():
    return render_template('customer_home_page.html')


@app.route("/employee_home_page", methods=['POST', 'GET'])
def employee_home_page():
    return render_template('employee_home_page.html')


@app.route("/manager_home_page", methods=['POST', 'GET'])
def manager_home_page():
    return render_template('manager_home_page.html')


@app.route("/admin_home_page", methods=['POST', 'GET'])
def admin_home_page():
    return render_template('admin_home_page.html')


if __name__ == '__main__':
    app.run(debug=True)
    myConnection.commit()
    myCursor.close()
    myConnection.close()