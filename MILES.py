import PySimpleGUI as sg
import random
from functions import *
from datetime import date
sg.theme('DarkBrown2')
def genNum():
    rangoN= '1'
    while (len(set(rangoN))) != 4:
        rangoN = str(random.randint(1000, 9999))
    return rangoN

def addRankings(lista):
    listaDeListaDeRanks = []
    file = open('../ranks.csv','r')
    leoTodo = file.readlines()
    file.close()
    for e in leoTodo:
        separo = e.split(',')
        nuevaLisAdd = [separo[0],separo[1],separo[2]]
        listaDeListaDeRanks.append(nuevaLisAdd)
    archivo = open('../ranks.csv','w')
    posi = 0
    for e in range(len(listaDeListaDeRanks)):
            if int(listaDeListaDeRanks[e][1])< int(lista[1]): 
                posi = e+1
                continue
    listaDeListaDeRanks.insert(posi,lista)
    for add in listaDeListaDeRanks:
        archivo.writelines(f'{add[0]},{add[1]},{add[2]}')
    archivo.close()

def tablaRanks(h,d):   
    header_list = ['column' + str(x) for x in range(len(d[0]))]
    sg.set_options(element_padding=(0, 0))
    layoutRank = [[sg.Table(values=d,
            headings=h,
            header_background_color='Orange',
            
            # vertical_scroll_only = True,
            hide_vertical_scroll = True,
            max_col_width=30,     
            justification='center',                           
            num_rows=min(5, 20))],
            [sg.Text(key='')],
            [sg.Button('Volver',size= (19,1),button_color=('Orange','Black'))]]
    return layoutRank

def datosJugador(n,i):
    datosFilas = [
        [sg.Text(f'> !HAS GANADO! <')],
        [sg.Text(f'- El numero era {n}')],
        [sg.Text(f'- Intentos {i}')],
        [sg.Text('Nombre'),sg.Input(key='name',size=(15,1))],
        [sg.Text('',key='data',visible=False)],
        [sg.Button('Cargar',button_color=('#F0D201','#020202'))]
    ]
    return datosFilas

def mainMenu():
    main = [ 
        [sg.Image(r'../miles2_30.png',size=(300,40))],
        [sg.Image(r'../THE_GAME _OF _YEAR.png')],
        [sg.Button('Comenzar >',expand_x=True,button_color=('#F0D201','#020202'),font=('Courier New',10),	border_width=5)],
        [sg.Button('Rankings',expand_x=True,button_color=('#F0D201','#020202'),size=(12,1))],
        [sg.Button('Ayuda',expand_x=True,button_color=('#F0D201','#020202'),size=(12,1))],
        [sg.Button('Salir',expand_x=True,button_color=('#CCC9C9','#580302'),font=('Arial ',10),border_width=5)]
        ]
    return main

