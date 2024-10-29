"""


 • This is the backend of the ROOMMATE-ALLOCATION application.
 • Please note that the front-end, login, etc. are still under construction.


"""

from datetime import datetime
import time
from mysql.connector import cursor
import mysql
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_connection = mysql.connector.connect(
    host="localhost",
    user="your_mysql_username",
    password="your_mysql_password",
    database="roommate_app"
)

cur = db_connection.cursor()


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#
#     print(f'username: {username}')
#     print(f'password: {password}')
#     print(verify_username_password(username, password))
#
#     return username, password


# def verify_username_password(username, password):
#
#     statement = f"SELECT university_email, password FROM student_info WHERE university_email = {username};"
#     check_db_for_credentials = cur.execute(statement)
#
#     print(check_db_for_credentials[0])
#     print(check_db_for_credentials[1])

"""
OCTOBER 29TH 2024:
  I have added GET and POST methods for most functions for redundancy though any one of GET or  POST could be used.
  
  """

# @app.route('/get_student_ids_by_gender', methods=['GET', 'POST'])
def get_student_ids_by_gender(gender):
    student_ids_of_gender = cur.execute(
        f"SELECT student_id, first_name, last_name FROM student_info WHERE gender = '{gender}';'")
    student_ids_of_gender_fetchall = cur.fetchall()
    student_ids_of_chosen_gender = student_ids_of_gender_fetchall
    student_ids_of_chosen_gender_list = []
    for student_id_of_chosen_gender in student_ids_of_chosen_gender:
        student_ids_of_chosen_gender_list.append(student_id_of_chosen_gender)
        #print(student_id_of_chosen_gender)
    # I used this line for testing the function in isolation: print(student_ids_of_chosen_gender_list)
    return student_ids_of_chosen_gender_list


@app.route('/get_student_id_by_bedtime_preference', methods=['GET', 'POST'])
def get_student_id_by_bedtime_preference(gender, bedtime_preference):

    db_connection = mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="roommate_app"
    )

    cur = db_connection.cursor()
    student_info = get_student_ids_by_gender(gender)
    print(f'Students with bedtime {bedtime_preference}:00\n\nStudent_id | Name\n\n')
    for student_info_row in student_info:
        student_info_row_id = student_info_row[0]
        student_info_row_first_name = student_info_row[1]
        student_info_row_last_name = student_info_row[2]
        db_statement = f"SELECT * FROM student_id_bedtime_preference_map where student_id = {student_info_row_id} AND bedtime_preference = {bedtime_preference};"
        cur.execute(db_statement)
        student_info_row_fetchall = cur.fetchall()
        for student_info_row_fetchall_row in student_info_row_fetchall:
            print(f'{student_info_row_id} | {student_info_row_first_name} {student_info_row_last_name}')

        # student_ids_with_specified_bedtime_fetchall = cur.fetchall()
        # print(student_ids_with_specified_bedtime_fetchall)
        # for student_id in student_ids_with_specified_bedtime_fetchall:
        #     print(f'{student_ids[0]} {student_ids[1]} prefers bedtime {bedtime_preference}.')
        return student_info_row_fetchall


