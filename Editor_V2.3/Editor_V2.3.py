#!/usr/bin/env python
# # -*- coding: utf-8 -*-

# This file is part of Editor_NAO_V2.3.

# Editor_NAO_V2.3 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# Editor_NAO_V2.3 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Editor_NAO_V2.3. If not, see <https://www.gnu.org/licenses/>.


# Změny:

# Plně funkční editor 
# Vyřešeno ukládání a nahrávání programů 
# Při vypnutí programu nabízí uložit soubor.
# Funguje přidávání/úprava/odstranění příkazů
# Fix změny cesty k souboru
# Vytvořená složka pro ukládání souborů 
# Založení nového souboru s koncovkou .en (editor nao)
#  
# Globální promněnné: 
#     filepath - cesta k editovanému souboru
#     dir - defaultní název složky pro ukládání programů
#     dirpath - cesta do mateřské složky
#     Changed - identifikátor změny programu



from turtle import width
import naoqi
import webbrowser
import sys
import os
import time
import os.path
from Tkinter import *
import tkMessageBox
from tkSimpleDialog import askstring
from tkFileDialog import askopenfilename
import tkFont
import pickle
import prikazy
import atexit

reload(sys)
sys.setdefaultencoding('utf-8')

filepath=None
connected=False
dir="Soubory"
Changed=0
dirpath=os.path.dirname(__file__)

#Založení složky pro uložené soubory
try:
    if os.path.exists(dir):
        print("Složka \"soubory\" již existuje")
    else:
        os.mkdir(dir)
        
except Exception as e:
    print("chyba",e)


class Objekt:
    def __init__(self, id, typ, parametr=None):
        self.id=id
        self.typ=typ        
        self.parametr=parametr
        # 
        #  Typ: 1- vstan
        #       2- sedni
        #       3- ....
        #

# Po ukončení programu
def exit_handler(): # Odstrani prazdne soubory + check jestli nenastala změna -> případný save // nefunguje protože je dřív metoda save odstraněna
    global dirpath, filepath, Changed, tlacitka, dir
    if Changed==1:
        x=tkMessageBox.askquestion("Uložit?", "Chcete uložit změny?")
        if x:
            if len(tlacitka)<2:
                return
            if filepath != None:
                with open(filepath, 'wb') as outp:
                    pickle.dump(tlacitka,outp)
                        
                f=open(filepath,"r")
                print(f.read())
        
            else:
                direpath=dirpath
                direpath=os.path.join(direpath, dir)
                k=True
                while k:
                    filename=askstring("Nový soubor","Zadejte název nového souboru: ")
                    direcpath=os.path.join(direpath,filename)
                    direcpath=direcpath+".en"
                    print (direcpath)
                    if os.path.exists(direcpath):
                        x=tkMessageBox.askquestion("Přepsat", "Zadaný soubor již existuje, přepsat?")
                        if x:
                            break       
                    else:
                        k=False
                
                f = open(direcpath, "w")
                f.close()
                filepath=direcpath
                with open(filepath, 'wb') as outp:
                    pickle.dump(tlacitka,outp)
    # Smazání prázdných souborů           
    arr = os.listdir("Soubory")
    dirp=dirpath
    for i in arr:
        d=os.path.join(dirp,dir)
        i=os.path.join(d,i)
        if (os.stat(i).st_size == 0):
            print("XXX",i)
            try:
                os.remove(i)
            except Exception as e:
                print("chyba",e)
                
def callback():
    webbrowser.open_new("https://github.com/DStrobl97")
    
def about():
    okno=Toplevel(root, bg="white")
    okno.title("O aplikaci")
    okno.geometry("450x250")
    
    obr = PhotoImage(file="gplv3.gif")
    text= Label(okno,bg="white", image=obr)
    text.image=obr

    text0 = Label(okno, bg="white", text="Editor_NAO_V2.3")
    text1 = Label(okno, bg="white", text="Creator: Daniel Štrobl")
    text2 = Label(okno, bg="white", fg="blue", text="https://github.com/DStrobl97")
    text2.bind("<Button-1>", lambda e: callback())
    text3 = Label(okno, bg="white", text="Copyright © 2022")
    text4 = Label(okno, bg="white", text="Under GNU GPL v3 license")
    
    but0 =Button(okno, bg="#f7a654", width=5,height=2, text="Zpět",  command=lambda: okno.destroy())
    text0.pack()
    text1.pack()
    text2.pack()
    text3.pack()
    text4.pack()
    text.pack()
    but0.pack(pady=10)
