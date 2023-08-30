from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__, static_url_path='/static')
app.secret_key = '7388bb75420f83b9b0f0a8b5377dc9cb'

def insert_user_data(data):
    
        try:
            # Configure database connection
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }

            # Connect to the database
            connection = mysql.connector.connect(**db_config)

            # Create a cursor object
            cursor = connection.cursor()

            # Insert data into the table
            insert_query = "INSERT INTO users (full_name, phone, email, password, college_id, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, data)
            
            # Commit the changes and close the cursor and connection
            connection.commit()
            cursor.close()
            connection.close()
            
            return True

        except mysql.connector.Error as e:
            print("Error:", e)
            return False


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        college_id = request.form['college_id']
        gender = request.form['gender']
        
        hashed_password = generate_password_hash(password)
        
        data = (full_name, phone, email, hashed_password, college_id, gender)
        
        if insert_user_data(data):
            return "User data inserted successfully."
        else:
            return "Failed to insert user data."

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Connect to the database
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            # Fetch the user's hashed password from the database based on the provided email
            select_query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            
            if result:
                hashed_password = result[0]
                if check_password_hash(hashed_password, password):
                    session['email'] = email
                    cursor.close()
                    connection.close()
                    return redirect(url_for('dashboard'))
                else:
                    cursor.close()
                    connection.close()
                    return "Invalid credentials"
            else:
                cursor.close()
                connection.close()
                return "User not found"
        
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return "Database error"

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # Fetch user data from the database based on the email in the session
        email = session['email']

        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "canteen"
            }
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            select_query = "SELECT full_name, phone, college_id, gender FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()

            if user_data:
                full_name, phone, college_id, gender = user_data
                return render_template('dashboard.html', full_name=full_name, phone=phone, college_id=college_id, gender=gender)
            else:
                return "User data not found."

        except mysql.connector.Error as e:
            print("Error:", e)
            return "Failed to fetch user data."

    else:
        return redirect(url_for('index'))
    
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'email' in session:
        if request.method == 'POST':
            full_name = request.form['full_name']
            phone = request.form['phone']
            college_id = request.form['college_id']
            email = session['email']

            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "canteen"
                }
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                update_query = "UPDATE users SET full_name = %s, phone = %s, college_id = %s WHERE email = %s"
                cursor.execute(update_query, (full_name, phone, college_id, email))
                connection.commit()

                cursor.close()
                connection.close()

                return redirect(url_for('dashboard'))

            except mysql.connector.Error as e:
                print("Error:", e)
                return "Failed to update user data."

        else:
            email = session['email']
            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "canteen"
                }
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                select_query = "SELECT full_name, phone, college_id, gender FROM users WHERE email = %s"
                cursor.execute(select_query, (email,))
                user_data = cursor.fetchone()

                cursor.close()
                connection.close()

                if user_data:
                    full_name, phone, college_id, gender = user_data
                    return render_template('edit_profile.html', full_name=full_name, phone=phone, college_id=college_id, gender=gender)
                else:
                    return "User data not found."

            except mysql.connector.Error as e:
                print("Error:", e)
                return "Failed to fetch user data."

    else:
        return redirect(url_for('index'))
@app.route('/logout')
def logout():
   
    session.clear()
    return redirect(url_for('index')) 

@app.route('/property_list2')
def property_list2():
    return render_template('property_list2.html')

@app.route('/property_list1')
def property_list1():
    return render_template('property_list1.html')

@app.route('/property_list3')
def property_list3():
    return render_template('property_list3.html')

@app.route('/property_list4')
def property_list4():
    return render_template('property_list4.html')

@app.route('/property_list5')
def property_list5():
    return render_template('property_list5.html')

@app.route('/index_after_login')
def index_after_login():
    return render_template('index_after_login.html')

@app.route('/properties_list1_after_login')
def properities_list1_after_login():
    return render_template('properties_list1_after_login.html')

@app.route('/property_list2_after_login')
def property_list2_after_login():
    return render_template('property_list2_after_login.html')

@app.route('/property_list3_after_login')
def property_list3_after_login():
    return render_template('property_list3_after_login.html')



if __name__ == '__main__':
    app.run(debug=True)



