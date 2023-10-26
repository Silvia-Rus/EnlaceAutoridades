from pymarc import MARCReader


def getSubfields(field, subfield):
    return field.get_subfields(subfield) #devuelve una lista

def getDollar9(field):
   return getSubfields(field, '9') #devuelve una lista

def getDollarA(field):
   return getSubfields(field, 'a') #devuelve una lista

def getHasUnlinkedAuth(field):
   buffer = False
   if(len(getDollar9(field)) == 0 and len(getDollarA(field) > 0)):
      buffer = True
   return buffer

def get1XXDollarA(record, field):
   if(len(record.get_fields(field).get_subfields('a')) > 0):
      return record.get_fields(field)[0].get_subfields('a')[0] #ojo no hay un else esto camina?



   
   
   


