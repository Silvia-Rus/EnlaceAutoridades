import csv  

# header = ['name', 'area', 'country_code2', 'country_code3']
# data = ['Afghanistan', 652090, 'AF', 'AFG']

# reader = csv.reader(open("employees.csv"))
# no_lines= len(list(reader))
# print(no_lines)

def createCSV():
    header = ['Field','Link', 'BN', '$a', 'SF2']
    with open('export.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def writeCSV(field, BN, dollarA, subfieldTwoText = ''):
    link = 'http://catalogo.fi.uba.ar:8080/cgi-bin/koha/cataloguing/addbiblio.pl?biblionumber='+BN+'#tab6XX'
    # link = 'http://catalogo.fi.uba.ar:8080/cgi-bin/koha/catalogue/detail.pl?biblionumber='+BN
    data = [field, link, BN, dollarA, subfieldTwoText]
    with open('export.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)
