import csv  


directory = 'reports/'
unmatchedName = directory+'unmatchedExport'
matchedName   = directory+'matchedExport'
counterName   = directory+'counterExport'
linkCatalogBib = 'http://catalogo.fi.uba.ar:8080/cgi-bin/koha/cataloguing/addbiblio.pl?biblionumber='
linkCatalogAut = 'http://catalogo.fi.uba.ar:8080/cgi-bin/koha/authorities/detail.pl?authid='

def createCSV(name, header):
    with open(name+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def createCSVUnmatched():
    header = ['Field','BN', '$a', 'SF2','Link']
    createCSV(unmatchedName, header)

def createCSVMatched():
    #revisar
    header = ['Field','BN','$9','$a', 'SF2','Aut','Biblio']
    createCSV(matchedName, header)

def createCSVCounters():
    #revisar
    header = ['REPORT']
    createCSV(counterName, header)

def initCSV():
    createCSVUnmatched()
    createCSVMatched()
    createCSVCounters()

def formLinkBib(field, BN):
    numberField = field[0]
    tab = '#tab'+numberField+'XX'
    link = linkCatalogBib+BN+tab
    return link

def formLinkAut(subfield9Text):
    link = linkCatalogAut+subfield9Text+'#tab1XX'
    return link

def writeCSV(name, data):
    field = data[0]
    BN = data[1]
    link = formLinkBib(field, BN)
    data.append(link)
    with open(name+'.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def writeCSVUnmatched(data):
    writeCSV(unmatchedName, data)

def writeCSVMatched(data):
    subfield9Text = data[2]
    linkAut = formLinkAut(subfield9Text)
    data.append(linkAut)
    writeCSV(matchedName, data)

def writeCSVCounter(data):
     with open(counterName+'.csv', 'a') as f:
        writer = csv.writer(f)
        for d in data:
            # print(d[0]+d[1])
            writer.writerow(d)

def terminal(data):
     with open('terminal.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


