from pymarc import MARCReader
from getters import getFieldDollarA
from getters import getHasUnlinkedAuth
from getters import getFields
from getters import getBiblioNumber  
from connector import throwQuery
from exporter import createCSV
from exporter import writeCSV
# from getters import getLenListFields

biblios = 'mrcFiles/BIB_TODOS.mrc'
# biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

unlinkedAuth = 0 
matchingAuth = 0
recordCounter = 0

def link_auth(bibRecord, field, auth): 
  global unlinkedAuth
  global matchingAuth
  global recordCounter
  # print(recordCounter)
  listFields = getFields(bibRecord, field) #toma TODOS los encabezamientos del 650
  i = 0   
  for fieldInList in listFields:          
    if getHasUnlinkedAuth(fieldInList):    #filtra los SIN $9
      unlinkedAuth = unlinkedAuth + 1
      biblionumber = getBiblioNumber(record)
      dollarA = getFieldDollarA(bibRecord, field, i)
      results = throwQuery(auth, 'a', dollarA)
      print("EN REG:  BN:  "+str(biblionumber)+" - "+str(field)+"$a: "+dollarA)
      if len(results) > 0:
         result = results[0]
         print("EN BASE: 001: "+str(result[0])+" - "+str(auth)+"$a: "+result[2].encode('utf-8'))
         matchingAuth = matchingAuth+1
      else:
         writeCSV(field.encode('utf-8'),biblionumber.encode('utf-8'), dollarA)
         print("No matching authorities.")
      print("-----------")
    i = i+1
  recordCounter = recordCounter+1

def print_resume():
  print("Records examined:     "+str(recordCounter))
  print("Unlinked authorities: "+str(unlinkedAuth))
  print("Matched authorities:  "+str(matchingAuth))
    
def link_perso_100(record):
    link_auth(record, '100', '100')

def link_perso_700(record):
    link_auth(record, '700', '100')
    # print_resume('700')

def link_topic_650(record):
    link_auth(record, '650', '150')

def link_corpo_110(record):
    link_auth(record, '110', '110')

def link_corpo_710(record):
    link_auth(record, '710', '110')

createCSV()
with open(biblios, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
      # link_perso_100(record)
      # link_perso_700(record)
      link_topic_650(record)
      # link_corpo_110(record)
      # link_corpo_710(record)
    print_resume()
  
    
  
     








             
      

            
         

  

  




