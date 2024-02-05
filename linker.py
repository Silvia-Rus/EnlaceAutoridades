from pymarc import MARCReader
from getters   import getSubfieldA
from getters   import getNRSubfield
from getters   import getHasUnlinkedAuth
from getters   import getFields
from getters   import getBiblioNumber  
from connector import findMatchingAuth
from exporter  import createCSVUnmatched
from exporter  import writeCSVUnmatched
from exporter  import createCSVMatched
from exporter  import writeCSVMatched

# biblios = 'mrcFiles/BIB_TODOS.mrc'
biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

unlinkedAuth  = 0 
matchingAuth  = 0
recordCounter = 0

def link_auth(bibRecord, field, auth1XX): 
  global unlinkedAuth
  global matchingAuth
  global recordCounter
  i = 0   
  listFields = getFields(bibRecord, field) 
  for fieldInList in listFields: 
    #FILTERING         
    if getHasUnlinkedAuth(fieldInList):  
      unlinkedAuth += 1
      #PREPARING
      biblionumber          = getBiblioNumber(bibRecord)
      firstSubfieldText     = getSubfieldA(bibRecord, field, i) #generally $a
      secondSubfield        = getSecondSubfield(field)
      secondSubfieldText    = getSecondSubfieldText(bibRecord, field, i, secondSubfield)
      #MATCHING
      results       = findMatchingAuth(auth1XX, field, firstSubfieldText, biblionumber, secondSubfield, secondSubfieldText)
    
      #PREPARING
      if len(results) > 0:
         result = results[0]
         subfield9Text = str(result[0])
         print(logInfoDB(auth1XX, result, secondSubfieldText))
         bibRecord.get_fields(field)[i].add_subfield('9', subfield9Text)
         data =[field.encode('utf-8'),biblionumber.encode('utf-8'), subfield9Text, firstSubfieldText, secondSubfieldText]
         writeCSVMatched(data)
         matchingAuth += 1
      else:
         data = [field.encode('utf-8'),biblionumber.encode('utf-8'),firstSubfieldText, secondSubfieldText]
         writeCSVUnmatched(data)
         print("No matching authorities.")
      print("-----------")
    i += 1
  #WRITING
  with open('prueba14.mrc', 'a') as out:
    out.write(record.as_marc())
  recordCounter = recordCounter+1

def getSecondSubfield(field):
     if field == '100' or field == '700' :
      return 'd'
     elif field == '110' or field == '710' : 
      return 'b'
     else:
      return ''
   
def getSecondSubfieldText(record, field, i, secondSubfield):
  if     secondSubfield    != '': 
     secondSubfieldText = getNRSubfield(record,field, secondSubfield, i)
  else:  
     secondSubfieldText = ''
  return secondSubfieldText

def print_resume():
  print("Records examined:     "+str(recordCounter))
  print("Unlinked authorities: "+str(unlinkedAuth))
  print("Matched authorities:  "+str(matchingAuth))

     
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

createCSVUnmatched()
createCSVMatched()
with open(biblios, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
      # link_perso_100(record)
      # link_perso_700(record)
      link_topic_650(record)
      # link_corpo_110(record)
      # link_corpo_710(record)
    print_resume()

  
    
  
     








             
      

            
         

  

  




