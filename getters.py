from pymarc import MARCReader

#FIELDS
def getListaDeCampoEnRegistro(record, field):
   return record.get_fields(field)

#SUBFIELDS
def getSubfields(field, subfield):
    return field.get_subfields(subfield) #devuelve una lista

def getListDollar9(campo):
   return getSubfields(campo, '9') 

def getListDollarA(campo):
   return getSubfields(campo, 'a') 

def getHasUnlinkedAuth(campo):
   return len(getListDollar9(campo)) == 0 and len(getListDollarA(campo)) > 0

# def getNRSubfield(record, field, subfield, index): #ESTE INDEX ES PARA LOS CAMPOS REPETIBLES S
#                                           # E DEBE ITERAR CUANDO SE ITERA ESA LISTA                                    
   
   
#    if len(record.get_fields(field)) > 0 and len(record.get_fields(field)[index].get_subfields(subfield)) > 0:
#       return record.get_fields(field)[index].get_subfields(subfield)[0].encode('utf-8')

def getSubfields(campo, subcampo):                                  
   return campo.get_subfields(subcampo)

def getValorSubfield(subcampo):
      return subcampo.encode('utf-8')

def getBiblioNumber(record):
   return record.get_fields('999')[0].get_subfields('c')[0]


   
   
   


