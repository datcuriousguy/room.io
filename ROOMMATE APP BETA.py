from datetime import datetime

from mysql.connector import cursor
import mysql
from flask import Flask, request, jsonify
from flask_cors import CORS

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hayabusa@2004",
    database="roommate"
)

cur = db_connection.cursor()

cur.execute('DESC student_info')

for row in cur.fetchall():
    print(row)

app = Flask(__name__)
CORS(app)


# This function is supplied to accept the entered university email id from the webpage (roommate_beta.html)
#it does this by being called by a line of code in the roommate_beta.js file.z

def check_user_and_password(university_email_id, password):
    try:

        # Query to check if username exists
        cur.execute('use roommate;')
        query_user = "SELECT COUNT(*) FROM student_info WHERE university_email = %s"
        cur.execute(query_user, (university_email_id,))
        user_exists = cur.fetchone()[0] > 0

        # Query to check if the username and password match
        query_password = "SELECT COUNT(*) FROM user WHERE user_name = %s AND user_password = %s"
        cur.execute(query_password, (university_email_id, password))
        password_correct = cur.fetchone()[0] > 0

        cur.close()
        db_connection.close()

        # Log the login attempt
        with open('LOGIN_HISTORY.txt', 'a+') as login_history_file:
            login_record = f'User {university_email_id} logged in at {datetime.datetime.now()}\n\n'
            login_history_file.write(login_record)

        return user_exists, password_correct

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False, False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False, False


@app.route('/api/check-user-password', methods=['POST'])
def check_user_password():
    """
    Check if a user's password is correct.

    Returns:
        JSON response: Whether the user exists and if the password is correct.
    """
    data = request.get_json()
    university_email_id = data['university_email_id']
    password = data['password']

    user_exists, password_correct = check_user_and_password(university_email_id, password)

    return jsonify({'exists': user_exists, 'password_correct': password_correct})


if __name__ == '__main__':
    app.run()
