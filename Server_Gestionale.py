import mysql.connector
from mysql.connector import FieldType as Ft
import socket 
import Facilities as F
import threading as th

#---------FUNZIONI BASE--------------------FUNZIONI BASE-----------------------FUNZIONI BASE--------------------FUNZIONI BASE

def scegli_porta_logica(cont,listaPL,conn):
    porta_logica = 0
    if(cont!=0):
        while(porta_logica<1 or porta_logica>2 ):
            porta_logica = int(F.input_send('Scegli la porta logica, Inserisci\n1-AND\n2-OR\n-->',conn))
        if(porta_logica==1):
            listaPL.append('AND')
        else:
            listaPL.append('OR')
    else:
        listaPL.append('AND')
        cont = 1

def manage_between(conn_client):
    data_i = F.input_send('Inserisci data iniziale(YYYY-MM-GG o YYYY/MM/GG):',conn_client)
    data_f = F.input_send('Inserisci data finale(YYYY-MM-GG o YYYY/MM/GG):',conn_client)
    return f"'{data_i}' AND '{data_f}'"


def controllo_tipo(column,cur,field_names,incr):
    field_types = [i[1] for i in cur.description]
    print(field_types)
    print(field_names)
    for i in range(0,len(field_names)):
        if field_names[i] == column:
            result = Ft.get_info(field_types[i+incr])
            if result=='VAR_STRING':
                return('1')
            elif result =='LONG':
                return('2')
            elif result =='DATE':
                return('3')
            elif result =='FLOAT':
                return('4')
            else:
                print('Errore')

def manage_single_input(conn_client,column,field_names,cur,frase,incr):
    data_type = controllo_tipo(column,cur,field_names,incr)
    print(data_type)
    print(column)
    if(data_type=='2' or data_type=='4'):
        while(numero<0):
            numero = int(F.input_send(f'{frase}(valore numerico):',conn_client))
        valore = str(numero)
    elif (data_type=='3'):
        valore = F.input_send(f'{frase}(YYYY-MM-GG o YYYY/MM/GG):',conn_client)
    else:
        valore = F.input_send(f'{frase}:',conn_client)
    return valore

def create_menu(name_list):
    frase=''
    for i in range(0,len(name_list)):
        frase+=f'\n{i}-{name_list[i]}'
    return frase

def controllo_inserimento(frase,lista,conn,incr_in,incr_fin):
    scelta=-1
    while(scelta<0+incr_in or scelta>len(lista)+incr_fin):
        scelta=int(F.input_send(frase,conn))
    return scelta

def scegli_nome_tabella(cur,conn):
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'azienda'"
    cur.execute(query)
    dati = cur.fetchall()
    F.send_a_list(dati,conn)
    flag = True
    while(flag):
        nome_tabella = F.input_send('Inserisci il nome della tabella:',conn)
        for i in dati:
            if(nome_tabella==i[0]) : 
                flag=False
                break
    return nome_tabella

def scegli_condizione(conn_client,data_type,colonna):
    diz_operatori = {'1':'<','2':'>','3':'<=','4':'>=','5':'=','6':'<>','7':' BETWEEN '}
    frase = "Scegli l'operatore di diseguaglianza(<,>, ect...)\n1 - '<'\n2 - '>'\n3 - '<='\n4 - '>='\n5 - '='\n6 - '<>'\n"
    if(data_type=='2' or data_type=='4'):
        frase += '-->'
        operatore = diz_operatori[str(controllo_inserimento(frase,[1,2,3,4,5,6],conn_client,1,0))]
        numero = -1
        while(numero<0):
            numero = int(F.input_send(f'Inserisci valore per la seguente condizione\n{colonna}{operatore}',conn_client))
        valore = str(numero)
    elif (data_type=='3'):
        frase += "7 - BETWEEN(confronta la data con un range di date, restituisce True solo se essa è inclusa nel range)\n-->"
        operatore = diz_operatori[str(controllo_inserimento(frase,[1,2,3,4,5,6,7],conn_client,1,0))]
        if(operatore==diz_operatori['7']):
            valore = manage_between(conn_client)
        else:
            valore = F.input_send(f'Inserisci data(YYYY-MM-GG o YYYY/MM/GG) per la seguente condizione\n{colonna}{operatore}',conn_client)
    else:
        operatore = diz_operatori['5']
        valore = F.input_send(f'Inserisci stringa per la seguente condizione\n{colonna}{operatore}',conn_client)
    return valore,operatore


