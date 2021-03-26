import zipfile
import os
import sys
from tempfile import TemporaryDirectory
from dbfread import DBF

#---------------Estrae l'archivio .zip nella cartella corrente-----------------
def apriFileZip(daAprire):
    with zipfile.ZipFile(str(mainDir) + '/'+ str(daAprire), 'r') as zippete: #apre il file .zip dalla cartella in cui è stato fatto partire lo script
        zippete.extractall(tempDir) #e lo estrae nella cartella temporanea
        
#-----------------Controlla che nella Current Directory ci siano dei file .zip-----------------------------        
def cercaFile():
    found = 0
    for file in listaFileZip:
        if os.path.exists(file):
            found += 1
            if found == 1:
                print("Ho trovato i seguenti file: \n")
            print(str(found) + ": " + file)

    if (not os.path.exists("*.zip")) and found == 0:
        print("Non ho trovato nessun file .zip :(")
        found = 0
    return found

#--------------Controlla che il file .zip contenga i 4 tipi di file richiesti dal SINFI
def controllaCartellaDentroZip(nomeZip):
    countDBF = 0
    countPRJ = 0
    countSHP = 0
    countSHX = 0
    if os.path.isdir(str(tempDir) + '/' + str(nomeZip)) == True:       #Un archivio nel formato del SINFI prevede che al suo interno vi sia una cartella con lo
        with os.scandir(str(tempDir) + '/' + str(nomeZip)) as entries: #stesso nome del .zip stesso (a meno dell'estensione)
            for entry in entries:
                if entry.name.endswith(".dbf"):
                    countDBF += 1
                if entry.name.endswith(".prj"):
                    countPRJ += 1
                if entry.name.endswith(".shp"):
                    countSHP += 1
                if entry.name.endswith(".shx"):
                    countSHX += 1
            if countDBF == 1 and countPRJ == 1 and countSHP == 1 and countSHX == 1:
                return True
            else:
                return False
    else:
        return False
#---------Estrapola diverse informazioni dal file .dbf (es: lunghezza totale dei cavi)-------------------------------------
def elaboraDBF(nomeDir):
    somma = 0
    massimo = 0
    lista = DBF(str(tempDir) + '/' + str(nomeDir) + '/' + '*.dbf', load=True) #Prende il file .dbf estratto nella cartella temporanea e lo converte in una lista 
                                            #utilizzabile da Python
    for i in range(0,len(lista)):
        print("ID tratta: " + str(lista.records[i]['ID']) + "; lunghezza: " + str(lista.records[i]['lunghezza']) +" m")
        somma += lista.records[i]['lunghezza']
        if lista.records[i]['lunghezza'] > massimo:
            massimo = lista.records[i]['lunghezza']
            id = lista.records[i]['ID']
    print("\nIn totale nel database sono presenti " + str(len(lista)) + " tratte")
    print("La lunghezza di tutte le tratte sommate è: " + str(round(somma, 3)) + " m")
    print("Intervallo di confidenza al 5%: [" + str(round((somma - 0.05*somma), 3)) + " -- " + str(round((somma + 0.05*somma), 3)) + "]")
    print("Il cavo di lunghezza massima è lungo: " + str(massimo) + "m e il suo ID è: " + str(id))
    print("Volendo è possibile aggiungere molte altre funzionalità...")
#-----------------------------------------------------Main----------------------------------------------------
#Fa in modo che la current directory sia quella in cui si trova lo script quando viene fatto partire
pathAssoluto = os.path.abspath(sys.argv[0])
mainDir = os.path.dirname(pathAssoluto)
os.chdir(mainDir)

#Crea una cartella temporanea e la usa per estrarre un eventuale file .zip. Uscendo dal "with" la cartella viene
#automaticamente cancellata

    
#------Scansiono la Current Directory alla ricerca di tutti i fileche termianao con ".zip" e li salvo i rispettivi nomi in una lista di stringhe-------------------
listaFileZip = []
with os.scandir(mainDir) as entries:
    for entry in entries:
        if entry.name.endswith(".zip"):
            listaFileZip.append(entry.name)

trovati = cercaFile() #Restituisce un numero intero pari al numero di file .zip che ha trovato

#-----------------------------In base a quanti file ho trovato, agisco di conseguenza----------------------------------------
if trovati == 0 or trovati == 1 or (trovati>1 and trovati<=len(listaFileZip)): 
    
    if trovati == 0:
        input("Premi invio per chiudere")
    
    if trovati == 1:
        print("\nLavoro sul file: " + str(listaFileZip[0]))
        with TemporaryDirectory() as tempDir: #crea una cartella temporanea in cui estrarre i file .zip
            os.chdir(tempDir)
            print(tempDir)
            apriFileZip('/' + listaFileZip[0])
            nomeZipDaCuiTogliereUltimi4Char = listaFileZip[0]
            if controllaCartellaDentroZip(nomeZipDaCuiTogliereUltimi4Char[:-4]) == True:
                input("Premi invio per continuare...")
                elaboraDBF(nomeZipDaCuiTogliereUltimi4Char[:-4])
            else:
                print("Formato file .zip scelto non conforme al formato SINFI!")
            os.chdir(mainDir)
            input("Premi invio per chiudere")
        
    if trovati > 1:
        try:  
            scelta = int(input("\nScegli il file che vuoi leggere (inserisci un valore intero): "))
        except:
            print("Hai inserito un valore non valido")
        
        if scelta<=len(listaFileZip) and scelta > 0:
            print("Hai scelto: " + str(listaFileZip[scelta - 1]))
            with TemporaryDirectory() as tempDir: #crea una cartella temporanea in cui estrarre i file .zip
                os.chdir(tempDir)           #una volta usciti dal campo del "with" la cartella viene eliminata
                print(tempDir)
                priFileZip(listaFileZip[scelta - 1])
                nomeZipDaCuiTogliereUltimi4Char = listaFileZip[scelta - 1]
                if controllaCartellaDentroZip(nomeZipDaCuiTogliereUltimi4Char[:-4]) == True:
                    input("Premi invio per continuare...")
                    elaboraDBF(nomeZipDaCuiTogliereUltimi4Char[:-4])
                else:
                    print("Formato progetto SINFI errato")
                os.chdir(mainDir)
                input("Premi invio per chiudere")
        else:
            input("Hai inserito un valore non valido!")
else:
    print("valore errato")
    input("Premi invio per chiudere")