# Vytvoření nového objektu
def create(typ,parametr=None):
        
    tlacitka[0]=tlacitka[0]+1
    id=tlacitka[0]
    tlacitka.append(Objekt(id,typ,parametr))
    print("Created: ", id)
    
    k=len(tlacitka)-1
    # print tlacitka[0]
    place(k)
    
# Umístění nového objektu včetně názvu, parametru do seznamu objektů a bindování jednotlivých entit k popup oknu
def place(k):
    uniq=k
    popisek = tlacitka[uniq].typ
    popisek=str(seznamfci(popisek))
    if tlacitka[uniq].parametr!=None:
        parmtr=tlacitka[uniq].parametr
        if tlacitka[uniq].typ==5:
            parmtr=parmtr.rsplit('/', 1)[-1]
        popisek=popisek.replace("%/%",parmtr)
    id=int(tlacitka[uniq].id)
    print ("ukladam ", popisek, id)
    b = Label(frame, text = popisek, font=('Georgia 8'), bg="white", borderwidth=2, relief="groove", padx=5,pady=5)
    b.bind("<Button-1>", lambda event: do_popup(event, id))
    seznam_objektu.append(b)
    update()

# Vykreslení objektů v seznamu objektů
def update():
    global Changed 
    Changed = 1
    list = frame.slaves()
    print(list)
    for widg in list:
        widg.forget()
    
    for i in seznam_objektu:
        i.pack(side=TOP, anchor=NW, expand=TRUE)
    print (seznam_objektu)
    

# Pomocná fce pro výpis
# def tisk(k):
#     print (k)

# Definování vyskakovacího okna    
def do_popup(event, id):
    m=Menu(root)
    # m.add_command(label= "info", command=lambda: tisk(id)) -- výpis id objektu
    m.add_command(label ="Přesunout výše" ,command= lambda: up(id))
    m.add_command(label ="Přesunout níže",command= lambda: down(id))
    m.add_command(label ="Upravit parametr",command= lambda: parametr(id))
    m.add_separator()
    m.add_command(label ="Odstranit",command= lambda: delete(id))
    for i in range(1, tlacitka[0]+1):
        print (i)
        # print (i, identita)
        # print (tlacitka[i].id)
        if int(tlacitka[i].id)==int(id):
            pozice=i
            break
    try:
        print(pozice)
    except:
        pozice=1
    typ=tlacitka[pozice].typ
    if typ<5:
        m.entryconfig("Upravit parametr", state="disabled")
    elif typ==5:
        m.entryconfig("Upravit parametr", label="Upravit cestu", command=lambda: upravcestu(id))
        
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
 
# Změna parametru skrze vyskakovací okno       
def parametr(identita):
    print("provadim zmenu parametru", identita, tlacitka[0])
    try:
        for i in range(1, tlacitka[0]+1):
            print (i)
            # print (i, identita)
            # print (tlacitka[i].id)
            if int(tlacitka[i].id)==int(identita):
                print(tlacitka[i].parametr)
                pozice=i
                break
    except:
        print("Daný prvek nemá parametr.\n")
    x=askstring("Nový parametr ","Zadejte nový parametr: ")
    tlacitka[pozice].parametr=x
    typ=tlacitka[pozice].typ
    txt=seznamfci(typ).replace("%/%", x)
    seznam_objektu[pozice-1].configure(text=txt)
    update()

