import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='db0',
                                         user='testuser',
                                         password='testuser')

    sql_select_Query = "select * from auth_user"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in Laptop is: ", cursor.rowcount)

    print("\nPrinting each laptop record")
    for row in records:
        print("Id = ", row[0], )
        print("password = ", row[1])
        print("last login = ", row[2])
        print("is superuser  = ", row[3], "\n")

except Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if (connection.is_connected()):
        connection.close()
        cursor.close()
        print("MySQL connection is closed")