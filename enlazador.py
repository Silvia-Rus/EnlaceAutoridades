from pymarc    import MARCReader
from getters   import getSubfields
from getters   import getValorSubfield
from getters   import getHasUnlinkedAuth
from getters   import getListaDeCampoEnRegistro
from getters   import getBiblioNumber  
from setters   import setCampoSubcampoValor

from connector import findMatchingAuth
from informes  import writeCSVUnmatched
from informes  import writeCSVMatched
from informes  import writeCSVCounter
from informes  import initCSV
from campo import Campo
from subcampo import Subcampo


# biblios = 'mrcFiles/BIB_TODOS.mrc'
# biblios = 'mrcFiles/BIB_500REG_1.mrc'
biblios = 'mrcFiles/BIB_14REG.mrc'
# biblios = 'mrcFiles/BIB_1REG.mrc'

campo100 = Campo('100', [Subcampo('a', ''), Subcampo('d', '')])
campo110 = Campo('110', [Subcampo('a', ''), Subcampo('b', '')])
campo650 = Campo('650', [Subcampo('a', '')])
campo700 = Campo('700', [Subcampo('a', ''), Subcampo('d', '')])
campo710 = Campo('710', [Subcampo('a', ''), Subcampo('b', '')])

listaDeCampos = [campo100, campo110, campo650, campo710, campo700]

nameMrcModified = 'mrcTransformed/BIB_EXPORT_OK.mrc'
unlinkedAuth  = 0 
matchingAuth  = 0
recordCounter = 0

def link_auth(bibRecord): 
  global unlinkedAuth
  global matchingAuth
  global recordCounter
  for campo in listaDeCampos: 
    ocurrenciasDelCampo = getListaDeCampoEnRegistro(bibRecord, campo.campo)
    if(hayElementosEn(ocurrenciasDelCampo)):
      i = 0
      for ocurrencia in ocurrenciasDelCampo:
        campoSin9 = detectarCampoSinEnlazar(ocurrencia, campo)
        if(campoSin9 != False):
          print(campoSin9)
          authId =  detectarAuthIdenBD(campoSin9)
          if(authId != False):
            setCampoSubcampoValor(ocurrenciasDelCampo[i], '9', authId)
        i+=1
  escribirMarc(bibRecord)

def escribirMarc(record):
  with open(nameMrcModified, 'a') as out:
    out.write(record.as_marc())

def hayElementosEn(array):
  retorno = False
  if(len(array) > 0):
    retorno = True
  return retorno
  
def detectarCampoSinEnlazar(ocurrencia, c): 
  campo = ocurrencia 
  retorno = False  
  if getHasUnlinkedAuth(ocurrencia):
    # unlinkedAuth += 10
    campoRetorno = Campo(c.campo, [])
    for sc in c.subcampos: # para cada uno del subcampo por ej. dolar a
      listaSubcampos = getSubfields(campo, sc.letra) # listado de ocurrencias del dolar a
      if(hayElementosEn(listaSubcampos)):
        for sc2 in listaSubcampos:
          valor = getValorSubfield(sc2)
          campoRetorno.subcampos.append(Subcampo(sc.letra, valor))
    # print(campoRetorno)
    return campoRetorno 
  return retorno

def detectarAuthIdenBD(campo):
  retorno = False
  ocurrenciasEnBD = findMatchingAuth(campo)
  if(hayElementosEn(ocurrenciasEnBD)):
    print(str(ocurrenciasEnBD[0][0]))
    return str(ocurrenciasEnBD[0][0])
  return retorno


# def export_counter():
#   data1 = ["Records examined:     ", str(recordCounter)]
#   data2 = ["Unlinked authorities: ", str(unlinkedAuth)]
#   data3 = ["Matched authorities:  ",str(matchingAuth)]
#   data = [data1, data2, data3]
#   writeCSVCounter(data)

# def logInfoDB(auth, result, subfieldTwo):
#   text = "EN BASE: 001: "+str(result[0])+" - "+str(auth)+"$a: "+str(result[2].encode('utf-8'))
#   if str(result[3].encode('utf-8')) != '' : 
#      text += "$"+subfieldTwo+": "+str(result[3].encode('utf-8'))
#   return text
   
initCSV()
with open(biblios, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
      link_auth(record)
    # export_counter()

  
    
  
     








             
      

            
         

  

  