# Změna pozice skrze vyskakovací okno      
def up(identita):
    print("provadim UP",identita, tlacitka[0])        
    for i in range(1, tlacitka[0]+1):
        print (i)
        # print (i, identita)
        # print (tlacitka[i].id)
        if int(tlacitka[i].id)==int(identita):
            pozice=i
            break
    try:
        if pozice >1:
            print(pozice,pozice-1)
            tlacitka[pozice],tlacitka[pozice-1] = tlacitka[pozice-1],tlacitka[pozice]
            pozice=pozice-1
            seznam_objektu[pozice],seznam_objektu[pozice-1] =seznam_objektu[pozice-1],seznam_objektu[pozice]
            # print("prvni: ", puvodni)
            # print("druha: ", predchozi)
            
            # print("prvni: ",puvodni )
            # print("druha: ",predchozi )
        
    except:
        pass
    update()

# Změna pozice skrze vyskakovací okno          
def down(identita):
    print("provadim Down",identita, tlacitka[0])  
    print (len(tlacitka)-1)      
    for i in range(1, tlacitka[0]+1):
        print (i)
        # print (i, identita)
        # print (tlacitka[i].id)
        if int(tlacitka[i].id)==int(identita):
            pozice=i
            break
    if pozice !=(len (tlacitka)-1):
        print(pozice,pozice+1)
        tlacitka[pozice],tlacitka[pozice+1] = tlacitka[pozice+1],tlacitka[pozice]
        pozice=pozice-1
        seznam_objektu[pozice],seznam_objektu[pozice+1] =seznam_objektu[pozice+1],seznam_objektu[pozice]
        # print("prvni: ", puvodni)
        # print("druha: ", predchozi)
        
        # print("prvni: ",puvodni )
        # print("druha: ",predchozi )
        
    else:
        pass
    update()
    
# Odstranění objektu skrze vyskakovací okno      
def delete(identita):
    pozice=0
    print("provadim DELETE",identita, tlacitka[0])  
    for i in range(1, tlacitka[0]+1):
        print(i, tlacitka[i].id) 
        # print (i, identita)
        # print (tlacitka[i].id)
        if int(tlacitka[i].id)==int(identita):
            pozice=i
            break
    print("Tohle se odstrani v prvnim seznamu: ", pozice)
    tlacitka.pop(pozice)
    print("starej seznam id")
    for k in range(1,len(tlacitka)):
        print (tlacitka[k].id)
    print (seznam_objektu)
    print("Tohle se odstrani v druhem seznamu: ", pozice-1)
    seznam_objektu.pop(pozice-1)
    print (seznam_objektu)
    
    update()
    # reindex() -- nefunkcni kvuli bind 
        
    

# def reindex():
#     tlacitka[0]= len(tlacitka)-1
#     for i in range(1,len(tlacitka)):
#         tlacitka[i].id=i
#         print (tlacitka[i].id)
    
# Testovací funkce k tlacitku   
# def pa():
#     for i in range(1,len(tlacitka)):
#         k=tlacitka[i]
#         print (k.id,k.typ, k.parametr)
#     print (seznam_objektu)
#     # print ID_generator
#     #print (len(tlacitka))
#     # print tlacitka[0].id

#toto je seznam obsahujici informace nesene tlacitky (jde o ID tlacitka)
def seznamfci(typ):
    typ=int(typ)
    seznam={
        1:"Sedni si",
        2:"Vstaň",
        3:"Lehni si na záda",
        4:"Lehni si na břicho",
        5:"Přečti ze souboru %/%",
        6:"Řekni: %/%",
        7:"Jdi dopředu o %/% cm",
        8:"Otoč se vlevo o %/% °",
        9:"Otoč se vpravo o %/% °",
        10:"Počkej %/% s"
    }
    return seznam.get(typ,"Error")

# Fce k získání číselného parametru        
def ziskejparametrc(typ):
    k=askstring("Parametr ","Zadejte parametr: ")
    if k.isdigit():
        print(k, type(k))
        create(typ,k)
    else:
        tkMessageBox.showerror("Zadán nesprávný vstup","Zadán nesprávný vstup")

# Fce k získání textového parametru  
def ziskejparametrt(typ):
    x=askstring("Parametr ","Zadejte parametr: ")
    create(typ,x)

# Fce k získání cesty k souboru jako parametr
def ziskejcestu():
    cesta=askopenfilename(title="Vyberte soubor")
    if os.path.exists(cesta):
        create(5, cesta)