inicio = sg.Window('MILES', mainMenu(),no_titlebar=True, size=(200,260),element_justification='center',grab_anywhere=True) 
valWin = True
head = ['NOMBRE','INTENTOS','FECHA']
win2_activa = False
while True:
    win2_activa = False
    valRank = True
    eveInicio,valInicio=inicio.read()
    if eveInicio == 'Salir':
        break  
    if eveInicio == 'Comenzar >' and not win2_activa:
        inicio.Hide()
        layout = [
            [sg.Button('Generar Numero',button_color = ('#DC5A09','#020202'),expand_x=True)],
            [sg.Text('Adivina el numero')],
            [sg.Input(key='num1',size=(2,2)),sg.Input(key='num2',size=(2,2)),sg.Input(key='num3',size=(2,2)),sg.Input(key='num4',size=(2,2))],
            [sg.Button('Adivinar',expand_x=True,button_color=('#03B303','#020202'))],
            [sg.Button('Volver',expand_x=True,button_color=('#CCC9C9','#580302'),font=('Arial ',10),size=(4,1))],           
            ]
        game = sg.Window('MILES', layout,no_titlebar=True, size=(150,160),element_justification='center',grab_anywhere=True )        
        cIntentos = 0
        valNum = False
        valWin = True
        win2_activa = True
        while valWin:            
            lisNums = [] 
            eveGame,valGame=game.read()
            if eveGame in [None, 'Volver']:
                game.close()
                win2_activa =False
                inicio.UnHide()
                valWin = False
            elif eveGame =='Generar Numero':
                if not valNum :
                    cIntentos = 0
                    numPc = genNum()
                    valNum = True
                    sg.popup(f'Numero generado',no_titlebar=True)
                else:
                    sg.popup('Tu numero ya a sido generado')
            elif eveGame == 'Adivinar': 
                if valNum == True: 
                    n1 = verificarInt(valGame['num1'])
                    n2 = verificarInt(valGame['num2'])
                    n3 = verificarInt(valGame['num3'])
                    n4 = verificarInt(valGame['num4'])
                    if (n1[0] and n2[0] and n3[0] and n4[0]):
                        if len(valGame['num1'])==1 and len(valGame['num2'])==1 and len(valGame['num3'])==1 and len(valGame['num4'])==1:
                            cIntentos += 1
                            lisNums.append(valGame['num1'])
                            lisNums.append(valGame['num2'])
                            lisNums.append(valGame['num3'])
                            lisNums.append(valGame['num4'])
                            regular = 0
                            bien = 0 
                            for buscar in range(4):               
                                if lisNums[buscar] in numPc:           
                                    if lisNums[buscar] == numPc[buscar]:
                                        bien += 1 
                                    else: 
                                        regular += 1 
                            if bien == 4:
                                fecHoy = todaysDate()
                                gane=sg.Window('GANASTE',datosJugador(numPc,cIntentos),no_titlebar=True,element_justification='center' )
                                while True:
                                    eveGane,valGane=gane.read()
                                    if eveGane == 'Cargar':
                                        if  valGane['name'] != '' and ' ' not in valGane['name']:
                                            valNum = False
                                            cargaData = [valGane['name'],str(cIntentos),f'{fecHoy}\n']
                                            addRankings(cargaData)
                                            game['num1'].update('')
                                            game['num2'].update('')
                                            game['num3'].update('')
                                            game['num4'].update('')                                            
                                            gane.close()
                                            break
                                        else:
                                            gane['data'].update('Nombre invalido',visible=True)
                            else: 
                                sg.popup('Sigue intentando',f'Bien = {bien} \r Regular = {regular}',no_titlebar=True)                        
                        else:   
                            sg.popup('Error','Los valores ingresados no son validos.',no_titlebar=True,auto_close = True ,auto_close_duration = 5)
                            game['num1'].update('')                  
                            game['num2'].update('')                  
                            game['num3'].update('')                  
                            game['num4'].update('')
                    else:   
                        sg.popup('Error','Los valores ingresados no son validos.',no_titlebar=True,auto_close = True ,auto_close_duration = 5)
                        game['num1'].update('')                  
                        game['num2'].update('')                  
                        game['num3'].update('')                  
                        game['num4'].update('')
                else:
                    sg.popup('Debe generar un numero',no_titlebar=True,auto_close = True ,auto_close_duration = 5)
    elif eveInicio == 'Rankings':
        a = open('../ranks.csv','r')
        b = a.readlines()
        listaDeListaRank=[]
        for e in b:
            separo= e.split(',')
            nuevaL = [separo[0],separo[1],separo[2]]
            listaDeListaRank.append(nuevaL)
        windowRank= sg.Window('RANKINGS', tablaRanks(head,listaDeListaRank),no_titlebar=True,grab_anywhere=True,element_justification='center' )
        while valRank:
            evento, valor = windowRank.read()
            if evento in [None, 'Volver']:
                windowRank.close()
                valRank = False            
                
    elif eveInicio == 'Ayuda':
        sg.popup('                                     AYUDA',
        ' > Este juego consiste en adivinar un número de 4 cifras que piensa la computadora.\n \n > Si un dígito del usuario está en el número de la computadora la respuesta será:   \n    - BIEN, si esta en la misma posición   \n    - REGULAR, si esta presente pero en otra posición',
        no_titlebar=True,grab_anywhere=True)

inicio.close() 