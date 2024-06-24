
class Subcampo:
    """se define un subcampo con su contenido"""
    letra = ''
    valor = ''
    
    def __init__(self, letra, valor):
        self.letra = letra
        self.valor = valor
    
    def __str__(self):
        return "$"+self.letra+": "+self.valor
       
    




