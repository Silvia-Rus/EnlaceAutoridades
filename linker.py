from pymarc import MARCReader
from getters import getFieldDollarA
from getters import getNRSubfield
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
  listFields = getFields(bibRecord, field) 
  i = 0   
  for fieldInList in listFields: 
    #FILTERING         
    if getHasUnlinkedAuth(fieldInList):  
      unlinkedAuth += 1

      #PREPARING
      biblionumber     = getBiblioNumber(bibRecord)
      dollarA          = getFieldDollarA(bibRecord, field, i)
      subfieldTwo      = subfieldTwoReturn(field)
      #MATCHING
      matchAuth       = matchReturn(record, auth, field, dollarA, biblionumber, i, subfieldTwo)
      results         = matchAuth[0]
      subfieldTwoText = matchAuth[1]
         
      #PREPARING
      if len(results) > 0:
         result = results[0]
         print(logInfoDB(auth, result, subfieldTwo))
         bibRecord.get_fields(field)[i].add_subfield('9', str(result[0]))
         matchingAuth += 1
      else:
         writeCSV(field.encode('utf-8'),biblionumber.encode('utf-8'), dollarA, subfieldTwoText)
         print("No matching authorities.")
      print("-----------")
    i += 1
  #WRITTING
  with open('prueba14.mrc', 'a') as out:
    out.write(record.as_marc())
  recordCounter = recordCounter+1

def subfieldTwoReturn(field):
     if field == '100' or field == '700' :
      return 'd'
     elif field == '110' or field == '710' : 
      return 'b'
     else:
      return ''
   
def matchReturn(record, auth, field, dollarA, biblionumber, i, subfieldTwo = ''):
   if    subfieldTwo    != '': subfieldTwoText = getNRSubfield(record,field,subfieldTwo,i)
   else: subfieldTwoText = ''
   results = throwQuery(auth, 'a', dollarA, subfieldTwo, subfieldTwoText) 
   print(logInfoReg(biblionumber, field , 'a', dollarA, subfieldTwo, subfieldTwoText))
   return [results, subfieldTwoText]

def print_resume():
  print("Records examined:     "+str(recordCounter))
  print("Unlinked authorities: "+str(unlinkedAuth))
  print("Matched authorities:  "+str(matchingAuth))

def logInfoReg(biblionumber, field, subfieldOne, textOne, subfieldTwo = '', textTwo = ''):
  text = "EN REG:  BN:  "+str(biblionumber)+" - "+str(field)+"$"+subfieldOne+": "+textOne
  if field != '650': 
     text += " $"+subfieldTwo+": "+str(textTwo) 
  return text
     
def logInfoDB(auth, result, subfieldTwo):
  text = "EN BASE: 001: "+str(result[0])+" - "+str(auth)+"$a: "+str(result[2].encode('utf-8'))
  if str(result[3].encode('utf-8')) != '' : 
     text += "$"+subfieldTwo+": "+str(result[3].encode('utf-8'))
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
      # link_perso_100(record)
      # link_perso_700(record)
      link_topic_650(record)
      # link_corpo_110(record)
      # link_corpo_710(record)
    print_resume()

  
    
  
     








             
      

            
         

  

  




