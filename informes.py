import csv  
from datetime import datetime

fechaAhora = datetime.now().strftime("%Y%m%d%H%M%S")
directory = 'archivos/reports/'
unmatchedName = directory+fechaAhora+'_unmatchedExport'
matchedName   = directory+fechaAhora+'_matchedExport'
counterName   = directory+fechaAhora+'_counterExport'
linkCatalogBib = 'http://catalogo.fi.uba.ar:8080/cgi-bin/koha/cataloguing/addbiblio.pl?biblionumber='
linkCatalogAut = 'http://catalogo.fi.uba.ar:8080/cgi-bin/koha/authorities/detail.pl?authid='

def createCSV(name, header):
    """
        Crea un CSV nuevo y le asigna una cabecera.

        Args:
            name (str): nombre del archivo CSV a crear.
            header (List): list con el nombre de todas las columnas que va a contener.
    """
    with open(name+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def createCSVUnmatched():
    """
      Crea un CSV en el que se van a registrar los campos que no tienen enlace y no se han podido enlazar.
    """
    header = ['Link', 'BN','Campo','$a', 'SC2']
    createCSV(unmatchedName, header)

def createCSVMatched():
    """
      Crea un CSV en el que se van a registrar los campos que se han podido enlazar.
    """
    header = ['Aut','Biblio','BN','Campo','$9','$a', 'SC2']
    createCSV(matchedName, header)

def createCSVCounters():
    """
      Crea un CSV en el que se van a registrar las cifras finales del proceso de enlazado de encabezamientos.
    """
    header = ['REPORT']
    createCSV(counterName, header)

def initCSV():
    """
      Crea todos los CSV sobre los que se va a escribir durante el proceso de enlazado de campos.
    """
    createCSVUnmatched()
    createCSVMatched()
    createCSVCounters()

def writeCSV(name, data):
    """
      Escribe en un CSV con data que entra por parametro.

      Args:
       name (str): nombre del archivo en el que se quiere escribir.
       data (list de str): data que se quiere escribir en el archivo.
    """
    with open(name+'.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def writeCSVUnmatched(biblionumber, campo):
    """
      Escribe en el CSV en el que se registran los campos que no se han podido enlazar.
      Muestra por terminal los datos del campo.

      Args:
       biblionumber (str): biblionumber del registro en el que se encuentra el campo sin enlazar.
       campo (Campo): campo que se no se ha podido enlazar.

      Return:
        String: los datos que se van a mostrar por pantalla sobre el campo que no se ha podido enlazar.
    """
    data = []
    data.append(linkCatalogBib+biblionumber)
    data.append(biblionumber)
    data.append(campo.campo)
    for sc in campo.subcampos:
        data.append(sc.valor)
    writeCSV(unmatchedName, data)
    return "BN:"+biblionumber+" - Campo: "+str(campo.campo)+" (NO enlazado)\n"

def writeCSVMatched(biblionumber, SC9, campo):
    """
      Escribe en el CSV en el que se registran los campos que  se han podido enlazar.
      Muestra por terminal los datos del campo.

      Args:
       biblionumber (str): biblionumber del registro en el que se encuentra el campo sin enlazar.
       SC9 (str): el $9 asignado.
       campo (Campo): campo que se ha enlazado..

      Return:
        String: los datos que se van a mostrar por pantalla sobre el campo que se ha podido enlazar.
    """
    data = []
    data.append(linkCatalogAut+SC9)
    data.append(linkCatalogBib+biblionumber)
    data.append(biblionumber)
    data.append(campo.campo)
    data.append(SC9)
    for sc in campo.subcampos:
        data.append(sc.valor)
    writeCSV(matchedName, data)
    return "BN:"+biblionumber+" - Campo: "+str(campo.campo)+" (Enlazado)\n"

def writeCSVCounter(recordCounter, unlinkedAuth, matchingAuth):
    """
      Registra en el CSV de cifras finales del proceso de enlazado de encabezamientos.
      Muestra por terminal los datos.

      Args:
       recordCounter (int): el numero de registros analizados.
       unlinkedAuth (int): numero de encabezamientos que no se han podido enlazar.
       matchingAuth (int): numero de encabezamientos que se han podido enlazar.

      Return:
        String: los datos que se van a mostrar por pantalla sobre el campo que no se ha podido enlazar.
    """
    texto = ''
    data1 = ["Registros analizados: ", str(recordCounter)]
    data2 = ["Autoridades sin enlazar: " , str(unlinkedAuth)]
    data3 = ["Autoridades enlazadas: "  , str(matchingAuth)]
    data = [data1, data2, data3]
    with open(counterName+'.csv', 'a') as f:
        writer = csv.writer(f)
        for d in data:
            texto += str(d)+"\n"
            writer.writerow(d)
    return "RESUMEN: \n"+texto




