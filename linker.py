from pymarc import MARCReader
from getters import getFieldDollarA
from getters import getFieldDollarD
from getters import getHasUnlinkedAuth
from getters import getFields
from getters import getBiblioNumber  
from connector import throwQuery
from exporter import createCSV
from exporter import writeCSV
# from getters import getLenListFields

# biblios = 'mrcFiles/BIB_TODOS.mrc'
biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

unlinkedAuth = 0 
matchingAuth = 0
recordCounter = 0

def link_auth(bibRecord, field, auth): 
  global unlinkedAuth
  global matchingAuth
  global recordCounter
  listFields = getFields(bibRecord, field) #toma TODOS los encabezamientos del 650
  i = 0   
  for fieldInList in listFields:          
    if getHasUnlinkedAuth(fieldInList):    #filtra los SIN $9
      unlinkedAuth += 1
      biblionumber = getBiblioNumber(bibRecord)
      dollarA      = getFieldDollarA(bibRecord, field, i)
      subfieldTwo  = ''

      if field == '650': 
         results = throwQuery(auth, 'a', dollarA) 
         print(logInfoReg(biblionumber, field , 'a', dollarA))
      elif field == '100':
         dollarD = getFieldDollarD(bibRecord, field, i)
         results = throwQuery(auth, 'a', dollarA, 'd', dollarD) 
         print(logInfoReg(biblionumber, field , 'a', dollarA, 'd', dollarD))

      
      if len(results) > 0:
         result = results[0]
         print(logInfoDB(auth, result, subfieldTwo))
         matchingAuth += 1
      else:
         writeCSV(field.encode('utf-8'),biblionumber.encode('utf-8'), dollarA)
         print("No matching authorities.")
      print("-----------")
    i += 1
  recordCounter = recordCounter+1

   
def print_resume():
  print("Records examined:     "+str(recordCounter))
  print("Unlinked authorities: "+str(unlinkedAuth))
  print("Matched authorities:  "+str(matchingAuth))

def logInfoReg(biblionumber, field, subfieldOne, textOne, subfieldTwo = '', textTwo = ''):
  text = "EN REG:  BN:  "+str(biblionumber)+" - "+str(field)+"$"+subfieldOne+": "+textOne
  if field != '650': text += " $"+subfieldTwo+": "+str(textTwo) 
  return text
     
def logInfoDB(auth, result, subfieldTwo):
  text = "EN BASE: 001: "+str(result[0])+" - "+str(auth)+"$a: "+result[2].encode('utf-8')
  if result[3].encode('utf-8') != '' : text += "$"+subfieldTwo+": "+str(result[3].encode('utf-8'))
  return text

     
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
      link_perso_100(record)
      # link_perso_700(record)
      # link_topic_650(record)
      # link_corpo_110(record)
      # link_corpo_710(record)
    print_resume()
  
    
  
     








             
      

            
         

  

  




