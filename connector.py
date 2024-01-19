import mysql.connector

def formExtractValue(field, subfield):
    return '''ExtractValue(a.marcxml, '//datafield[@tag="'''+field+'"]/subfield[@code="'+subfield+'''"]')'''

def query(field, subfieldOne, textOne, subfieldTwo, textTwo):
    extractValueOne = formExtractValue(field, subfieldOne)
    extractValueTwo = formExtractValue(field, subfieldTwo)
    selectPart = 'SELECT a.authid, a.authtypecode, '+extractValueOne+', '+extractValueTwo
    fromPart = ' FROM auth_header a '
    if(str(textTwo) == 'None'):
        wherePart = 'WHERE '+extractValueOne+'="'+textOne+'"'
    else:
        wherePart = 'WHERE '+extractValueOne+'="'+textOne+'" AND '+extractValueTwo+'="'+textTwo+'"'
    # print(selectPart+fromPart+wherePart)
    return selectPart+fromPart+wherePart
   

def throwQuery(field,subfieldOne,textOne,subfieldTwo = 'd',textTwo = 'None'):
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
        # cursor.execute(queryOneSubfield(field, subfieldOne, textOne))
        cursor.execute(query(field, subfieldOne, textOne, subfieldTwo, textTwo))
        results = cursor.fetchall()
    except mysql.connector.Error as error:
        print("ERROR CONNECTING:", error)
    finally:
        if connection != -1: 
            cursor.close()
            connection.close()
        return results

# print(throwQuery('100','a','Baldwin, John S.,')) #test = [(1, u'PERSO_NAME', u'Baldwin, John S.,')]



