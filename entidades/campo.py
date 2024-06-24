from entidades.subcampo import Subcampo
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
        retorno = str(self.campo).encode("utf-8")
        for subcampo in self.subcampos:
            retorno +='$'+str(subcampo.letra).encode("utf-8")+': '+str(subcampo.valor).encode("utf-8")
        return retorno

       
      

