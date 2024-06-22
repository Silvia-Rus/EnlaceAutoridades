from pymarc import MARCReader

def setCampoSubcampoValor(campo, subcampo, valor):
    campo.add_subfield(subcampo, valor)

