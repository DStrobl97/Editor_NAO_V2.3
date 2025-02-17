# -*- coding: utf-8 -*-
from Tkinter import *
from naoqi import *
import prikazy
import sys,os
import re
#import os.path
from os import path
import tkMessageBox
import Tkinter, ScrolledText
import tkFileDialog
import subprocess
import time

odeslal=0
pripojeni=1
jmenoprogramu = ""
filepath=""

def combine_funcs(*funcs):
       def combined_func(*args, **kwargs):
           for f in funcs:
               f(*args, **kwargs)
       return combined_func
      
def prikaz():
    def config():
        if os.path.exists("config.ini"):
            k=open("config.ini",'r')
            for line in k:
                k=line.split()
                line="".join(k)
                if "IP=" in line:
                    t= line.split('=')
                    ipentry.insert(0,t[1])
                if "Port=" in line:
                    t= line.split('=')
                    portentry.insert(0,t[1])
                    portentry["state"]="readonly"
        else:
            k=open("config.ini",'w')
            k.write("IP=192.168.32.100\n")
            k.write("Port=9559")
            k.close()
            config()
    def Toeditor():
        k=open("config.ini",'w')
        k.write("IP="+ipentry.get()+"\n")
        k.write("Port="+portentry.get())
        k.close()
        root_R.destroy()
        editor()
        
    def about():
        okno=Toplevel(root_R, bg="white")
        okno.title("O aplikaci")
        okno.geometry("450x200")
        obr = PhotoImage(file="logo_color.gif")
        text= Label(okno,bg="white", image=obr)
        text.image=obr
        text0 = Label(okno, bg="white", text="Aplikace byla vytvořena jako bakalářská práce na katedře informatiky PF JCU.")
        text1 = Label(okno, bg="white", text="Aplikaci vytvořil: Daniel Štrobl")
        text2 = Label(okno, bg="white", text="Vedoucí práce: Mgr. Václav Šimandl, Ph.D.")
        but0 =Button(okno, bg="#f7a654", text="Zpět", width=10,height=4,  command=lambda: okno.destroy())
        text.pack()
        text0.pack()
        text1.pack()
        text2.pack()
        but0.pack(pady=10)
        
    def add(cislo):
        vysledek=100
        ip=ipentry.get()
        port=portentry.get()
        
           
        if cislo==0:
            vysledek=prikazy.pozice(ip,port,"Sit")        
            
        elif cislo==1:
            vysledek=prikazy.pozice(ip,port,"Stand")        

        elif cislo==2:
            vysledek=prikazy.pozice(ip,port,"LyingBack")
         
        elif cislo==3:
            vysledek=prikazy.pozice(ip,port,"LyingBelly")
            
        elif cislo==4:    
            getparametr(ip,port,0)
            
        elif cislo==5:
            lokace = tkFileDialog.askopenfilename()
            if lokace=="":
                return
            lokace=lokace.strip("\n")
            lokace=lokace.replace("/","//")
            with open(lokace, 'r') as file:
                data = file.read().replace('\n', '')
            print(data)
            sendto(ip,port,1,data)
            
        elif cislo==6:
            getparametr(ip,port,2)
        
        elif cislo==7:
            getparametr(ip,port,3)
            
        elif cislo==8:
            getparametr(ip,port,4)
        if vysledek!=100:
               stav(vysledek)
            
    def sendto(ip,port,cislo,parametr):
           if  parametr!="":
               try:
                      float(parametr)
                      if cislo >2:
                             k=int(parametr)
                             if k == abs(k):
                                    if cislo==3:
                                           vysledek=prikazy.otoc(ip,port,parametr)
                                    else:
                                           parametr=float(parametr) * -1
                                           vysledek=prikazy.otoc(ip,port,parametr)
                             else:
                                    tkMessageBox.showinfo("Varování", "Zadána nesprávná hodnota")
                      elif cislo==2:
                             vysledek=prikazy.jdi(ip,port,parametr)               
               except ValueError:
                      if cislo==0:
                             vysledek=prikazy.mluv(ip,port,parametr)
                      elif cislo==1:
                             vysledek=prikazy.cti(ip,port,parametr)

           else:
               tkMessageBox.showinfo("Varování", "Nezadána žádná hodnota")
           stav(vysledek)

    def stav(x):
        #odpojit diisable tlacitka
        global pripojeni
        pripojeni=x
        if x==0:
            button0["state"]="normal"
            button1["state"]="normal"
            button2["state"]="normal"
            button3["state"]="normal"
            button4["state"]="normal"
            button5["state"]="normal"
            button6["state"]="normal"
            button7["state"]="normal"
            button8["state"]="normal"
            ipentry["state"]="readonly"
            test_connect.grid_forget()
            test_disconnect.grid( row=0,column=4)
            k=open("config.ini",'w')
            k.write("IP="+ipentry.get()+"\n")
            k.write("Port="+portentry.get())
            k.close()
        else:
            
            button0["state"]="disabled"
            button1["state"]="disabled"
            button2["state"]="disabled"
            button3["state"]="disabled"
            button4["state"]="disabled"
            button5["state"]="disabled"
            button6["state"]="disabled"
            button7["state"]="disabled"
            button8["state"]="disabled"
            ipentry["state"]="normal"
            test_connect.grid( row=0,column=4)
            test_disconnect.grid_forget()
           
    def testing_connection():
        global pripojeni
        ip=ipentry.get()
        port=portentry.get()
        k= bool(prikazy.test(ip,port))
        if k:
            tkMessageBox.showinfo("Všechno v pořádku","Jsem připojený: " + ip +":" + port)
            stav(0)
        else:
            tkMessageBox.showerror("Chyba","Nedokázal jsem navázat spojení s " + ip +":" + port)
            stav(1)
            
    def getparametr(ip,port,cislo):
        w= Toplevel(root_R)
        wlabel= Label(w, text="Zadejte parametr: ")
        wentry= Entry(w)
        wbutton= Button(w, text="Ok",bg="green", command= combine_funcs(lambda: sendto(ip,port,cislo, wentry.get().encode('utf-8')), lambda: w.destroy()))
        wlabel.pack()
        wentry.pack()
        wentry.focus_set()
        wbutton.pack()


    root_R = Tkinter.Tk()
    root_R.title("Přímé příkazy")
    root_R.minsize(400,200)
    menu = Menu(root_R)
    root_R.config(menu=menu)

    connectmen=Menu(menu)
    menu.add_command(label='Otevřít editor', command=Toeditor)
    menu.add_command(label='O aplikaci', command=about)

    top=Frame(root_R)
    iplabel=Label(top,text='ip: ')
    ipentry=Entry(top)
    #ipentry.insert(0,"192.168.32.100")

    portlabel=Label(top, text='port: ')
    portentry=Entry(top, text="")
    #portentry.insert(0,"9559")
    #portentry[ "state"]="readonly"
    config()
    test_connect=Button(top, text='připojit', command=testing_connection)
    test_disconnect=Button(top, text='odpojit', command=lambda: stav(1))
    
    button0 = Button(root_R, text="Sedni si", width=20, height=2, bg="#f7a654", command= lambda: add(0))
    button1 = Button(root_R, text="Stoupni si", width=20, height=2, bg="#f7a654", command=lambda: add(1))
    button2 = Button(root_R, text="Lehni si na záda", width=20, height=2, bg="#f7a654", command=lambda: add(2))
    button3 = Button(root_R, text="Lehni si na břicho", width=20, height=2,  bg="#f7a654", command=lambda: add(3))
    button4 = Button(root_R, text="Řekni ...", width=20, height=2, bg="#f7a654", command=lambda: add(4))
    button5 = Button(root_R, text="Přečti ze souboru: ", width=20, height=2, bg="#f7a654", command=lambda: add(5))

    button6 = Button(root_R, text="Jdi dopředu o ...", width=20, height=2, bg="#f7a654", command=lambda: add(6))
    button7 = Button(root_R, text="Otoč se vlevo o ...", width=20, height=2, bg="#f7a654", command=lambda: add(7))
    button8 = Button(root_R, text="Otoč se vpravo o ...", width=20, height=2, bg="#f7a654", command=lambda: add(8))
    button9 = Button(root_R, text="Počkej ... s", width=20, height=2, bg="#f7a654", command=lambda: add(9), state=DISABLED)

    top.grid(row=0,columnspan=6)
    iplabel.grid( row=0,column=0)
    ipentry.grid( row=0,column=1)
    portlabel.grid( row=0,column=2)
    portentry.grid( row=0,column=3)
    test_connect.grid( row=0,column=4)
    test_disconnect.grid( row=0,column=4)
    
    
    button0.grid(row=1, column=0)
    button1.grid(row=1, column=2)
    button2.grid(row=1, column=4)
    button3.grid(row=1, column=6)
    
    button4.grid(row=3, column=0)
    button5.grid(row=3, column=2)
    button6.grid(row=3, column=4)
    button7.grid(row=3, column=6)
    
    button8.grid(row=5, column=2)
    button9.grid(row=5, column=4)

    col_count, row_count = root_R.grid_size()
    for row in xrange(row_count):
        root_R.grid_rowconfigure(row, minsize=5)
        
    for column in xrange(col_count):
        root_R.grid_columnconfigure(column, minsize=2)
    stav(pripojeni)
    root_R.mainloop()