# Fce k změně cesty k souboru jako parametr       
def upravcestu(identita):
    try:
        for i in range(1, tlacitka[0]+1):
            print (i)
            # print (i, identita)
            # print (tlacitka[i].id)
            if int(tlacitka[i].id)==int(identita):
                print(tlacitka[i].parametr)
                pozice=i
                break
    except:
        print("Daný prvek nemá parametr.\n")
    x=askopenfilename(title="Vyberte soubor: ")
    if os.path.exists(x):
        tlacitka[pozice].parametr=x
    x=x.rsplit('/', 1)[-1]
    typ=tlacitka[pozice].typ
    txt=seznamfci(typ).replace("%/%", x)
    
    seznam_objektu[pozice-1].configure(text=txt)
    update()
    
# Smazání obou seznamů
def clearmemory():
    global tlacitka,seznam_objektu
    tlacitka=[0]
    seznam_objektu=[]
    update()
    
def newfile():
    # Tady bude vytvoření nového souboru, předtím se ale musí ověřit změna souboru/ jestli je zde nějaká úprava
    # posléze nabídka k uložení předchozího projektu.
    global filepath,Changed
    if Changed==1:
        x=tkMessageBox.askquestion("Uložit soubor?", "Chcete původní soubor uložit? " )
        if x:
            savefile()
    createnewfile()
    
def createnewfile():
    global filepath, Changed
    clearmemory()
    
    dirpath=os.path.dirname(__file__)
    filename=askstring("Nový soubor","Zadejte název nového souboru: ")
    dirpath=os.path.join(dirpath, dir)
    dirpath=os.path.join(dirpath,filename)
    dirpath=dirpath+".en"
    print (dirpath)
    if os.path.exists(dirpath):
        tkMessageBox.showerror("Chyba", "Zadaný soubor již existuje")
        return
    
    f = open(dirpath, "w")
    f.close()
    nazev="Program  "
    nazev=str(nazev+filename) +".en "
    programlabel.configure(text=nazev)
    filepath=dirpath
    Changed=0
    
    
    
# Načítání souboru
def loadfile():
    global tlacitka, filepath, Changed, dir
    
    try:
        if len(tlacitka)>2 and Changed==1:
            t=tkMessageBox.askyesno("Uložit?","Chcete původní soubor uložit?")
            print(t)
            if t:
                savefile()
        load=askopenfilename(title="Vyberte soubor",initialdir=dir)
        if len(load)>0:
            filepath=load
        else:
            tkMessageBox.showinfo("Soubor nenahrán","Soubor nenahrán")
            return
    except:
        tkMessageBox.showinfo("Soubor nenahrán","Soubor nenahrán")
        return
    # with open(load) as f:
    #     lines = f.read() ##Assume the sample file has 3 lines
    #     inp = f.readlines()[2:]
    # print("Cely soubor:  ",lines)
    # count=lines.split('\n', 1)[0]
    # print ("dsdadsad",count)
    # tlacitka[0]=lines.split('\n', 1)[1]
    clearmemory()
    with open(load, 'rb') as inpt:
        tlacitka=pickle.load(inpt)
    tlacitka=list(tlacitka)
    print (tlacitka)
    for i in range(1,len(tlacitka)):
        print(i)
        print (tlacitka[i].typ)
        place(i)
    nazev="Program  "
    load=load.rsplit('/', 1)[-1]
    nazev=str(nazev+load)
    programlabel.configure(text=nazev)
    Changed=0
    
# Uložení souboru
def savefile():
    global Changed, filepath, tlacitka
    if filepath != None:
        with open(filepath, 'wb') as outp:
            pickle.dump(tlacitka,outp)
                
        f=open(filepath,"r")
        print(f.read())
        
    else:
        createnewfile()
        savefile()
    
    Changed=0

# Uložení souboru jako    
def savefileas():
    global filepath
    oldfile=filepath
    dirpath=os.path.dirname(__file__)
    newfile=askstring("Nový soubor","Zadejte název nového souboru: ")
    dirpath=os.path.join(dirpath, dir)
    dirpath=os.path.join(dirpath,newfile)
    dirpath=dirpath+".en"
    print (dirpath)
    if os.path.exists(dirpath):
        tkMessageBox.showerror("Chyba", "Zadaný soubor již existuje")
        return
    f = open(dirpath, "w")
    f.close()
    filepath=dirpath
    savefile()
    filepath=oldfile
    
