from subcampo import Subcampo
class Campo:
    """campo marc con sus subcampos"""
    campo = ''      # numero de campo
    subcampos = []  # listado de subcampos
    enAut = ''      # encabezamiento en autoridades

    def __init__(self, campo, subcampos):
        self.campo = campo
        self.subcampos = subcampos
        self.enAut = "1"+campo[1]+campo[2]

    def __str__(self):
        retorno = self.campo
        for subcampo in self.subcampos:
            retorno +='$'+subcampo.letra+': '+subcampo.valor
        return retorno

       
      

