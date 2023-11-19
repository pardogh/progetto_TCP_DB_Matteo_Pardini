## 1) Scarica il database e importalo su phpmyadmin

## 2) Assicurati che le versioni delle tue librerie corrispondano con quelle usate nel programma. Trovi le mie versioni nel file 'requirements.txt'

## 3) Scarica i file .py, dovrebbero essere Server_Gestionale.py, Client_Gestionale.py e Facilities.py

## 4) Avvia per primo il file Server_Gestionale.py

## 5) Avvia poi il file Client_Gestioanale.py

## 6) Come prima cosa inserisci la password, cioé : 'gestionale'

## 7) Ora le funzioni del gestionale dovrebbero essere disponibili

## 8) Spiegazione:
'''
Ho progettato il gestionale con 2 principali intenti: 
1 - Rendere le funzioni del gestionale il più adattabili possibile in base alle esigenze
2 - Gestire più lavoro possibile con il server, lasciando il client il più "leggero" possibile, infatti come si può notare le dimensioni del server confrontate con il client sono decisamente maggiori
3 - Rendere possibile la connessione a più utenti alla volta tramite l'utilizzo del multithreading
Le funzionalità disponibili non sono tante ma decentemente personalizzabili:

1-Select con scelta dei campi visualizzabili oltre che possibilità di imporre varie condizioni a scelta, per rendere la ricerca via via piu complessa
2-Inserimento di un record; tutti i campi sono di tipo NOT NULL, quindi si è "costretti" ad inserire tutti i dati
3-Update di un record con scelta dei campi da cambiare
4-Delete di un record

*Tra le funzionalità aggiuntive ho implementato la possibilità di usare la funzione BETWEEN tra 2 date durante la creazione della query di Visualizzazione
*Per snellire il codice ho implementato alcune funzioni aggiuntive in Facilities per: l'invio di una lista, la ricezione di un input da parte del client e infine la connessione con un database
Il client è modellato in maniera tale da gestire le determinate richieste del server in base ad un codice univoco per il tipo di funzione.
È possibile notare questa particolarità osservando che i codici tipo : '#99' corrispondono sia in Facilities che nelle 2 funzioni presenti nel Client

Specifico che non ho usato costrutti di tipo TRY-->EXCEPTION, quindi la gestione di determinati errori di inserimento non esiste
'''
