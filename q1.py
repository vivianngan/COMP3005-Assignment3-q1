import psycopg2
from datetime import datetime

#connect to database
#adjust these to match the database that you make
conn = psycopg2.connect(
    database = "Assignment3",
    user='postgres',
    password='Goat1234!!',
    host='localhost',
    port='5432'
)
conn.autocommit = True

cursor = conn.cursor()

#create students table and populate table with initial data
def db_setup():
    cursor.execute("DROP TABLE IF EXISTS students")

    sql = '''CREATE TABLE students (
        student_id SERIAL PRIMARY KEY,
        first_name VARCHAR(20) NOT NULL,
        last_name VARCHAR(20) NOT NULL,
        email VARCHAR(50) UNIQUE NOT NULL,
        enrollment_date DATE
    );'''

    cursor.execute(sql)

    sql = '''INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');'''

    cursor.execute(sql)

def getAllStudents():
    sql_select = '''
    SELECT *
    FROM students
    '''
    cursor.execute(sql_select)
    #gets the results from the query
    results = cursor.fetchall()
    print(results)
    for result in results:
        #sets each NULL date to NULL
        if result[4] == None:
            date = 'NULL'
        else:
            #formats the date with yyyy-mm-dd
            date = f'{result[4].strftime("%Y")}-{result[4].strftime("%m")}-{result[4].strftime("%d")}'
        #formats and prints each record from the students table
        result = f"{result[0]}. {result[1]} {result[2]}, {result[3]}, {date}"
        print(result)

def addStudent(first_name, last_name, email, enrollment_date):
    #checks if the enrollment date is null
    if enrollment_date == '':
        sql_insert = f'''
        INSERT INTO students (first_name, last_name, email) VALUES ('{first_name}', '{last_name}', '{email}')'''
    else:
        sql_insert = f'''
        INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('{first_name}', '{last_name}', '{email}', '{enrollment_date}')'''

    try:
        cursor.execute(sql_insert)
    except psycopg2.errors.UniqueViolation:
        print("Error: email is not unique")
    except Exception as e:
        print(e)
        
def updateStudentEmail(student_id, new_email):
    sql_insert = f'''
    UPDATE students
    SET email='{new_email}'
    WHERE student_id='{student_id}'
    '''
    try:
        cursor.execute(sql_insert)
    except psycopg2.errors.UniqueViolation:
        print("Error: Email not unique")
    except Exception as e:
        print(e)

def deleteStudent(student_id):
    sql_delete = f'''
    DELETE FROM students
    WHERE student_id={student_id}
    '''
    try:
        cursor.execute(sql_delete)
    except Exception as e:
        print(e)

def menu():
    #displays menu to user and gets the input
    return int(input("\n0. exit\n1. getAllStudents\n2. addStudent\n3. updateStudentEmail \n4. deleteStudent\n"))

def main():
    #setup database
    #db_setup()

    #loops menu
    exit = False
    while(exit != True):
        inp = menu()
        
        if inp == 0:
            exit = True
        elif inp == 1:
            getAllStudents()
        elif inp == 2:
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            date = input("Enrollment Date (yyyy-mm-dd): ")
            addStudent(first_name, last_name, email, date)
        elif inp == 3:
            student_id = int(input("Student Id: "))
            new_email = input("New Email: ")
            updateStudentEmail(student_id, new_email)
        else:
            student_id = int(input("Student Id: "))
            deleteStudent(student_id)

    #close connection to database when user quits program
    conn.close()

if __name__=="__main__":
    main()