# Pomocná fce k scrollovací nabídce
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    x=list(canvas.bbox(ALL))
    x[0]=0
    x[1]=25
    print(x)
    canvas.configure(scrollregion=x)
    
    
# Připojení k Nao
def connect():
        ip=ipentry.get()
        port=portentry.get()
        k= bool(prikazy.test(ip,port))
        if k:
            tkMessageBox.showinfo("Všechno v pořádku","Jsem připojený: " + ip +":" + port)
            connected=True
            disconnectbutton["state"]="normal"
            runbutton["state"]="normal"
            ipentry["state"]="readonly"
        else:
            tkMessageBox.showerror("Chyba","Nedokázal jsem navázat spojení s " + ip +":" + port)
def disconnect():
    tkMessageBox.showinfo("","Odpojeno ")
    disconnectbutton["state"]="disabled"
    runbutton["state"]="disabled"
    ipentry["state"]="normal"
    
def run():
    global filepath,Changed, tlacitka
    if filepath==None:
        k=tkMessageBox.askquestion("", "Není vybrán žádný program, chcete vytvořit nový?")
        if k:
            newfile()
            savefile()
        else:
            return
    elif Changed==1:
        x=tkMessageBox.askquestion("","Chcete program uložit a spustit?")
        if x:
            savefile()
        else:
            return
    
    for i in range(1,len(tlacitka)):
        a=tlacitka[i].typ
        b=tlacitka[i].parametr
        runcommand(a,b)

def runcommand(typ,parametr):
    ip=ipentry.get()
    port=portentry.get()
    if typ==1:
        er=prikazy.pozice(ip,port,"Sit")
    elif typ==2:
        er=prikazy.pozice(ip,port,"Stand")
    elif typ==3:
        er=prikazy.pozice(ip,port,"LyingBack")
    elif typ==4:
        er=prikazy.pozice(ip,port,"LyingBelly")
    elif typ==5:
        with open(parametr, 'r') as file:
            data = file.read().replace('\n','')
            er=prikazy.cti(ip,port,data)

    elif typ==6:
        er=prikazy.mluv(ip,port,parametr)
    elif typ==7:
        er=prikazy.jdi(ip,port,parametr)
    elif typ==8:
        er=prikazy.otoc(ip,port,parametr)
    elif typ==9:
        parametr=parametr*-1
        er=prikazy.otoc(ip,port,parametr)
    else: 
        parametr=float(parametr)
        time.sleep(parametr)
    if er>0:
        tkMessageBox.showerror("Chyba", "Při zpracování robotem nastala neočekávaná chyba.")
        disconnect()
      
    
    
        

    
tlacitka = []
tlacitka.append(0)
seznam_objektu=[]

root = Tk()
root.geometry("600x400")
ipport=Frame(root)
ipport.grid(row=0, column=0, columnspan=4)

textlabel=Label(ipport,text="Připojení: ",font=('Georgia 14 bold'))
iplabel=Label(ipport,text="IP: ")
ipentry=Entry(ipport,width=14)
ipentry.insert(0,"192.168.32.100")
portlabel=Label(ipport,text="Port: ")
portentry=Entry(ipport,width=5)
portentry.insert(0,"9559")
portentry["state"]="readonly"
connectbutton=Button(ipport,text="Připojit se", command=connect)
disconnectbutton=Button(ipport,text="Odpojit se", command=disconnect)
disconnectbutton["state"]="disabled"
runbutton=Button(ipport,text="Spustit Program", command=run, state="disabled")

textlabel.grid(row=0,columnspan=5, pady=5)
iplabel.grid(row=1, rowspan=2,column=0)
ipentry.grid(row=1, rowspan=2, column=1, padx=8)
portlabel.grid(row=1, rowspan=2, column=2)
portentry.grid(row=1, rowspan=2, column=3)
connectbutton.grid(row=1, column=4, padx=20)
disconnectbutton.grid(row=2, column=4, padx=20)
runbutton.grid(row=1, rowspan=2, column=5, padx=20)

