import mysql.connector

def query(field, subfield, text):
    extractValue = '''ExtractValue(a.marcxml, '//datafield[@tag="'''+field+'"]/subfield[@code="'+subfield+'''"]')'''
    selectPart = 'SELECT a.authid, a.authtypecode, '+extractValue
    fromPart = ' FROM auth_header a '
    wherePart = 'WHERE '+extractValue+'="'+text+'"'
    # print(selectPart+fromPart+wherePart)
    return selectPart+fromPart+wherePart
   

def throwQuery(field,subfield,text):
    connection = -1
    try:
        connection =  mysql.connector.connect(
                      host='127.0.0.1',
                      port=8889,
                      user="root",
                    #  password="",
                      database='koha_biblioteca',
                      charset='utf8')
        cursor = connection.cursor()
        cursor.execute(query(field, subfield, text))
        results = cursor.fetchall()
    except mysql.connector.Error as error:
        print("ERROR CONNECTING:", error)
    finally:
        if connection != -1: 
            cursor.close()
            connection.close()
        return results

# print(throwQuery('100','a','Baldwin, John S.,')) #test = [(1, u'PERSO_NAME', u'Baldwin, John S.,')]



