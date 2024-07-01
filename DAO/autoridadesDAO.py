import mysql.connector
from entidades.subcampo import Subcampo
from entidades.campo import Campo

def formExtractValue(campo, subcampo):
    """
    Forma el string que extrae los valores de los subcampos del registro de autoridad en una consulta SQL.
    
    Args:
        campo (Campo): el campo en el registro bibliografico del que se quiere buscar el valor.
        subcampo (Subcampo): el subcampo del que se quiere buscar el valor.
    
    Returns: 
        string: listo para usar en la consulta SQL.
    """
    return '''ExtractValue(a.marcxml, '//datafield[@tag="'''+campo.enAut+'"]/subfield[@code="'+subcampo.letra+'''"]')'''+'="'+subcampo.valor+'"'

def query(campo):
    """
        Forma la query en SQL lista para ser lanzada a la BD.
        
        Args:
            campo (Campo): campo del que se quiere buscar correspondencia en la BD.
        
        Returns:
            string: la query en SQL lista para ser lanzada a la BD.
    """
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

def findMatchingAuth(campo):
    """
        Conecta a la BD y lanza una consulta a la BD de autoridades.

        Args:
            campo (Campo) que se busca.
        
        Returns:
            List: Los resultados de la busqueda.
    """
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
        