def editor():
    def config():
        if os.path.exists("config.ini"):
            k=open("config.ini",'r')
            for line in k:
                k=line.split()
                line="".join(k)
                if "IP=" in line:
                    t= line.split('=')
                    ipentry.insert(0,t[1])
                if "Port=" in line:
                    t= line.split('=')
                    portentry.insert(0,t[1])
                    portentry["state"]="readonly"
        else:
            k=open("config.ini",'w')
            k.write("IP=192.168.32.100\n")
            k.write("Port=9559")
            k.close()
            config()
    def newfile():
        w= Toplevel(root)
        wlabel= Label(w, text="Zadejte jmeno: ")
        wentry= Entry(w)
        wbutton= Button(w, text="Ok",bg="green", command= combine_funcs(lambda: create( wentry.get()), lambda: w.destroy()))
        wlabel.pack()
        wentry.pack()
        wentry.focus_set()
        wbutton.pack()
        
    def create(f):
        global filepath
        if path.exists(f +".txt"):
            answer=tkMessageBox.askquestion("Chyba","Soubor už existuje, Chcete ho přepsat?")
            if answer=='yes':
                l1.config(text = f)
                f=f+".txt"
                open(f,"w+")
                l1.config(text = f)
                filepath= os.path.abspath(f)
                l1.config(text = filepath)
                update()
        else:
            f=f+".txt"
            open(f,"w+") 
            filepath= os.path.abspath(f)
            l1.config(text = filepath)
            update()
            #with open(f,"w+") as fil:
              #  fil.write(('TEST'))
    def loadfile():
        global filepath
        try:
              filepath = tkFileDialog.askopenfilename()
              l1.config(text = filepath)
              update()
        except:
              print("")
    def runorder():
        k=open("config.ini",'w')
        k.write("IP="+ipentry.get()+"\n")
        k.write("Port="+portentry.get())
        k.close()
        root.destroy()
        prikaz()
        
    def about():
        okno=Toplevel(root, bg="white")
        okno.title("O aplikaci")
        okno.geometry("450x200")
        obr = PhotoImage(file="logo_color.gif")
        text= Label(okno,bg="white", image=obr)
        text.image=obr
        text0 = Label(okno, bg="white", text="Aplikace byla vytvořena jako bakalářská práce na katedře informatiky PF JCU.")
        text1 = Label(okno, bg="white", text="Aplikaci vytvořil: Daniel Štrobl")
        text2 = Label(okno, bg="white", text="Vedoucí práce: Mgr. Václav Šimandl, Ph.D.")
        but0 =Button(okno, bg="#f7a654", text="Zpět", width=10,height=4, command=lambda: okno.destroy())
        text.pack()
        text0.pack()
        text1.pack()
        text2.pack()
        but0.pack(pady=10)
    def update():
        programvstup.delete("all")
        file1=open(filepath,'r')
        x1=0
        y1=0
        xdistance=120
        ydistance=60
        maxx=600
        maxy=360
        for line in file1:
            if "Cti" in line:
                k=line.replace('#', '')
                x=k.split('/', -1)
                line="Cti z \n" + x[-1]
            else:
                line=line.replace('#', '')
            if x1<maxx:
                x2=x1+xdistance
                y2=y1+ydistance
            else:
                x1=0
                x2=x1+xdistance
                y1=y1+ydistance
                y2=y1+ydistance
            programvstup.create_rectangle(x1,y1,x2,y2,fill="#FFA500")
            programvstup.create_text((x2-60),(y2-30), text=line)
            x1=x2
        file1.close()

    def zpet():
        if filepath=="":
            tkMessageBox.showinfo("Varování", "Prosím nahrajte soubor, nebo vytvořte nový")
            return
        readFile = open(filepath)
        lines = readFile.readlines()
        readFile.close()
        w = open(filepath,'w')
        w.writelines([item for item in lines[:-1]])
        w.close()
        update()
    def  smazat():
        if filepath=="":
            tkMessageBox.showinfo("Varování", "Prosím nahrajte soubor, nebo vytvořte nový")
            return
        MsgBox = tkMessageBox.askquestion ('Smazat','Opravdu chcete všechno smazat?',icon = 'warning')
        if MsgBox=="yes":
                open(filepath,"w")
        update()
            
    def getparametr(typ):
        w= Toplevel(root)
        wlabel= Label(w, text="Zadejte parametr: ")
        wentry= Entry(w)
        wbutton= Button(w, text="Ok",bg="green", command= combine_funcs(lambda: odeslat( wentry.get().encode('utf-8'),typ), lambda: w.destroy()))
        wlabel.pack()
        wentry.pack()
        wentry.focus_set()
        wbutton.pack()
        w.protocol("WM_DELETE_WINDOW", lambda:  combine_funcs(zpet(), w.destroy()))
        
    def odeslat( wentry, typ):
        if  wentry!="":
               try:
                      float(wentry)
                      if typ =="+":
                             k=int(wentry)
                             if k == abs(k):
                                    fil=open(filepath,"a")
                                    fil.write((wentry)+ "\n")
                                    fil.close()
                             else:
                                    tkMessageBox.showinfo("Varování", "Zadána nesprávná hodnota")
                                    zpet()
                      else:
                             fil=open(filepath,"a")
                             fil.write((wentry)+ "\n")
                             fil.close()                             
               except ValueError:
                      if typ =="a":
                             fil=open(filepath,"a")
                             fil.write((wentry)+ "\n")
                             fil.close()
                      else:
                             tkMessageBox.showinfo("Varování", "Zadána nesprávná hodnota")
                             zpet()

        else:
               tkMessageBox.showinfo("Varování", "Nezadána žádná hodnota")
               zpet()
        update()
            

    def add(cislo):
        global filepath
        if filepath=="":
            tkMessageBox.showinfo("Varování", "Prosím nahrajte soubor, nebo vytvořte nový")
        else:
            if cislo==0:
                fil=open(filepath,"a")
                fil.write(('Sedni si')+ "\n")
                fil.close()

            elif cislo==1:
                fil=open(filepath,"a")
                fil.write(('Vstan')+ "\n")
                fil.close()
                
            elif cislo==2:
                fil=open(filepath,"a")
                fil.write(('Lehni na zada')+ "\n")
                fil.close()
                
            elif cislo==3:
                fil=open(filepath,"a")
                fil.write(('Lehni na bricho')+ "\n")
                fil.close()
                
            elif cislo==4:
                fil=open(filepath,"a")
                fil.write('Rekni# ')
                fil.close()
                getparametr("a")
                
            elif cislo==5:
                textpath = tkFileDialog.askopenfilename()
                if textpath!="":
                    fil=open(filepath,"a")
                    fil.write('Cti# ')
                    fil.write(textpath + '\n')
                    fil.close()

                
            elif cislo==6:
                fil=open(filepath,"a")
                fil.write(('Jdi# '))
                fil.close()
                getparametr("0")
            
            elif cislo==7:
                fil=open(filepath,"a")
                fil.write(('Otoc se vlevo# '))
                fil.close()
                getparametr("+")
                

            elif cislo==8:
                fil=open(filepath,"a")
                fil.write(('Otoc se vpravo#  '))
                fil.close()
                getparametr("+")
                 
            elif cislo==9:
                fil=open(filepath,"a")
                fil.write(('Pockej# '))
                fil.close()
                getparametr("+")
            update()
    
    def stav(x):
        #odpojit diisable tlacitka
        global pripojeni
        pripojeni=x
        if x==0:
            bstart["state"]="normal"
            ipentry["state"]="readonly"
            k=open("config.ini",'w')
            k.write("IP="+ipentry.get()+"\n")
            k.write("Port="+portentry.get())
            k.close()
            test_connect.grid_forget()
            test_disconnect.grid( row=0,column=4)            
        else:
            bstart["state"]="disabled"
            ipentry["state"]="normal"
            test_connect.grid( row=0,column=4)
            test_disconnect.grid_forget()
           
    def testing_connection():
        ip=ipentry.get()
        port=portentry.get()
        k= bool(prikazy.test(ip,port))
        if k:
            tkMessageBox.showinfo("Všechno v pořádku","Jsem připojený: " + ip +":" + port)
            stav(0)
        else:
            tkMessageBox.showerror("Chyba","Nedokázal jsem navázat spojení s " + ip +":" + port)
            stav(1)
            
    def start():
        ip=ipentry.get()
        port=portentry.get()
        global filepath
        
        if filepath=="":
            tkMessageBox.showinfo("Varování", "Prosím nahrajte soubor, nebo vytvořte nový")
            return
               #print("Připojení OK")
        f=open(filepath, 'r')
        print f
        for line in f:
                         
             if line.strip('\n') == 'Sedni si':
                  #print('sednu si')
                  prikazy.pozice(ip,port,"Sit")  
             elif line.strip('\n') == 'Vstan':
                  prikazy.pozice(ip,port,"Stand")            
             elif line.strip('\n') == 'Lehni na zada':
                  prikazy.pozice(ip,port,"LyingBack")
             elif line.strip('\n') == 'Lehni na bricho':
                  prikazy.pozice(ip,port,"LyingBelly")
             else:
                  x=line.split('# ', 1)
                  prikaz=x[0]
                  parametr=x[1]
                  if prikaz=='Rekni':
                       prikazy.mluv(ip,port,parametr)
                  elif prikaz=='Cti':
                       lokace=parametr
                       lokace=lokace.strip("\n")
                       #lokace=lokace.replace("/","//")
                       lokace=lokace.encode("utf8")
                       with open(lokace, 'r') as file:
                            data = file.read().replace('\n','')
                            prikazy.cti(ip,port,data)
                           
                  elif prikaz=='Jdi':
                       prikazy.jdi(ip,port,parametr)
                  elif prikaz=='Otoc se vlevo':
                       prikazy.otoc(ip,port,parametr)
                  elif prikaz=='Otoc se vpravo':
                       parametr=float(parametr) * -1
                       prikazy.otoc(ip,port,parametr)
                  else:
                       parametr=float(parametr)
                       time.sleep(parametr)
        
    #Grafické rozraní
    root = Tkinter.Tk()
    root.title("Aplikace ovladani robota NAO")
    root.minsize(400,570)

    #Menu
    menu = Menu(root) 
    root.config(menu=menu)

    filemenu = Menu(menu) 
    menu.add_cascade(label='Soubor', menu=filemenu) 
    filemenu.add_command(label='Nový', command = newfile) 
    filemenu.add_command(label='Otevřít...', command = loadfile) 

    Status=Menu(menu)

    orders = Menu(menu)
    menu.add_command(label="Spustit příkaz", command = runorder)

    helpmenu = Menu(menu) 
    menu.add_command(label='O aplikaci', command = about)

    #top Frame
    middleFrame = Frame (root)

    top=Frame(root)
    iplabel=Label(top,text='ip: ')
    ipentry=Entry(top)

    portlabel=Label(top, text='port: ')
    portentry=Entry(top)
    config()
    button0 = Button(middleFrame, text="Sedni si", width=20, height=2, bg="#f7a654", command= lambda: add(0))
    button1 = Button(middleFrame, text="Vstaň", width=20, height=2, bg="#f7a654", command=lambda: add(1))
    button2 = Button(middleFrame, text="Lehni si na záda", width=20, height=2, bg="#f7a654", command=lambda: add(2))
    button3 = Button(middleFrame, text="Lehni si na břicho", width=20, height=2,  bg="#f7a654", command=lambda: add(3))
    button4 = Button(middleFrame, text="Řekni ...", width=20, height=2, bg="#f7a654", command=lambda: add(4))
    button5 = Button(middleFrame, text="Přečti ze souboru: ", width=20, height=2, bg="#f7a654", command=lambda: add(5))

    button6 = Button(middleFrame, text="Jdi dopředu o ...", width=20, height=2, bg="#f7a654", command=lambda: add(6))
    button7 = Button(middleFrame, text="Otoč se vlevo o ...", width=20, height=2, bg="#f7a654", command=lambda: add(7))
    button8 = Button(middleFrame, text="Otoč se vpravo o ...", width=20, height=2, bg="#f7a654", command=lambda: add(8))
    button9 = Button(middleFrame, text="Počkej ... s", width=20, height=2, bg="#f7a654", command=lambda: add(9))
    
    top.pack()
    iplabel.grid( row=0,column=0)
    ipentry.grid( row=0,column=1)
    portlabel.grid( row=0,column=2)
    portentry.grid( row=0,column=3)
    
    button0.grid(row=1, column=0)
    button1.grid(row=1, column=2)
    button2.grid(row=1, column=4)
    button3.grid(row=1, column=6)

    button4.grid(row=3, column=0)
    button5.grid(row=3, column=2)
    button6.grid(row=3, column=4)
    button7.grid(row=3, column=6)

    button8.grid(row=5, column=2)
    button9.grid(row=5, column=4)

    col_count, row_count = middleFrame.grid_size()
    for row in xrange(row_count):
        middleFrame.grid_rowconfigure(row, minsize=5)
        
    for column in xrange(col_count):
        middleFrame.grid_columnconfigure(column, minsize=2)

    #bottom Frame
    bottomFrame = Frame(root)
    bottomFrame.pack(side=BOTTOM)
    middleFrame.pack(side=BOTTOM)

    l1 = Label(bottomFrame, text = jmenoprogramu, pady=3,padx=10)
    l1.pack()

    programvstup = Canvas(bottomFrame, width=600,height=380, bg="white")


    bstart = Button(bottomFrame, bg="green", fg="black", text="Spustit",width=10,height=3, command=start)
    bnew= Button(bottomFrame, bg="grey", text="Nový",width=10,height=2, command=newfile)
    bload = Button(bottomFrame, bg="grey", text="Nahrát",width=10,height=2, command=loadfile)
    bzpet = Button(bottomFrame, bg="grey", text="Zpět", width=10, height=2,command=zpet)
    bsmazat = Button(bottomFrame, bg="red",fg="black", text="Smazat vše", width=10, height=2,command=smazat)

    test_connect=Button(top, text='připojit', command=testing_connection)
    test_disconnect=Button(top, text='odpojit', command=lambda:stav(1))
    test_connect.grid( row=0, column =4)
    test_disconnect.grid( row=0, column =4)
    
    programvstup.pack(side=RIGHT)
    bstart.pack(side=TOP)
    bnew.pack(side=TOP)
    bload.pack(side=TOP)

    bsmazat.pack(side=BOTTOM)
    bzpet.pack(side=BOTTOM)
    #bottom Frame
    stav(pripojeni)
    root.mainloop() 

editor()
