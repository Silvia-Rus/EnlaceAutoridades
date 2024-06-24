
class EscribirMARC:

    nombreArchivo = ''

    def __init__(self, nombreArchivo):
        self.nombreArchivo = nombreArchivo

    def escribir(self, record):
        with open(self.nombreArchivo, 'a') as out:
            out.write(record.as_marc())