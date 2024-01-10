from pymarc import MARCReader
from getters import getFieldDollarA
from getters import getHasUnlinkedAuth
from getters import getFields
from getters import getBiblioNumber  
from getters import getListDollarA

from connector import throwQuery


# from getters import getLenListFields

# biblios = 'mrcFiles/BIB_TODOS.mrc'
biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

perso = 'mrcFiles/AUT_PERSO_NAME.mrc'
# perso = 'mrcFiles/AUT_PERSO_NAME_test.mrc'
corpo = 'mrcFiles/AUT_CORPO_NAME.mrc'
topic = 'mrcFiles/AUT_PERSO_NAME.mrc'
unlinkedAuth = 0 
matchingAuth = 0
recordCounter = 1

def link_auth(bibRecord, field, auth): 
  global unlinkedAuth
  global matchingAuth
  global recordCounter
  # print(recordCounter)
  listFields = getFields(bibRecord, field) #toma TODOS los encabezamientos del 650
  for fieldInList in listFields:             
    if getHasUnlinkedAuth(fieldInList):    #filtra los SIN $9
      # unlinkedAuth = unlinkedAuth + 1
      biblionumber = getBiblioNumber(record)
      dollarA = getListDollarA(fieldInList)[0]
      result = throwQuery(auth, 'a', dollarA)[0]
      print("EN REG:  BN:  "+str(biblionumber)+" - "+str(field)+"$a: "+str(dollarA))
      print("EN BASE: 001: "+str(result[0])+" -  "+str(auth)+"$a "+str(result[2]))
      print("-----------")
  recordCounter = recordCounter+1

def print_resume():
  print("Unlinked authorities: "+str(unlinkedAuth))
  print("Matching authorities: "+str(matchingAuth))
    
def link_perso_100(record):
    link_auth(record, '100', perso)

def link_perso_700(record):
    link_auth(record, '700', perso)
    # print_resume('700')

def link_topic_650(record):
    link_auth(record, '650', '150')

def link_corpo_110(record):
    link_auth(record, '110', corpo)

def link_corpo_710(record):
    link_auth(record, '710', corpo)

with open(biblios, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
      # link_perso_100(record)
      # link_perso_700(record)
      link_topic_650(record)
      # link_corpo_110(record)
      # link_corpo_710(record)
    # print_resume()
  
    
  
     








             
      

            
         

  

  




