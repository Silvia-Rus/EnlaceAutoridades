import mysql.connector
# import pyodbc as po

def throwQuery():
    query = ''''SELECT a.authid AS 'id', ExtractValue(a.marcxml, '//datafield[@tag="100"]/subfield[@code="a"]') AS 'encab' FROM auth_header a'''
    cursor = connection().cursor()
    cursor.execute(query)
    print(cursor.fetchall())

def connection():
    connection = -1
    try:
        connection =  mysql.connector.connect(
                      host='127.0.0.1',
                      port=8889,
                      user="root",
                      password="",
                      database="",
                      charset='utf8')
    except mysql.connector.Error as error:
        print("ERROR CONNECTING:", error)
    finally:
        print(connection)
        return connection





