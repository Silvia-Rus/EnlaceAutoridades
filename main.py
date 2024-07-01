
import os
from datetime import datetime
from entidades.campo     import Campo
from entidades.subcampo  import Subcampo
from enlazador import Enlazador
from pymarc    import MARCReader
from escribirMarc import EscribirMARC
from informes  import writeCSVCounter
from informes  import initCSV


# biblios = 'archivos/mrcFiles/BIB_TODOS.mrc'
# biblios = 'archivos/mrcFiles/BIB_500REG_1.mrc'
biblios = 'archivos/mrcFiles/BIB_14REG.mrc'
# biblios = 'archivos/mrcFiles/BIB_1REG.mrc'

campo100 = Campo('100', [Subcampo('a', ''), Subcampo('d', '')])
campo110 = Campo('110', [Subcampo('a', ''), Subcampo('b', '')])
campo650 = Campo('650', [Subcampo('a', '')])
campo700 = Campo('700', [Subcampo('a', ''), Subcampo('d', '')])
campo710 = Campo('710', [Subcampo('a', ''), Subcampo('b', '')])
fechaAhora = datetime.now().strftime("%Y%m%d%H%M%S")
nameMrcModified = 'archivos/mrcTransformed/'+fechaAhora+'_BIB_EXPORT.mrc'

listaDeCampos = [campo100, campo110, campo650, campo710, campo700]

e = EscribirMARC(nameMrcModified)
l = Enlazador()

initCSV()

if(len(listaDeCampos) > 0):
    if os.path.exists(biblios):
        with open(biblios, 'rb') as fh:
            reader = MARCReader(fh)
            for record in reader:
                recordBuffer = l.link_auth(listaDeCampos,record)
                e.escribir(recordBuffer)
            print(writeCSVCounter(l.recordCounter, l.unlinkedAuth, l.matchingAuth))
            print("Trasnformacion exitosa:\n"
                  "->Puede ver su archivo mrc modificado en archivos/mrcTransformed.\n"
                  "->Puede ver los informes completos en archivos/reports.")
    else:
           print("No se puede encontrar el archivo .mrc que se quiere modificar. \nRecuerde declararlo correctamente en la variable 'biblios' en el archivo main.py")  
else:
   print("No ha declarado campos para enlazar. \nRecuerde declaralos correctamente en la variable 'listaDeCampos' en el archivo main.py ")
   



   
