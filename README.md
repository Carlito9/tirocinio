### moduli importati
moduli di pubblico dominio:

    import paho.mqtt.client as paho
    import time
    import threading
    import json
    
moduli implementati nel progetto:

    import dicCamera
    import Save
    import hdcam
    import usbcam
    import treDcam
    import synchronizer

## `dicCamera.py`

Modulo il cui unico scopo è generare un dizionario per ogni camera con i parametri ricevuti dal file di configurazione, in seguito verrà aggiornato, convertito in json per poi venire inviato. Non importa nessun modulo.

## `synchronizer.py`

Modulo che sincronizza i vari thread attivi in modo tale da mandarli esecuzione uno alla volta seguendo l'ordine della coda che viene definita in questo modulo e contiene un numero associato ad ogni thread. Quando ogni camera ha acquisito un'immagine mette in pausa il programma per 10 secondi. Le varie funzioni che compongono questo metodo servono unicamente per la gestione della coda: aggiunta e rimozione degli elementi, svuotamento coda, aggiornamento dell'indice al termine dell'acquisizione di un'immagine

### moduli importati

moduli di pubblico dominio:

    import threading
    import time

## `Save.py`

Modulo che si occupa del salvataggio delle immagini per la camera usb e la 3d (**non per le hd**), ciò avviene tramite il salvataggio di array numpy passati come parametri in immagini png a colori (usb, 3d colorate) o in bianco e nero (3d normali). Inoltre sono presenti funzioni per la ricezione dei metadati da associare ad una immagine, i quali vengono allocati in un dizionario in attesa di essere salvati in un file di testo quando verrà salvata un'immagine.

### moduli importati

moduli di pubblico dominio:

    from PIL import Image
    

## `usbcam.py`

Modulo che gestisce la camera usb "Ximea", è costituito da un loop principale che mantiene in esecuzione fin quando la variabile event `e` ha il valore di `set` (il valore viene gestito dalla funzione comunication a meno che non si verifichi un'eccezione). All'interno di questo loop, vengono acquisite le immagini, da inviare al modulo delegato al salvataggio, dopodichè viene aggiornato il dizionario della camera. Tramite parametri contenuti nel file di configurazione è possibile regolare l'esposizione.

### moduli importati
  

modulo specifico della camera:  
 

    from ximea import xiapi  

moduli di pubblico dominio:  

    import threading  
    import time  

moduli implementati nel progetto:  

    import Save  
    import synchronizer  


## `hdcam.py`


Modulo che gestisce le camere hd "Basler", è costituito da un loop principale che mantiene in esecuzione fin quando la variabile event `e` ha il valore di `set` (il valore viene gestito dalla funzione comunication a meno che non si verifichi un'eccezione). All'interno di questo loop, vengono acquisite le immagini, le quali vengono salvate tramite la apposita funzione definita nel modulo pypylon (ll modulo Save è chiamato solo per creare il file di metadati), dopodichè viene aggiornato il dizionario della camera. Tramite parametri contenuti nel file di configurazione è possibile regolare l'esposizione. Particolarità di questo modulo è il fatto che gestisca tre diverse camere dello stesso tipo, mentre la connessione ad ogni camera viene effettuata ricercandone una che abbia lo stesso ip di quello specificato nel file di configurazione.

### moduli importati


modulo specifico della camera:

    from pypylon import pylon,genicam

moduli di pubblico dominio:

    import threading
    import time

moduli implementati nel progetto:

    import Save
    import synchronizer


## `3dcam.py`


Modulo che gestisce la camera 3d "Framos", è costituito da un loop principale che mantiene in esecuzione fin quando la variabile event `e` ha il valore di `set` (il valore viene gestito dalla funzione comunication a meno che non si verifichi un'eccezione). All'interno di questo loop, vengono acquisite le immagini, da inviare al modulo delegato al salvataggio, dopodichè viene aggiornato il dizionario della camera. Tramite parametri contenuti nel file di configurazione è possibile scegliere se acquisire immagini in modalità depth normalmente, quindi in bianco e nero, oppure a colori,tramite una funzione che appunto "colorizza" l'immagine. La connessione alla camera viene effettuata ricercandone una che abbia lo stesso ip di quello specificato nel file di configurazione.

### moduli importati


modulo specifico della camera:

    import pyrealsense2 as rs

moduli di pubblico dominio:

    import threading
    import time
    import numpy as np

moduli implementati nel progetto:

    import Save
    import synchronizer
