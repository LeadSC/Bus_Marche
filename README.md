# Bus_Marche

## Progetto Piattaforme Digitali per la Gestione del Territorio ##

### Appello: ###
* Secondo appello sessione estiva 2018/2019

### Alunni: ###
* [Andrea Pasero](https://github.com/Bilashos)
* [Simone Cecchetelli](https://github.com/LeadSC)

-----------------------------------------------------

### Descrizione ###

Il progetto Bus_Marche si pone come obbiettivi primari:
* La ricerca delle linee dell'Adriabus nei territori comunali di Pesaro, Urbino e Fano
* Ricerca di una linea con la rispettiva fermata più vicina
* Mostrare i prezzi delle linee Urbane e Extraurbane

### Schema ###
<p align="center">
    <img width="460" height="300" src="https://github.com/LeadSC/Bus_Marche/blob/master/img/Schema.jpg">
 </p>

-----------------------------------------------------

## Relazione ##

Il progetto è composto da 3 obbiettivi principali:
 * Realizzazione di un API (GET) in python
 * Implementazione di un BotTelegram (Python)
 * Creazione di un database mySQL in python



 ----------------------------------------------------
### Bus_Marche API ###

Realizzazione di un API (GET ) che prende i dati dal database mySQL:

  * Gli step dell'algoritmo per l'acquisizione dei dati che poi verrano restituiti in formato JSON, sono i seguenti:

  * Effettuata una richiesta HTTP per accedere ai dati desiderati
  * Effettuato il parsing dei dati ricevuti 
  * Manipolazione dei dati ottenuti 
  * Restituisce il JSON

Oltre alle API create da noi, sono state utilizzate delle API di Google per effettuare le seguenti operazioni:
  
  * Trasformare latitudine e longitudine nel nome della località
  * Calcolare la distanza dalla posizione attuale alla fermata più vicina
    
  * Stadi dell'algoritmo:
      * Effettuata una richiesta HTTP per accedere ai dati desiderati
      * Effettuato il parsing dei dati ricevuti 
      * Manipolazione dei dati ottenuti 
      * Restituisce il JSON


------------------------------------

### Bus_Marche Bot ###

Bus_Marche è un bot che permette all'utente di cercare la sua linea preferita e conoscerne la fermata più vicina, inoltre l'utente può visualizzare tutte le linee dell'Adriabus filtrate per i comuni. Infine dispone di un piccolo listino prezzi per le tratte ExtraUrbane ed Urbane.
Questo bot è stato realizzato in Python usando la libreria Telepot. Si interfaccia alle API create da noi ed al database tramite le API.




----------------------------------------------------------
### Links e riferimenti ### 
 * Link delle OpenData delle linee dell'autobus: https://www.dati.gov.it/dataset/trasporto-pubblico-locale-gtfs
 


