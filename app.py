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
    return render_template('register.html')


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