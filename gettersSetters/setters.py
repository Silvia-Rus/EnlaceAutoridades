from pymarc import MARCReader

def setCampoSubcampoValor(campo, subcampo, valor):
    """
        Se aniade un subcampo a un campo y se le asigna un valor.

        Args:
            campo (Field): campo al cual se le quiere aniadir el subcampo y el valor.
            subcampo (str): subcampo que se quiere aniadir al campo.
            valor (str): valor que se le quiere asignar al subcampo
    """
    campo.add_subfield(subcampo, valor)

