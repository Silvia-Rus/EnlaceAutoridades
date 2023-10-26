from pymarc import MARCReader
from getters import getDollar9
from getters import get1XXDollarA
from getters import getHasUnlinkedAuth


# biblios = 'mrcFiles/BIB_TODOS.mrc'
biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

perso = 'mrcFiles/AUT_PERSO_NAME.mrc'
# perso = 'mrcFiles/AUT_PERSO_NAME_prueba.mrc'
corpo = 'mrcFiles/AUT_CORPO_NAME.mrc'
topic = 'mrcFiles/AUT_PERSO_NAME.mrc'

def getAuth1XX(bibEnc):
  if bibEnc == '100' or bibEnc == '700':
    return '100'
  elif bibEnc == '110' or bibEnc == '710':
    return '100'
  elif bibEnc == '650':
    return '150' 
  
def link_auth(bibRecord, field, routeAuth): 
   lenListFields= len(bibRecord.get_fields(field))
   unlinkedFields = 0
   authExistent = 0    
   if lenListFields > 0:
         listFields = bibRecord.get_fields(field)
         for fieldInList in listFields:
            if len(fieldInList.get_subfields('9')) == 0 and len(fieldInList.get_subfields('a')) > 0 :
                unlinkedFields += 1
                with open(routeAuth, 'rb') as fh: # dentro del archivo de autoridades
                  reader = MARCReader(fh)
                  for recordAuth in reader:
                      auth1XX = recordAuth.get_fields(getAuth1XX(field))[0].get_subfields('a')[0]
                      # print(field)
                      # print(getAuth1XX(field))
                      # auth1XX = recordAuth.get_fields('100')[0].get_subfields('a')[0]
                      if len(auth1XX) > 0:
                        bibEncA = fieldInList.get_subfields('a')[0]
                        # print(auth1XX)
                        # print(bibEncA)
                        if auth1XX  == bibEncA:
                          print('holi')
                          authExistent += 1
                          print(authExistent)
                          #  print(recordAuth.get_fields('001')[0].value()) 
  
 
def link_perso_100(record):
    link_auth(record, '100', perso)

def link_perso_700(record):
    link_auth(record, '700', perso)

def link_topic_650(record):
    link_auth(record, '650', topic)

def link_corpo_110(record):
    link_auth(record, '110', corpo)

def link_corpo_710(record):
    link_auth(record, '710', corpo)

with open(biblios, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
      link_perso_100(record)
      link_perso_700(record)
      link_topic_650(record)
      link_corpo_110(record)
      link_corpo_710(record)
  
    
  
     








             
      

            
         

  

  