def create_query_update(conn_client,field_names,cur):
    valori = []
    num_mod = 0
    while(True):
        for i in range(0,len(field_names)):
            scelta = controllo_inserimento(f'Vuoi modificare il campo {field_names[i]}(1-si,2-no):',[1,2],conn_client,1,0)
            if scelta==1:
                ins = manage_single_input(conn_client,field_names[i],field_names,cur,f'Inserisci {field_names[i]}',1)
                valori.append({field_names[i] : ins})
                num_mod += 1
        print(valori)
        modifiche = ''
        cont = 0
        for i in valori:
            print(i)
            for key,value in i.items():
                if(cont!=num_mod-1):
                    modifiche += f"{key} = '{value}',"
                else:
                    modifiche += f"{key} = '{value}'"
                cont+=1
        print(modifiche)
        break
    return modifiche
    
        

def create_query_select(cur,conn_client):
    field_names = [i[0] for i in cur.description]
    frase_1 = 'Scegli la colonna su cui fare la condizione:'
    frase_1 += create_menu(field_names)
    frase_1 +=f'\n{len(field_names)}-Concludi inserimento colonne\n-->'
    print(frase_1)
    parametri = []
    listaPL = []
    listaTC = []
    cont=0
    frase = 'Ecco le condizioni create --> WHERE 1=1 '
    visua_attr = []
    flag = False
    for i in range(0,len(field_names)):
        if i == 0:
            scelta = controllo_inserimento("Inserisci 1 - Se vuoi visulizzare tutti i cambi della tabella, 2 - Passa all'inserimento dei campi singoli:",[1,2],conn_client,0,0)
            if scelta == 1 : 
                flag = True
                visua_attr.append('*')
        elif flag!=True:
            scelta = controllo_inserimento(f'Vuoi visualizzare il campo {field_names[i]}(1-si,2-no):',[1,2],conn_client,1,0)
            if scelta==1:
                visua_attr.append(f"{field_names[i]}")
    while(True):
        scelta_col = controllo_inserimento(frase_1,field_names,conn_client,0,0)
        if scelta_col==len(field_names) : break
        tipo = controllo_tipo(field_names[scelta_col],cur,field_names,0)
        valore , operatore = scegli_condizione(conn_client,tipo,field_names[scelta_col])
        listaTC.append(operatore)
        if(operatore==' BETWEEN '):
            parametri.append({field_names[scelta_col] : valore})
        else:
            parametri.append({field_names[scelta_col] : f"'{valore}'"})
        scegli_porta_logica(cont,listaPL,conn_client)
        frase += f'{listaPL[cont]} {field_names[scelta_col]}{listaTC[cont]}{parametri[cont][field_names[scelta_col]]} '
        conn_client.send(frase.encode())
        conn_client.recv(1024)
        cont+=1
    
    campi = ''

    for i in range(0,len(visua_attr)):
        if i==len(visua_attr)-1:
            campi += f"{visua_attr[i]} "
        else:
            campi += f"{visua_attr[i]},"

    clausole = ''
    l = -1
    flag = False
    for i in parametri:
        l += 1
        for key,value in i.items():
            if(listaTC[l]==' BETWEEN '):
                flag = True
                indice = l
                k = key
                v = value
            else:
                clausole += f"{listaPL[l]} {key}{listaTC[l]}{value} "

        if flag == True : clausole += f"{listaPL[indice]} {k}{listaTC[indice]}{v} "
    return clausole , campi

#def create_query_insert(cur):
    field_names = [i[0] for i in cur.description]
    valori = [[]]
    k=-1
    while(True):
        k+=1
        for i in range(1,len(field_names)):
            ins = input(f'Inserisci {field_names[i]}:')
            valori[k].append(ins)
        scelta=0
        
        while(scelta<1 or scelta>2):
            scelta=int(input('Inserisci\n1-Continua\n2-Concludi\n-->'))
        if scelta==2:break
    query = f" ({', '.join(field_names[1::])}) VALUES"
    for k in valori:
        query+='('
        for i in range(0,len(k)):
            if(i==len(k)-1):
                query += "'" + k[i]+"'"+')'
            else:
                query += "'" + k[i]+"'"+','
    print(query)
    return query

def create_query_insert(nome, tupla):
    msg = f"""INSERT INTO {nome}("""
    tup = ', '.join(tupla)
    msg += (tup +')')
    msg +=  ' VALUES '
    val = ','.join(['%s']*len(tupla))
    msg += f'({val})'
   
    return msg


def delete_column(conn,cur,lock):
    nome_tabella = scegli_nome_tabella(cur,conn)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    cur.fetchall()
    field_names = [i[0] for i in cur.description]
    frase = 'Scegli la colonna su cui fare la condizione:'
    frase += create_menu(field_names)
    frase +='\n-->'
    scelta_col = controllo_inserimento(frase,field_names,conn,0,0)
    query =f'ALTER TABLE {nome_tabella} DROP COLUMN {field_names[scelta_col]}'
    with lock:
        cur.execute(query)


