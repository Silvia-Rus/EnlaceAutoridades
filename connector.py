import mysql.connector
from subcampo import Subcampo
from campo import Campo



def formExtractValue(campo, subcampo):
    return '''ExtractValue(a.marcxml, '//datafield[@tag="'''+campo.enAut+'"]/subfield[@code="'+subcampo.letra+'''"]')'''+'="'+subcampo.valor+'"'

# def query(campo, subcampoOne, textOne, subcampoTwo, textTwo):
#     extractValueOne = formExtractValue(campo, subcampoOne)
#     extractValueTwo = formExtractValue(campo, subcampoTwo)
#     selectPart = 'SELECT a.authid, a.authtypecode, '+extractValueOne+', '+extractValueTwo
#     fromPart = ' FROM auth_header a '
#     if(str(textTwo) == 'None'):
#         wherePart = 'WHERE '+extractValueOne+'="'+textOne+'"'
#     else:
#         wherePart = 'WHERE '+extractValueOne+'="'+textOne+'" AND '+extractValueTwo+'="'+textTwo+'"'
#     # print(selectPart+fromPart+wherePart)
#     return selectPart+fromPart+wherePart
   
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
    print(selectPart+fromPart+wherePart)
    return selectPart+fromPart+wherePart

def throwQuery(campo):
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
        # cursor.execute(queryOneSubcampo(campo, subcampoOne, textOne))
        cursor.execute(query(campo))
        results = cursor.fetchall()
    except mysql.connector.Error as error:
        print("ERROR CONNECTING:", error)
    finally:
        if connection != -1: 
            cursor.close()
            connection.close()
        return results

def findMatchingAuth(campo):
   results = throwQuery(campo) 
   #print(logInfoRecord(biblionumber, campo , 'a', firstSubcampoText, secondSubcampo, secondSubcampoText))
   return results

def logInfoRecord(biblionumber, campo, subcampoOne, textOne, subcampoTwo = '', textTwo = ''):
  text = "EN REG:  BN:  "+str(biblionumber)+" - "+str(campo)+"$"+subcampoOne+": "+textOne
  if campo != '650': 
     text += " $"+subcampoTwo+": "+str(textTwo) 
  return text

# print(throwQuery('100','a','Baldwin, John S.,')) #test = [(1, u'PERSO_NAME', u'Baldwin, John S.,')]