okno_prikazu= Frame(root)
okno_prikazu.grid(row=1,column=0,padx=30, pady=10, sticky="nsew")

mainframe = Frame(root)
mainframe.grid(row=1, column=1,sticky="nsew", padx=5, pady=10)
programlabel=Label(mainframe, text="Program: ", font=('Georgia 14 bold'))
programlabel.pack(side=TOP, anchor=NW)

mycanvas=Canvas(mainframe)
my_scrollbar = Scrollbar(mainframe, orient=VERTICAL, command=mycanvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)


mycanvas.pack(side=LEFT,fill=BOTH, expand=1,)




# mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion = mycanvas.bbox(ALL)))
mycanvas.configure(yscrollcommand=my_scrollbar.set)

frame=Frame(mycanvas)
mycanvas.create_window((10,25), window=frame, anchor="nw", width=450)
frame.bind("<Configure>", lambda event, canvas=mycanvas: onFrameConfigure(mycanvas))

root.grid_rowconfigure(1,weight=2)
root.grid_columnconfigure(1,weight=1)

mainmenu=Menu(root)
filemenu=Menu(mainmenu,tearoff=0)
filemenu.add_command(label="Nový ", command=newfile)
filemenu.add_command(label="Načíst", command=loadfile)
filemenu.add_command(label="Uložit", command=savefile)
filemenu.add_command(label="Uložit jako", command=savefileas)

aboutm=Menu(mainmenu,tearoff=0)
aboutm.add_command(label="O aplikaci", command=about)
mainmenu.add_cascade(label="Soubor",menu=filemenu)
mainmenu.add_cascade(label="O aplikaci",menu=aboutm)


prikaz0=Button(okno_prikazu, text="Sedni si ", width=15, height=2, command=lambda: create(1))
prikaz1=Button(okno_prikazu, text="Vstaň", width=15, height=2,command=lambda: create(2))
prikaz2=Button(okno_prikazu, text="Lehni si na záda", width=15, height=2, command=lambda: create(3))
prikaz3=Button(okno_prikazu, text="Lehni si na břicho", width=15, height=2, command=lambda: create(4))
prikaz4=Button(okno_prikazu, text="Přečti ze souboru", width=15, height=2,command=ziskejcestu)
prikaz5=Button(okno_prikazu, text="Řekni ...", width=15, height=2, command=lambda: ziskejparametrt(6))
prikaz6=Button(okno_prikazu, text="Jdi dopředu o ... cm", width=15, height=2, command=lambda: ziskejparametrc(7))
prikaz7=Button(okno_prikazu, text="Otoč se vlevo o ... °", width=15, height=2, command=lambda: ziskejparametrc(8))
prikaz8=Button(okno_prikazu, text="Otoč se vpravo o ... °", width=15, height=2, command=lambda: ziskejparametrc(9))
prikaz9=Button(okno_prikazu, text="Počkej ... s ", width=15, height=2, command=lambda: ziskejparametrc(10))
text_prikazy=Label(okno_prikazu, text="Seznam příkazů:",font=('Georgia 14 bold'))

# druhy=Button(root, text="vykresli", command=pa )
# druhy.pack()
text_prikazy.grid(row=0, columnspan=2,pady=2)
prikaz0.grid(row=1, column=0,pady=2, padx=5)
prikaz1.grid(row=1, column=1,pady=2, padx=5)
prikaz2.grid(row=2, column=0,pady=2, padx=5)
prikaz3.grid(row=2, column=1,pady=2, padx=5)
prikaz4.grid(row=3, column=0,pady=2, padx=5)
prikaz5.grid(row=3, column=1,pady=2, padx=5)
prikaz6.grid(row=4, column=0,pady=2, padx=5)
prikaz7.grid(row=4, column=1,pady=2, padx=5)
prikaz8.grid(row=5, column=0,pady=2, padx=5)
prikaz9.grid(row=5, column=1,pady=2, padx=5)


atexit.register(exit_handler)
root.config(menu=mainmenu)
root.mainloop()
