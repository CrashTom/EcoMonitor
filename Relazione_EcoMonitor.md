**EcoMonitor**

*Sistema di monitoraggio ambientale distribuito*

Tommaso Liuzza \| Jacopo Cingia \| Nicola Bonardi

1\. Introduzione

EcoMonitor è un sistema client-server sviluppato in Python per
raccogliere, condividere e visualizzare misure ambientali rilevate dagli
studenti tramite l\'applicazione phyphox. Il progetto è stato realizzato
nell\'ambito dell\'Unità di Apprendimento sulla sostenibilità ambientale
della classe 4EI.

L\'obiettivo principale era costruire un sistema distribuito in cui ogni
studente potesse inviare dati da un sensore al server centrale, che li
elabora e li salva in un file CSV. Una dashboard sviluppata con
Streamlit permette di visualizzare i risultati in tempo reale.

2\. Architettura del sistema

Il sistema è composto da quattro componenti principali:

-   **server.py:** Il server TCP multithreading. Rimane sempre in
    ascolto sulla porta 5000 e crea un thread dedicato per ogni client
    che si connette, gestendo le richieste in parallelo tramite una coda
    condivisa thread-safe.

-   **client.py:** Il client interattivo. Ogni studente avvia il client,
    si identifica con il proprio nome e può inviare misure usando il
    comando INVIA, controllare lo stato della coda con CODA, o chiudere
    la connessione con ESCI.

-   **misure.csv:** Il file di archiviazione. Contiene tutte le misure
    raccolte con le colonne: studente, sensore, valore, luogo, data_ora.

-   **dashboard.py:** La dashboard sviluppata con Streamlit. Legge il
    file CSV e mostra tabella completa, statistiche aggregate e grafici
    interattivi.

3\. Funzionamento del sistema

3.1 Protocollo di comunicazione

La comunicazione avviene tramite socket TCP. Alla connessione, il client
invia il proprio nome nel formato NOME:nomestudente. Il server risponde
con un messaggio di benvenuto e rimane in attesa di comandi. Il
protocollo prevede tre comandi principali:

-   **INVIA:** invia una nuova misura nel formato
    INVIA:sensore,valore,luogo. Il server salva i dati nel CSV e
    risponde con la data e ora correnti.

-   **CODA:** richiede lo stato attuale della coda condivisa, mostrando
    le richieste in elaborazione.

-   **ESCI:** chiude la connessione in modo ordinato.

3.2 Gestione della concorrenza

Il server gestisce più connessioni contemporanee grazie al modulo
threading di Python. Per ogni client viene creato un thread con
daemon=True, in modo che si chiuda automaticamente quando il server
termina. La coda condivisa è implementata con queue.Queue, che è
thread-safe per natura. Per le operazioni sulla lista visibile
(coda_lista) viene usato un oggetto threading.Lock() per evitare
condizioni di gara tra i thread.

3.3 Salvataggio dei dati

I dati vengono salvati nel file misure.csv con apertura in modalità
append (\"a\"), così ogni nuova misura viene aggiunta in fondo senza
sovrascrivere le precedenti. Il file viene creato automaticamente con
l\'intestazione corretta alla prima esecuzione del server, se non esiste
già.

4\. Dashboard Streamlit

La dashboard è sviluppata con il framework Streamlit e utilizza la
libreria pandas per l\'elaborazione dei dati. Alla sua apertura legge il
file misure.csv e mostra:

-   La tabella completa di tutte le misure raccolte.

-   Tre metriche in evidenza: totale misure, valore medio e numero di
    studenti.

-   Un grafico a barre con il valore medio per luogo di rilevazione.

-   Un grafico a barre con il numero di misure inviate da ciascuno
    studente.

La dashboard viene avviata con il comando python -m streamlit run
dashboard.py e si apre automaticamente nel browser sulla porta locale
8501.

5\. Strumenti e tecnologie utilizzate

-   **Python 3:** linguaggio principale per server, client e dashboard.

-   **socket (modulo standard):** comunicazione TCP tra client e server.

-   **threading (modulo standard):** gestione parallela dei client.

-   **queue (modulo standard):** coda condivisa thread-safe.

-   **csv (modulo standard):** lettura e scrittura del file dati.

-   **Streamlit:** framework per la dashboard web interattiva.

-   **pandas:** manipolazione e aggregazione dei dati nella dashboard.

6\. Conclusioni

Il progetto EcoMonitor ha permesso di mettere in pratica i concetti di
programmazione di rete, gestione della concorrenza e visualizzazione dei
dati affrontati durante il corso. Partendo dalla comunicazione TCP con i
socket, abbiamo costruito un sistema completo che va dalla raccolta del
dato ambientale fisico (tramite phyphox) fino alla sua visualizzazione
in una dashboard web.

La gestione dei thread e della coda condivisa è stato l\'aspetto più
delicato, poiché ha richiesto attenzione per evitare race condition tra
i client connessi contemporaneamente. L\'uso di queue.Queue e
threading.Lock() ha permesso di gestire correttamente la
sincronizzazione.

Il sistema è funzionante e rispetta tutti i requisiti della versione
base: server multithreading, coda condivisa, salvataggio CSV e dashboard
con tabelle e grafici.