def alter_record(conn_client,cur,conn,lock):
    nome_tabella = scegli_nome_tabella(cur,conn_client)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    data = cur.fetchall()
    field_names = [i[0] for i in cur.description]
    conn_client.send(f'Ecco i record prensenti sulla tabella {nome_tabella}:'.encode())
    conn_client.recv(1024)
    F.send_a_list(data,conn_client)
    query = f'UPDATE {nome_tabella} SET '
    while(True):
        flag = False
        id = int(F.input_send("Scegli l'ID del record che vuoi modificare:",conn_client))
        for i in data:
            if(i[0])==id: 
                query += create_query_update(conn_client,field_names[1::],cur)
                flag = True
        if flag == True:
            query += f' WHERE {field_names[0]}={id}'
            break
    with lock:
        conn_client.send(f'Ecco la query completa:\n{query}'.encode())
        conn_client.recv(1024)
        cur.execute(query)
        conn.commit()
        conn_client.send(f'Record modificato correttamente, ecco come si presenta la tabella {nome_tabella}...'.encode())
        conn_client.recv(1024)
        cur.execute(f'SELECT * FROM {nome_tabella}')
        data = cur.fetchall()
        F.send_a_list(data,conn_client)

def delete_record(conn_client,cur,conn,lock):
    
    nome_tabella = scegli_nome_tabella(cur,conn_client)
    print(nome_tabella)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    data = cur.fetchall()
    field_names = [i[0] for i in cur.description]
    conn_client.send(f'Ecco i record prensenti sulla tabella {nome_tabella}:'.encode())
    conn_client.recv(1024)
    F.send_a_list(data,conn_client)
    query = f'DELETE FROM {nome_tabella} WHERE('
    while(True):
        flag = False
        id = int(F.input_send("Scegli l'ID del record che vuoi modificare:",conn_client))
        for i in data:
            if(i[0])==id: 
                flag = True
        if flag == True:
            scelta = controllo_inserimento('Scegli 1-Continua 2-Esci :',[1,2],conn_client,0,0)
            if scelta == 1:
                query += f'{field_names[0]}={id} OR '
            if scelta == 2:
                query += f'{field_names[0]}={id})'
                break
    with lock:
        conn_client.send(f'Ecco la query completa:\n{query}'.encode())
        conn_client.recv(1024)
        cur.execute(query)
        conn.commit()
        conn_client.send(f'Record modificato correttamente, ecco come si presenta la tabella {nome_tabella}...'.encode())
        conn_client.recv(1024)
        cur.execute(f'SELECT * FROM {nome_tabella}')
        data = cur.fetchall()
        F.send_a_list(data,conn_client)

#---------------------------------------------------------------------------------------------------------------
#---------------FUNZIONI MENU--------------------FUNZIONI MENU-----------------------FUNZIONI MENU-------------- 
#---------------------------------------------------------------------------------------------------------------
    
def db_insert_into(conn_client,lock):
    with lock:
        conn=F.conn_to_database('127.0.0.1','root','','azienda',3306)
        cur = conn.cursor()
        nome_tabella = scegli_nome_tabella(cur,conn_client)
        cur.execute(f'SELECT * FROM {nome_tabella}')
        cur.fetchall()
        '''
        porz_query = create_query_insert(cur)
        print(nome_tabella)
        query = f"""INSERT INTO {nome_tabella}{porz_query}"""
        '''
        field_names = [i[0] for i in cur.description]
        query = create_query_insert(nome_tabella, field_names[1::])
        print(query)
        valori = []
        k=-1
        while(True):
            k+=1
            valori.append([])
            
            for i in range(1,len(field_names)):
                ins = manage_single_input(conn_client,field_names[i],field_names,cur,f'Inserisci {field_names[i]}',0)
                valori[k].append(ins)
            scelta=0
            
            while(scelta<1 or scelta>2):
                scelta=int(F.input_send('Inserisci\n1-Continua\n2-Concludi\n-->',conn_client))
            if scelta==2:break
        with lock:
            for i in valori:
                conn_client.send(f"{query}'\n' {i}".encode())
                cur.execute(query,tuple(i))
                conn.commit()
            conn_client.send(f'Record inseriti correttamente, ecco come si presenta la tabella {nome_tabella}...'.encode())
            conn_client.recv(1024)
            cur.execute(f'SELECT * FROM {nome_tabella}')
            data = cur.fetchall()
            F.send_a_list(data,conn_client)




