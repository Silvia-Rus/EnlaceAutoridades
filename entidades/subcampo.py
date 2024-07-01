
class Subcampo:
    """se define un subcampo con su contenido"""
    letra = ''
    valor = ''
    
    def __init__(self, letra, valor):
        """Se construye el subcampo"""
        self.letra = letra
        self.valor = valor
    
    def __str__(self):
        """Representacion visual del subcampo en formato string."""
        return "$"+self.letra+": "+self.valor
       
    




