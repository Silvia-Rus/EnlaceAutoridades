import mysql.connector
from entidades.subcampo import Subcampo
from entidades.campo import Campo

def formExtractValue(campo, subcampo):
    return '''ExtractValue(a.marcxml, '//datafield[@tag="'''+campo.enAut+'"]/subfield[@code="'+subcampo.letra+'''"]')'''+'="'+subcampo.valor+'"'

def query(campo):
    selectPart = 'SELECT a.authid '
    fromPart = ' FROM auth_header a '
    wherePart = 'WHERE '
    i = len(campo.subcampos)
    
    for sc in campo.subcampos:
        extractValue = formExtractValue(campo, sc)
        wherePart += extractValue
        if(i > 1):
            wherePart += ' AND '
        i -= 1
    # print(selectPart+fromPart+wherePart)
    return selectPart+fromPart+wherePart

def throwQuery(campo):
    results = []
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
        cursor.execute(query(campo))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as error:
        print("ERROR CONECTANDO A LA BD. "
              "Asegurate de que los datos en throwQuery el archivo autoridadesDAO.py son correctos. "
              "Asegurate de que tu BD esta conectada. "
              "(Recuerda que este conector solo fue probado con MySQL). "
              "Mas detalles: ")
    finally:
        if connection != -1: 
            cursor.close()
            connection.close()
        

def findMatchingAuth(campo):
   results = throwQuery(campo) 
   return results





