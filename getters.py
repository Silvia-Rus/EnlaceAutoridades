from pymarc import MARCReader

#FIELDS
def getFields(record, field):
   return record.get_fields(field)

# def getLenListFields(record, field):
#    return len(getFields(record, field))

#SUBFIELDS
def getSubfields(field, subfield):
    return field.get_subfields(subfield) #devuelve una lista

def getListDollar9(field):
   return getSubfields(field, '9') 

def getListDollarA(field):
   return getSubfields(field, 'a') 

def getHasUnlinkedAuth(field):
   if(len(getListDollar9(field)) == 0 and len(getListDollarA(field)) > 0):
      return True
   else:
      return False
   
def getFieldDollarA(record, field, index): #ESTE INDEX ES PARA LOS CAMPOS REPETIBLES S
                                          # E DEBE INTERAR CUANDO SE ITEA ESA LISTA                                    
   
   if len(record.get_fields(field)) > 0 and len(record.get_fields(field)[index].get_subfields('a')) > 0:
      return record.get_fields(field)[index].get_subfields('a')[0].encode('utf-8')

def getBiblioNumber(record):
   return record.get_fields('999')[0].get_subfields('c')[0]


   
   
   


