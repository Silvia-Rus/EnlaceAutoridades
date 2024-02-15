from pymarc import MARCReader
from getters   import getSubfieldA
from getters   import getNRSubfield
from getters   import getHasUnlinkedAuth
from getters   import getFields
from getters   import getBiblioNumber  
from connector import findMatchingAuth
from exporter  import writeCSVUnmatched
from exporter  import writeCSVMatched
from exporter  import writeCSVCounter
from exporter  import initCSV

biblios = 'mrcFiles/BIB_TODOS.mrc'
# biblios = 'mrcFiles/BIB_500REG_1.mrc'
# biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

fieldToMatchList = ['100', '110', '650', '710', '700']

nameMrcModified = 'mrcTransformed/BIB_EXPORT.mrc'
unlinkedAuth  = 0 
matchingAuth  = 0
recordCounter = 0

def link_auth(bibRecord): 
  global unlinkedAuth
  global matchingAuth
  global recordCounter

  for field in fieldToMatchList: # auth = 650
    i = 0  
    auth1XX = getAuth1XX(field)
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
        print(biblionumber)
        #MATCHING
        results       = findMatchingAuth(auth1XX, field, firstSubfieldText, biblionumber, secondSubfield, secondSubfieldText)
        #PREPARING
        if len(results) > 0:
          result = results[0]
          subfield9Text = str(result[0])
          # print(logInfoDB(auth1XX, result, secondSubfieldText))
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
  with open(nameMrcModified, 'a') as out:
    out.write(record.as_marc())
  recordCounter = recordCounter+1

def getSecondSubfield(field):
     if field == '100' or field == '700' :
      return 'd'
     elif field == '110' or field == '710' : 
      return 'b'
     else:
      return ''

def getAuth1XX(field):
  auth1XX = '1'+field[1]+field[2]
  return auth1XX
     
def getSecondSubfieldText(record, field, i, secondSubfield):
  if     secondSubfield    != '': 
     secondSubfieldText = getNRSubfield(record,field, secondSubfield, i)
  else:  
     secondSubfieldText = ''
  return secondSubfieldText

def export_counter():
  data1 = ["Records examined:     ", str(recordCounter)]
  data2 = ["Unlinked authorities: ", str(unlinkedAuth)]
  data3 = ["Matched authorities:  ",str(matchingAuth)]
  data = [data1, data2, data3]
  writeCSVCounter(data)

def logInfoDB(auth, result, subfieldTwo):
  text = "EN BASE: 001: "+str(result[0])+" - "+str(auth)+"$a: "+str(result[2].encode('utf-8'))
  if str(result[3].encode('utf-8')) != '' : 
     text += "$"+subfieldTwo+": "+str(result[3].encode('utf-8'))
  return text
   
initCSV()
with open(biblios, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
      link_auth(record)
    export_counter()

  
    
  
     








             
      

            
         

  

  




