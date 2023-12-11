from pymarc import MARCReader
from getters import getFieldDollarA
from getters import getHasUnlinkedAuth
from getters import getFields
from getters import getBiblioNumber


# from getters import getLenListFields

biblios = 'mrcFiles/BIB_TODOS.mrc'
# biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

perso = 'mrcFiles/AUT_PERSO_NAME.mrc'
# perso = 'mrcFiles/AUT_PERSO_NAME_test.mrc'
corpo = 'mrcFiles/AUT_CORPO_NAME.mrc'
topic = 'mrcFiles/AUT_PERSO_NAME.mrc'
unlinkedAuth = 0 
matchingAuth = 0
recordCounter = 1

def getAuth1XX(bibEnc):
  if bibEnc == '100' or bibEnc == '700':
    return '100'
  elif bibEnc == '110' or bibEnc == '710':
    return '100'
  elif bibEnc == '650':
    return '150' 

def link_auth(bibRecord, field, routeAuth):
  
  global unlinkedAuth
  global matchingAuth
  global recordCounter
  print(recordCounter)
  listFields = getFields(bibRecord, field)
  i = 0   
   # aqui gira la lista de canpos X00 del bib     
  for fieldInList in listFields:             
    #  print(fieldInList)  
    #  print(getHasUnlinkedAuth(fieldInList))
    # print(i)
    # print('BN: '+ str(getBiblioNumber(bibRecord))) 
    if getHasUnlinkedAuth(fieldInList): 
      unlinkedAuth = unlinkedAuth + 1
      # print('BN: '+ str(getBiblioNumber(bibRecord)))
      with open(routeAuth, 'rb') as fh: # dentro del archivo de autoridades
        reader = MARCReader(fh)
        for recordAuth in reader:
          auth1XXSubfieldA = getFieldDollarA(recordAuth, getAuth1XX(field), 0)
          # print(recordAuth.get_fields('001')[0].value()) 
          # print(auth1XXSubfieldA) # CAMINA
        
          bibSubfieldA = getFieldDollarA(bibRecord, field ,i)

          # print(bibSubfieldA)
          if auth1XXSubfieldA  == bibSubfieldA:
            matchingAuth = matchingAuth + 1
            break
           #  print(recordAuth.get_fields('001')[0].value()) 
    i = i+1
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
    link_auth(record, '650', topic)

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
    print_resume()
  
    
  
     








             
      

            
         

  

  




