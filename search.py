
import os
import trie
import htmlparser
from time import time
import graf


htmlparser = htmlparser.Parser()
grafika = graf.Graph()

def ucitavanje_fajlova(putanja):
    fajlovi =[]

    for root_dir, sub_dirs, files in os.walk(putanja):
        for nesto in files:
            ime=root_dir+"\\"+nesto
            fajlovi.append(ime)

    return fajlovi


linkovi = {}
def indeks_pojavljivanja(fajlovi):
    stablo = trie.Trie()

    
    for fajl in fajlovi:

        if fajl.endswith('.html'):
            linkovi, reci = htmlparser.parse(fajl)


            for link in linkovi:
            
                lista = [link,fajl]
                grafika.add_edge(lista)

            for i in range(len(reci)):
                
                stablo.insert(reci[i].lower(),fajl,i)

    
    return stablo,grafika.graph_dict
    
def ispis_teksta(fajl):
    stablo = trie.Trie()
    links,words = htmlparser.parse(fajl)

    for i in range(len(words)):
        stablo.insert(words[i].lower(),fajl,i)

    
    return stablo,words


def pravljenje(recnik):

    lista=list(recnik.items())


    x = len(lista)
    sortirani_recnik = {}

    for i in range(x-1):
        for j in range(i+1,x):
            if lista[i][1] < lista[j][1]:
                t=lista[i]
                lista[i]=lista[j]
                lista[j]=t

        sortirani_recnik=dict(lista)    
    
    return sortirani_recnik