@app.route('/get_student_id_by_ac_fan_preference', methods=['GET', 'POST'])
def get_student_id_by_ac_fan_preference(gender, ac_fan_preference):
    """
        add if statement to use conditions:

        'ac'                  (=1)
        'fan'                 (=1)
        'ac and fan'          (both = 1)
        'none of ac and fan'  (=0)

        ... for the function

        get_student_id_by_ac_fan_preference()
        """

    """
    The 4 possible calls of get_student_id_by_ac_fan_preference(ac_fan_preference) are:

        get_student_id_by_ac_fan_preference(('ac', ''))
        get_student_id_by_ac_fan_preference(('', 'fan'))
        get_student_id_by_ac_fan_preference(('ac', 'fan'))
        get_student_id_by_ac_fan_preference(('', ''))

    """

    db_connection = mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="roommate_app"
    )

    cur = db_connection.cursor()

    if ac_fan_preference == ('ac', 'fan'):
        print('Students Using Both A/C & Fan:\n\n')
        student_info = get_student_ids_by_gender(gender)

        for student_info_row in student_info:
            student_info_row_id = student_info_row[0]
            student_info_row_first_name = student_info_row[1]
            student_info_row_last_name = student_info_row[2]

            db_connection = mysql.connector.connect(
                host="localhost",
                user="your_mysql_username",
                password="your_mysql_password",
                database="roommate_app"
            )

            cur = db_connection.cursor()
            student_ids = cur.execute(
                f'SELECT student_id FROM student_id_ac_fan_map WHERE {ac_fan_preference[0]} = 1 AND {ac_fan_preference[1]} = 1 AND student_id = {student_info_row_id};')
            student_ids = cur.fetchall()
            for student_id in student_ids:
                print(f'{student_info_row_id} | {student_info_row_first_name} {student_info_row_last_name}')
        cur.close()

    elif ac_fan_preference == ('ac', ''):

        print('Students Using Only A/C:\n\n')

        student_info = get_student_ids_by_gender(gender)

        for student_info_row in student_info:
            student_info_row_id = student_info_row[0]
            student_info_row_first_name = student_info_row[1]
            student_info_row_last_name = student_info_row[2]

            db_connection = mysql.connector.connect(
                host="localhost",
                user="your_mysql_username",
                password="your_mysql_password",
                database="roommate_app"
            )
            cur = db_connection.cursor()
            statement = f'SELECT student_id FROM student_id_ac_fan_map WHERE ac = 1 AND fan = 0 AND student_id = {student_info_row_id};'
            student_ids = cur.execute(
                statement)
            # print(statement) used to diagnose errors with the statement.
            student_ids = cur.fetchall()
            for student_id in student_ids:
                print(f'{student_info_row_id} | {student_info_row_first_name} {student_info_row_last_name}')
        cur.close()



    elif ac_fan_preference == ('', 'fan'):
        print('Students Using Only Fans:\n\n')
        student_info = get_student_ids_by_gender(gender)
        for student_info_row in student_info:

            student_info_row_id = student_info_row[0]
            student_info_row_first_name = student_info_row[1]
            student_info_row_last_name = student_info_row[2]

            db_connection = mysql.connector.connect(
                host="localhost",
                user="your_mysql_username",
                password="your_mysql_password",
                database="roommate_app"
            )

            cur = db_connection.cursor()
            student_ids = cur.execute(
                f'SELECT student_id FROM student_id_ac_fan_map WHERE ac = 0 AND fan = 1 AND student_id = {student_info_row_id};')
            student_ids = cur.fetchall()
            for student_id in student_ids:
                print(f'{student_info_row_id} | {student_info_row_first_name} {student_info_row_last_name}')
        cur.close()


    else:
        print('Students Using Neither A/C Nor Fan:\n\n')
        student_info = get_student_ids_by_gender(gender)
        for student_info_row in student_info:

            student_info_row_id = student_info_row[0]
            student_info_row_first_name = student_info_row[1]
            student_info_row_last_name = student_info_row[2]

            db_connection = mysql.connector.connect(
                host="localhost",
                user="your_mysql_username",
                password="your_mysql_password",
                database="roommate_app"
            )

            cur = db_connection.cursor()
            student_ids = cur.execute(
                f'SELECT student_id FROM student_id_ac_fan_map WHERE ac = 0 AND fan = 0 AND  student_id = {student_info_row_id};')
            student_ids = cur.fetchall()
            for student_id in student_ids:
                print(f'{student_info_row_id} | {student_info_row_first_name} {student_info_row_last_name}')
        cur.close()

        # student_ids = cur.execute(
        #                 f'SELECT student_id FROM student_id_ac_fan_map WHERE ac = 0 AND fan = 0 AND student_id = {student_info_row_id};')


# function to search students who have both an ac and fan preference:

@app.route('/get_student_id_by_ac_preference_fan_preference', methods=['GET', 'POST'])
def get_student_id_by_ac_temp(gender, ac_temp_preference):
    """
    ac_temp = int
    function call would look like:

    get_student_id_by_ac_temp(20)

    ^where 20 is the ac_temp_preference

    (ac_temp_preference is a column name in the table student_id_ac_temp_fan_speed_map)
    """
    student_info = get_student_ids_by_gender(gender)
    for student_info_row in student_info:
        student_info_row_id = student_info_row[0]
        student_info_row_first_name = student_info_row[1]
        student_info_row_last_name = student_info_row[2]

        db_connection = mysql.connector.connect(
            host="localhost",
            user="your_mysql_username",
            password="your_mysql_password",
            database="roommate_app"
        )

        cur = db_connection.cursor()
        student_ids = cur.execute(
            f'SELECT student_id, ac_temp_preference, fan_speed_preference FROM student_id_ac_temp_fan_speed_map WHERE ac_temp_preference = {ac_temp_preference} AND student_id = {student_info_row_id};')
        student_ids_fetchall = cur.fetchall()
        for student_id in student_ids_fetchall:
            first_name_query = cur.execute(f'select first_name from student_info where student_id = {student_id[0]}')
            first_name = cur.fetchall()[0][0]
            last_name_query = cur.execute(f'select last_name from student_info where student_id = {student_id[0]}')
            last_name = cur.fetchall()[0][0]
            # last_name = cur.execute(f'select last_name from student_info where student_id = {student_id[0]}')
            # student_name = f"{first_name} {last_name}"
            # student_name = f"{first_name}"
            ac_temp_preference_in_db = student_id[1]
            fan_speed_preference_in_db = student_id[2]
            print(
                f'{first_name} {last_name}\n____________________________\nAC Temperature Preference: {ac_temp_preference_in_db}℃\nFan Speed Preference: {fan_speed_preference_in_db}\n\n')
        cur.close()


@app.route('/select_roommate_preference', methods=['GET', 'POST'])
def select_roommate_preference(student_id, roommate_id, room_number):
    """
    Calling this function would look like:

    select_roommate_preference(105, 117, 1108)

    ^where 105 is the student_id of the preferred roommate.

    :param student_id: student_id, roommate_id
    :return:
    updates the room_student_map table:

    +-------------+------+------+-----+---------+-------+
    | Field       | Type | Null | Key | Default | Extra |
    +-------------+------+------+-----+---------+-------+
    | student2_id | int  | NO   |     | NULL    |       |
    | student1_id | int  | NO   |     | NULL    |       |
    | room_number | int  | NO   | PRI | NULL    |       |
    +-------------+------+------+-----+---------+-------+

    with:
        student2_id -> student_id
        student1_id -> roommate_id
        room_number -> room_number
    """


"""
    /// / /  /  /   /   /    /    /     /     M I N I  -  R E A D M E     /     /    /    /   /   /  /  / / /// 

    ...   The main functions are:   ...

        1. get_student_ids_by_gender(gender) ---> This is a helper function that is used by the remaining functions below it.
        2. get_student_id_by_bedtime_preference(gender, bedtime_preference)
        3. get_student_id_by_ac_fan_preference(gender, ac_fan_preference)
        4. get_student_id_by_ac_temp(ac_temp_preference)
    
    ____________________________________________________________________________________________________________________
    • Though I have tested all the functions and compared them to database values, I strongly encourage anyone to reach out 
    incase any discrepancies are discovered.
    ____________________________________________________________________________________________________________________

    /// NoteS: ///
    
    • The function get_student_ids_by_gender(gender) only returns a list of ids without printing it. However, 
    should you want to test the function and see the returned list of ids, you can un-comment the print-statement 
    above the return statement. 
    
    • Only one out of the above functions can be called at a time.
    
    • The commented functions below can be run, but note that the 3rd commented function from the top is set to ('ac', '') as an example.
      You can change the values of the tuple to:
      
      ('', 'fan')
      ('ac', '')   ---> current option
      ('', '')
      ('ac', 'fan')
      
      and obtain the students of a chosen gender with the ac/fan preference of your choice.

"""

#get_student_ids_by_gender('M')
#get_student_id_by_bedtime_preference('F', 23)
#get_student_id_by_ac_fan_preference('F', ('ac', ''))
#get_student_id_by_ac_temp('M', 23)

if __name__ == "__main__":
    app.run(debug=True)
