from entidades.subcampo import Subcampo
from gettersSetters.getters   import getSubfields
from gettersSetters.getters   import getValorSubfield

class Campo:
    """campo marc propio con ligeras adiciones para poder operar con objetos de clase Field de la biblioteca pymarc con sus subcampos"""
    campo = ''      # numero de campo
    subcampos = []  # listado de subcampos
    enAut = ''      # encabezamiento en autoridades

    def __init__(self, campo, subcampos):
        """
          Asigna los attibutos de campo y subcampos, que debe ser una lista.
          Inicializa el atributo "enAut" con el campo 1XX que le corresponda el encabezamiento. 
        """
        self.campo = campo
        self.subcampos = subcampos
        self.enAut = "1"+campo[1]+campo[2]

    def __str__(self):
        """
          Representacion visual del campo en formato string. 
        """
        retorno = str(self.campo).encode("utf-8")
        for subcampo in self.subcampos:
            retorno +='$'+str(subcampo.letra).encode("utf-8")+': '+str(subcampo.valor).encode("utf-8")
        return retorno
    
    @staticmethod
    def fieldToCampo(field, campo):
      """
        Convierte un objeto de tipo Field de la biblioteca pymarc en uno de la clase Campo.

        Args:
          Field (Field): campo que se quiere convertir a Campo.
          Campo (Campo): campo de muestra para convertir el Field. 
                         Contendra el campo y los subcampos que se van a necesitar en el campo de retorno.

        Return: el campo convertido segun lo especificado en el arg "campo"
      """
      retorno = False
      if(field.tag == campo.campo):
        retorno = Campo(campo.campo, [])
        for scEnCampo in campo.subcampos:
            listaSCEnField = getSubfields(field, scEnCampo.letra) 
            if(len(listaSCEnField) > 0):
                for scEnField in listaSCEnField:
                    valor = getValorSubfield(scEnField)
                    retorno.subcampos.append(Subcampo(scEnCampo.letra, valor))
        return retorno



        

       
      