def search_engine():

    while True:
    
        konacna_lista = []

        komanda_putanja = input('\nUnesite ime direktorijuma kog zelite da pretrazite ili konacnu putanju odvojenu ("\\") \n\n>>:')

        os.path.normpath(komanda_putanja)
    
        if "/" in komanda_putanja:
            print("Niste pravilno uneli konacnu putanju!")
            continue

        elif not "\\" in komanda_putanja:
            print('Niste pravilno uneli konacnu putanju!')
            continue 

        if  os.path.isdir(komanda_putanja):
        
            fajlovi = ucitavanje_fajlova(komanda_putanja)

            vreme1 = time()
            stablo1,graf1 = indeks_pojavljivanja(fajlovi)
            vreme2 = time()

            print('Vreme:',vreme2 - vreme1,'s')
            
            prevara = True

            while prevara:

                unesi_rec = input('\nUnesite rec po kojoj zelite da pretrazite fajlove\nX za nazad\n>>:')

                if unesi_rec.upper() == 'X':
                    break


                if "AND" in unesi_rec:

                    listic_reci = unesi_rec.split()
        
                    if len(listic_reci)==3:

                        reci = [listic_reci[0],listic_reci[2]]

                        recnik_bodovan = {}
                        reci[0]= reci[0].strip()
                        reci[1] = reci[1].strip()
                        recnik_pojavljivanja1 = stablo1.query(reci[0].lower())
                        recnik_pojavljivanja2 = stablo1.query(reci[1].lower())

                        if recnik_pojavljivanja1 and recnik_pojavljivanja2:

                            for kljuc in recnik_pojavljivanja1:
                                bodovi = 0

                                if kljuc in recnik_pojavljivanja2:
                                    bodovi = 20 *  len(recnik_pojavljivanja1[kljuc])+ 20 * len(recnik_pojavljivanja2[kljuc]) 
                                
                                    if kljuc in graf1.keys():

                                        bodovi = bodovi + len(graf1[kljuc])

                                        for link in graf1[kljuc]:
                                            
                                            if link in recnik_pojavljivanja1.keys() and link in recnik_pojavljivanja2.keys() :
                                                bodovi = bodovi + len(recnik_pojavljivanja1[link]) + len(recnik_pojavljivanja2[link])
                                            
                                            else:
                                                pass
                                    else:
                                        pass
                                
                                    recnik_bodovan[kljuc]=bodovi
                        else:
                            print('Nema rezultata za datu pretragu!')
                    
                    else:
                        print("Niste pravilno uneli reci!")
                        continue

                elif "OR" in unesi_rec:
                    listic_reci = unesi_rec.split()

                    if len(listic_reci)==3:
                        
                        reci = [listic_reci[0],listic_reci[2]]

                        recnik_bodovan = {}
                        for rec in reci:

                            rec = rec.strip()

                            recnik_pojavljivanja = stablo1.query(rec.lower())

                            if recnik_pojavljivanja:


                                for kljuc in recnik_pojavljivanja:
                                    bodovi = 0
                                    bodovi = 20 * len(recnik_pojavljivanja[kljuc])

                                    if kljuc in graf1.keys():
                                    
                                        bodovi = bodovi + len(graf1[kljuc])

                                        
                                        for link in graf1[kljuc]:
                                            
                                            if link in recnik_pojavljivanja.keys():
                                        
                                                bodovi = bodovi + len(recnik_pojavljivanja[link])

                                            else:
                                                pass
                                    else:
                                        pass
                                    
                                    if kljuc in recnik_bodovan.keys():
                                        recnik_bodovan[kljuc] += bodovi
                                    else:
                                        recnik_bodovan[kljuc] = bodovi

                    else:
                        print('Niste pravilno uneli reci!')
                        continue

                elif "NOT" in unesi_rec:
                    listic_reci = unesi_rec.split()
        
                    if len(listic_reci)==3:

                        reci = [listic_reci[0],listic_reci[2]]

                        recnik_bodovan = {}
                        reci[0]= reci[0].strip()
                        reci[1] = reci[1].strip()
                        recnik_pojavljivanja1 = stablo1.query(reci[0].lower())
                        recnik_pojavljivanja2 = stablo1.query(reci[1].lower())

                        if recnik_pojavljivanja1 and recnik_pojavljivanja2:

                            for kljuc in recnik_pojavljivanja1:
                                bodovi = 0

                                if kljuc not in recnik_pojavljivanja2.keys():

                                    bodovi = 20 *  len(recnik_pojavljivanja1[kljuc])
                                
                                    if kljuc in graf1.keys():

                                        bodovi = bodovi + len(graf1[kljuc])

                                        for link in graf1[kljuc]:
                                            
                                            if link in recnik_pojavljivanja1.keys():
                                                bodovi = bodovi + len(recnik_pojavljivanja1[link])
                                            
                                
                                
                                    recnik_bodovan[kljuc]=bodovi

                        elif recnik_pojavljivanja1:

                            for kljuc in recnik_pojavljivanja1:
                                bodovi = 0

                                bodovi = 20 *  len(recnik_pojavljivanja1[kljuc])
                            
                                if kljuc in graf1.keys():

                                    bodovi = bodovi + len(graf1[kljuc])

                                    for link in graf1[kljuc]:
                                        
                                        if link in recnik_pojavljivanja1.keys():
                                            bodovi = bodovi + len(recnik_pojavljivanja1[link])
                                        
                            
                            
                                recnik_bodovan[kljuc]=bodovi


                    else:
                        print("Niste pravilno uneli reci!")
                        continue

                else:
                    reci = unesi_rec.split()

                    recnik_bodovan = {}
                    for rec in reci:

                        rec = rec.strip()

                        recnik_pojavljivanja = stablo1.query(rec.lower())

                        if recnik_pojavljivanja:


                            for kljuc in recnik_pojavljivanja:
                                bodovi = 0
                                bodovi = 20 * len(recnik_pojavljivanja[kljuc])

                                if kljuc in graf1.keys():
                                
                                    bodovi = bodovi + len(graf1[kljuc])

                                    
                                    for link in graf1[kljuc]:
                                        
                                        if link in recnik_pojavljivanja.keys():
                                    
                                            bodovi = bodovi + len(recnik_pojavljivanja[link])

                                        else:
                                            pass
                                else:
                                    pass
                                
                                if kljuc in recnik_bodovan.keys():
                                    recnik_bodovan[kljuc] += bodovi
                                else:
                                    recnik_bodovan[kljuc] = bodovi

                
                sortirano = pravljenje(recnik_bodovan)
                lista_sortiranih = list(sortirano)

                if len(lista_sortiranih) > 0 :

                    if 'OR' in unesi_rec:

                        reci = unesi_rec.split("OR")
                        kljuc12 = lista_sortiranih[0]
                        stablo_za,lista_reci = ispis_teksta(kljuc12)

                        for rec in reci:
                            rec = rec.strip()

                            stablo_indeksi = stablo_za.query(rec.lower())
                            if stablo_indeksi:
                

                                if stablo_indeksi[kljuc12][0] + 10 < len(lista_reci):
                                    for i in range(10):
                                        broj = stablo_indeksi[kljuc12][0] + i 
                                        lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[broj]
                                else:
                                    for i in range(stablo_indeksi[kljuc12][0]-10,stablo_indeksi[kljuc12][0]):
                                        lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[i]
                        
                    elif 'NOT' in unesi_rec:

                        reci = unesi_rec.split("NOT")
                        kljuc12 = lista_sortiranih[0]
                        stablo_za,lista_reci = ispis_teksta(kljuc12)

                        rec = reci[0].strip()

                        
                        stablo_indeksi = stablo_za.query(rec.lower())
                        if stablo_indeksi:


                            if stablo_indeksi[kljuc12][0] + 10 < len(lista_reci):
                                for i in range(10):
                                    broj = stablo_indeksi[kljuc12][0] + i 
                                    lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[broj]
                            
                            else:

                                for i in range(stablo_indeksi[kljuc12][0]-10,stablo_indeksi[kljuc12][0]):
                                    lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[i]
                    
                    elif 'AND' in unesi_rec:

                        reci = unesi_rec.split("AND")
                        kljuc12 = lista_sortiranih[0]
                        stablo_za,lista_reci = ispis_teksta(kljuc12)

                        for rec in reci:
                            rec = rec.strip()

                            stablo_indeksi = stablo_za.query(rec.lower())
                            if stablo_indeksi:

                                if stablo_indeksi[kljuc12][0] + 5 < len(lista_reci):
                                    for i in range(5):
                                        broj = stablo_indeksi[kljuc12][0] + i 
                                        lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[broj]
                                
                                else:
                                    for i in range(stablo_indeksi[kljuc12][0]-10,stablo_indeksi[kljuc12][0]):
                                        lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[i]


                    
                    else:
                        reci = unesi_rec.split()

                        kljuc12 = lista_sortiranih[0]
                        stablo_za,lista_reci = ispis_teksta(kljuc12)

                        for rec in reci:
                            rec = rec.strip()

                            stablo_indeksi = stablo_za.query(rec.lower())
                            if stablo_indeksi:
                    

                                if stablo_indeksi[kljuc12][0] + 10 < len(lista_reci):
                                    for i in range(10):
                                        broj = stablo_indeksi[kljuc12][0] + i 
                                        lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[broj]
                                
                                else:
                                    for i in range(stablo_indeksi[kljuc12][0]-10,stablo_indeksi[kljuc12][0]):
                                        lista_sortiranih[0] = lista_sortiranih[0] + " " + lista_reci[i]
                
                else:
                    print('Nema rezultata za pretrazenu rec!')


                try:
                    print('Ima ',len(lista_sortiranih),' rezultata pretrage.')
                    unesi_broj = int(input('\nUnesite broj rezultata koliko zelite da budu prikazani\n\n>>: '))

                except:
                    print("Niste uneli broj!")

                    continue

                if len(konacna_lista)==0:
                    
                    if unesi_broj < len(lista_sortiranih):
                        for i in range(unesi_broj):
                            print(i+1,'.',' ',lista_sortiranih[i])
                            konacna_lista.append(lista_sortiranih[i])
                    
                    else:
                        for i in range(len(lista_sortiranih)):
                            print(i+1,'.',' ',lista_sortiranih[i])
                            konacna_lista.append(lista_sortiranih[i])

                
                else:
                    if unesi_broj < len(lista_sortiranih):
                        y = len(konacna_lista)
                        for i in range(y):
                            print(i+1,'.','',konacna_lista[i])
                        print('\n===NOVI REZULTATI PRETRAGE===\n')

                        for i in range(unesi_broj):
                            print(i+1,'.','',lista_sortiranih[i])
                            konacna_lista.append(lista_sortiranih[i])
                    
                    else:
                        y = len(konacna_lista)

                        for i in range(y):
                            print(i+1,'.','',konacna_lista[i])
                        print('\n===NOVI REZULTATI PRETRAGE===\n')

                        for i in range(len(lista_sortiranih)):
                            print(i+1,'.','',lista_sortiranih[i])
                            konacna_lista.append(lista_sortiranih[i])

                
                while True:
                    lista_sortiranih = []
                    nastavak = input('\nDa li zelite da nastavite sa unosom u istom direktorijumu\n1.DA\n2.NE\n\n>>:')
                    if nastavak.upper()=='DA':
                        break

                    elif nastavak.upper()=='NE':
                        prevara = False
                        break

                    else:
                        print('\nNepravilan unos!')

        else:
            print("Niste pravilno uneli konacnu putanju!")