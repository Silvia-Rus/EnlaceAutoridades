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
    with open(name+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def createCSVUnmatched():
    header = ['Link', 'BN','Campo','$a', 'SC2']
    createCSV(unmatchedName, header)

def createCSVMatched():
    #revisar
    header = ['Aut','Biblio','BN','Campo','$9','$a', 'SC2']
    createCSV(matchedName, header)

def createCSVCounters():
    #revisar
    header = ['REPORT']
    createCSV(counterName, header)

def initCSV():
    createCSVUnmatched()
    createCSVMatched()
    createCSVCounters()

def writeCSV(name, data):
    with open(name+'.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def writeCSVUnmatched(biblionumber, campo):
    data = []
    data.append(linkCatalogBib+biblionumber)
    data.append(biblionumber)
    data.append(campo.campo)
    for sc in campo.subcampos:
        data.append(sc.valor)
    writeCSV(unmatchedName, data)
    return "BN:"+biblionumber+" - Campo: "+str(campo.campo)+" (NO enlazado)\n"

def writeCSVMatched(biblionumber, SC9, campo):
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




