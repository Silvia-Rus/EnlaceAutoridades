from pymarc    import MARCReader
from gettersSetters.getters   import getSubfields
from gettersSetters.getters   import getValorSubfield
from gettersSetters.getters   import getHasUnlinkedAuth
from gettersSetters.getters   import getListaDeCampoEnRegistro
from gettersSetters.getters   import getBiblioNumber  
from gettersSetters.setters   import setCampoSubcampoValor
from DAO.autoridadesDAO import findMatchingAuth
from informes  import writeCSVUnmatched
from informes  import writeCSVMatched
from informes  import initCSV
from entidades.campo     import Campo
from entidades.subcampo  import Subcampo

class Enlazador:

  def __init__(self):
    self.unlinkedAuth  = 0 
    self.matchingAuth  = 0
    self.recordCounter = 0

  def link_auth(self, listaDeCampos, bibRecord): 
    self.recordCounter += 1
    for campo in listaDeCampos: 
      ocurrenciasDelCampo = getListaDeCampoEnRegistro(bibRecord, campo.campo)
      if(Enlazador.hayElementosEn(ocurrenciasDelCampo)):
        i = 0
        for ocurrencia in ocurrenciasDelCampo:
          campoSin9 = Enlazador.detectarCampoSinEnlazar(ocurrencia, campo)
          if(campoSin9 != False):
            biblionumber = getBiblioNumber(bibRecord)
            authId =  Enlazador.detectarAuthIdenBD(campoSin9)
            if(authId != False):
              setCampoSubcampoValor(ocurrenciasDelCampo[i], '9', authId)
              print(writeCSVMatched(biblionumber, authId, campoSin9))
              self.matchingAuth+=1
            else:
              print(writeCSVUnmatched(biblionumber, campoSin9))
              self.unlinkedAuth+=1
          i+=1
    return bibRecord
  
  @staticmethod
  def hayElementosEn(array):
    retorno = False
    if(len(array) > 0):
      retorno = True
    return retorno
  
  @staticmethod
  def detectarCampoSinEnlazar(ocurrencia, c): 
    campo = ocurrencia 
    retorno = False  
    if getHasUnlinkedAuth(ocurrencia):
      campoRetorno = Campo(c.campo, [])
      for sc in c.subcampos: # para cada uno del subcampo por ej. dolar a
        listaSubcampos = getSubfields(campo, sc.letra) # listado de ocurrencias del dolar a
        if(Enlazador.hayElementosEn(listaSubcampos)):
          for sc2 in listaSubcampos:
            valor = getValorSubfield(sc2)
            campoRetorno.subcampos.append(Subcampo(sc.letra, valor))
      # print(campoRetorno)
      return campoRetorno 
    return retorno
  
  @staticmethod
  def detectarAuthIdenBD(campo):
    retorno = False
    ocurrenciasEnBD = findMatchingAuth(campo)
    if(Enlazador.hayElementosEn(ocurrenciasEnBD)):
      return str(ocurrenciasEnBD[0][0])
    return retorno


  # def logInfoDB(auth, result, subfieldTwo):
  #   text = "EN BASE: 001: "+str(result[0])+" - "+str(auth)+"$a: "+str(result[2].encode('utf-8'))
  #   if str(result[3].encode('utf-8')) != '' : 
  #      text += "$"+subfieldTwo+": "+str(result[3].encode('utf-8'))
  #   return text
   


  
    
  
     








             
      

            
         

  

  