def db_read(conn_client):
    conn=F.conn_to_database('127.0.0.1','root','','azienda',3306)
    cur = conn.cursor()
    nome_tabella = scegli_nome_tabella(cur,conn_client)
    cur.execute(f'SELECT * FROM {nome_tabella}')
    cur.fetchall()        
    field_names = [i[1] for i in cur.description]
    print(field_names)
    for i in field_names:
        print(Ft.get_info(i))
    clausole , campi = create_query_select(cur,conn_client)
    query = f"SELECT {campi} FROM {nome_tabella} where 1=1 {clausole}"
    conn_client.send(f'Ecco la query di SELECT : {query}'.encode())
    conn_client.recv(1024)
    print(query)
    cur.execute(query)
    dati = cur.fetchall()
    conn_client.send('Ecco i dati recuperati dal database date le condizioni inserite precedentemente:'.encode())
    conn_client.recv(1024)
    F.send_a_list(dati,conn_client)



def db_alter_record(conn_client,lock):
    conn=F.conn_to_database('127.0.0.1','root','','azienda',3306)
    cur = conn.cursor()
    lista_opzioni = []
    #lista_opzioni.append('Elimina una colonna')
    #lista_opzioni.append('Aggiungi una colonna')
    lista_opzioni.append('Modifica un record già esistente')
    menu = ''
    menu += 'Inserisci'
    menu += create_menu(lista_opzioni)
    menu += f'\n{len(lista_opzioni)}-Esci\n->'
    while(True):
        scelta = controllo_inserimento(menu,lista_opzioni,conn_client,0,0)
        if scelta == 0:
            alter_record(conn_client,cur,conn,lock)
        if scelta == 1:
            break
    
def db_delete_record(conn_client,lock):
    conn=F.conn_to_database('127.0.0.1','root','','azienda',3306)
    cur = conn.cursor()
    lista_opzioni = []
    #lista_opzioni.append('Elimina una colonna')
    #lista_opzioni.append('Aggiungi una colonna')
    lista_opzioni.append('Modifica un record già esistente')
    menu = ''
    menu += 'Inserisci'
    menu += create_menu(lista_opzioni)
    menu += f'\n{len(lista_opzioni)}-Esci\n->'
    while(True):
        scelta = controllo_inserimento(menu,lista_opzioni,conn_client,0,0)
        if scelta == 0:
            delete_record(conn_client,cur,conn,lock)
        if scelta == 1:
            break

#-------------------------------------------------------------------------------------------------------------------------------
#----------------MAIN------------------MAIN---------------------MAIN------------------MAIN------------------MAIN----------------
#-------------------------------------------------------------------------------------------------------------------------------

def menu_iniziale(conn_client,lock):
    ins = ""
    i = 0
    while(i<3 and ins != PASSWORD):
        dati = "Inserisci password," + str(3-i) + " tentativi rimasti:"
        ins = F.input_send(dati,conn_client)
        i+=1
    data = -1

    if(ins == PASSWORD):
        while(data!=5):
            data = controllo_inserimento('Inserisci\n1-Inserire nuovo record\n2-Leggere dati tramite select\n3-Modificare un record\n4-Eliminare un record\n5-Chiudi la connessione\n-->',[1,2,3,4,5],conn_client,0,0)
            if(data==1):
                print('Eseguo nuovo record') #inserire
                db_insert_into(conn_client,lock)  
            elif data==2:
                print('Eseguo leggere dati') #leggere
                db_read(conn_client)  
            elif data==3:
                print('Eseguo modifica record') #modificare
                db_alter_record(conn_client,lock)
            elif data==4:
                print('Eseguo eliminare record') #eliminare
                db_delete_record(conn_client,lock)
        conn_client.send('Chiusura connessione...'.encode())
        conn_client.close()
    else:
        conn_client.send("Tentativi massimi raggiunti. Chiudo la connessione".encode())
        conn_client.close()



if __name__ == "__main__":
    PASSWORD = "gestionale"
    HOST = 'localhost'                 # Nome simbolico che rappresenta il nodo locale
    PORT = 50010              # Porta non privilegiata arbitraria
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("server avviato, in ascolto...")
    i = 0
    lock=th.Lock()
    lista_conn = []
    thread = []
    while True:
        lista_conn.append(s.accept())
        lista_conn[i][0].send('Ciao, Benvenuto nel mio gestionale!'.encode())
        lista_conn[i][0].recv(1024)
        thread.append(th.Thread(target=menu_iniziale,args=(lista_conn[i][0],lock)))
        thread[i].start()
        i=i+1



