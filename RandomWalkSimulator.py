#!/usr/bin/python3
from RandomNumberGenerator import Generator
from prettytable import PrettyTable
import tkinter as tk
import math
from itertools import combinations
import numpy
import pylab
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Application(tk.Frame):
    def __init__(self, master=None,width = 60,height =60):
        tk.Frame.__init__(self, master)
        self.width=width
        self.height=height
        self.grid()
        self.Gen = Generator()
        self.positionDepart = (math.floor(width/2),math.floor(height/2))
        self.initWidgets()
        
    
    def Execute(self,WalkType,Gen):
        self.canvas.delete('all')
        if WalkType == "Classique":
            #self.ClassiqueRandomWalk(Gen)
            self.classicRandomWalk(Gen)
        elif WalkType == "Unique":
            self.UniqueRandomWalk(Gen)
        elif WalkType == "Sans retour":
            self.SansRetourRandomWalk(Gen)
        else:
            ValueError("IMPOSSIBLE")
            
        
    def initWidgets(self):
        #Choix du nombre de pas
        self.ChoixPasLabel = tk.Label(self,text="Choisir nombre de pas")
        self.ChoixPasLabel.grid(column=1,row=0,rowspan=1)
        self.ChoixPasSpinBox = tk.Spinbox(self,from_=5,to=100)
        self.ChoixPasSpinBox.grid(column = 1, row = 0, rowspan = 2)
        #Choix de la marche
        self.RandomWalkLabel = tk.Label(self,text="Type de marche aléatoire : ")
        self.RandomWalkLabel.grid(column=1,row=1,rowspan=1)
        OptionList = ["Classique","Sans retour","Unique"]
        variable = tk.StringVar(self)
        variable.set(OptionList[0])
        self.opt = tk.OptionMenu(self,variable,*OptionList)
        self.opt.config(width=12, font=('Helvetica', 12))
        self.opt.grid(column=1,row=1,rowspan=2)
        

        #Modifier valeur Générateur du nombre aléatoire :
        self.ChoixGenerateur = tk.Label(self,text = "Paramètres du générateur :")
        self.ChoixGenerateur.grid(column=1,row=2,rowspan=1)
    
        self.ModulusLabel = tk.Label(self,text="Modulo")
        self.ModulusLabel.grid(column=1,row=2,rowspan=2)
        self.ModulusEntry = tk.Entry(self)
        self.ModulusEntry.insert(0,self.Gen.modulus)
        self.ModulusEntry.grid(column=2, row=2,rowspan = 2)
        
        self.MultiplierLabel = tk.Label(self,text="Multiplier")
        self.MultiplierLabel.grid(column=1,row=2,rowspan=3)
        self.MultiplierEntry = tk.Entry(self)
        self.MultiplierEntry.insert(0,self.Gen.a)
        self.MultiplierEntry.grid(column=2, row=2,rowspan = 3)
        
        self.IncrementLabel = tk.Label(self,text="Increment")
        self.IncrementLabel.grid(column=1,row=2,rowspan=4)
        self.IncrementEntry = tk.Entry(self)
        self.IncrementEntry.insert(0,self.Gen.c)
        self.IncrementEntry.grid(column=2, row=2,rowspan = 4)
        
        self.SeedLabel = tk.Label(self,text="Seed")
        self.SeedLabel.grid(column=1,row=2,rowspan=5)
        self.SeedEntry = tk.Entry(self)
        self.SeedEntry.insert(0,self.Gen.seed)
        self.SeedEntry.grid(column=2, row=2,rowspan = 5)
        
        #Graphique
        self.GraphLabel = tk.Label(self,text="Choisir nb Steps pour le graphique ")
        self.GraphLabel_ = tk.Label(self,text="(Le graphique executera chaque algorithme de 0 jusqu'au nombre de steps)")
        
        self.GraphLabel.grid(column=1,row=4,rowspan=2)
        self.GraphLabel_.grid(column=1,row=4,rowspan=3)
        self.GraphEntry = tk.Entry(self)
        self.GraphEntry.insert(0,"101")
        self.GraphEntry.grid(column=2, row=4,rowspan = 3)
        
        #Boutton executer
        self.ExecuteButton = tk.Button(text = "Executer",command=lambda :self.Execute(variable.get(),Generator(int(self.ModulusEntry.get()),int(self.MultiplierEntry.get()),int(self.IncrementEntry.get()),int(self.SeedEntry.get()))))
        self.ExecuteButton.config(anchor='center')
        self.ExecuteButton.grid(column=1,row=1,rowspan=2)
        #Boutton graphique : 
        self.ExecuteGraph = tk.Button(text = "Voir graphiques",command=self.ShowGraph)
        self.ExecuteGraph.config(anchor='n')
        self.ExecuteGraph.grid(column=0,row=1,rowspan=1)
        #Canvas pour la grille
        self.initCanvas()
    
    def initCanvas(self):
        canvasWidth = self.width *5
        canvasHeight = self.height *5
        self.canvas = tk.Canvas(self,width = canvasWidth, height = canvasHeight)
        self.canvas.grid(column = 0,row =0,rowspan = 8)

    def ClassicForGraph(self, iter):
        Gen = Generator(int(self.ModulusEntry.get()),int(self.MultiplierEntry.get()),int(self.IncrementEntry.get()),int(self.SeedEntry.get()))
        x = numpy.zeros(int(iter))
        y=numpy.zeros(int(iter))
        for i in range(0,int(iter)):
            val = int(Gen.lcg(0,4))
            if val == 0: 
                x[i] = x[i - 1] + 1
                y[i] = y[i - 1] 
            elif val == 1: 
                x[i] = x[i - 1] - 1
                y[i] = y[i - 1] 
            elif val == 2: 
                x[i] = x[i - 1] 
                y[i] = y[i - 1] + 1
            else: 
                x[i] = x[i - 1] 
                y[i] = y[i - 1] - 1 
        
        Cox = float(x[-1] - x[0])**2.
        Coy = float(y[-1] - y[0])**2.
        distance = Cox + Coy
        return distance
    def ReturnForGraph(self, iter):
        Gen = Generator(int(self.ModulusEntry.get()),int(self.MultiplierEntry.get()),int(self.IncrementEntry.get()),int(self.SeedEntry.get()))
        x = numpy.zeros(int(iter))
        y=numpy.zeros(int(iter))
        PasAvant=(0,0)
        Modificate = (0,0)
        for i in range(0,iter):
            while True:
                val = int(Gen.lcg(0,4))
                if val == 0: 
                    Modificate = (1,0)
                    x[i] = x[i - 1] + 1
                    y[i] = y[i - 1] 
                elif val == 1: 
                    Modificate = (-1,0)
                    x[i] = x[i - 1] - 1
                    y[i] = y[i - 1] 
                elif val == 2: 
                    Modificate = (0,1)
                    x[i] = x[i - 1] 
                    y[i] = y[i - 1] + 1
                elif val == 3: 
                    Modificate = (0,-1)
                    x[i] = x[i - 1] 
                    y[i] = y[i - 1] - 1
                if PasAvant[0] + Modificate[0] != 0 or PasAvant[1] + Modificate[1] != 0:
                    PasAvant = Modificate
                    break
        
        Cox = float(x[-1] - x[0])**2.
        Coy = float(y[-1] - y[0])**2.
        distance = Cox + Coy
        return distance
    def UniqueForGraph(self, iter):
        Gen = Generator(int(self.ModulusEntry.get()),int(self.MultiplierEntry.get()),int(self.IncrementEntry.get()),int(self.SeedEntry.get()))
       
        x = numpy.zeros(int(iter))
        y=numpy.zeros(int(iter))
        current_position = [0,0]
        visited_points = current_position
        possible_moves = [self.move(current_position,dx=dx) for dx in range(-1,2) if -int(iter)<=current_position[0] + dx <=int(iter)]+  [self.move(current_position,dy=dy) for dy in range(-1,2) if -int(iter) <= current_position[1]+dy<=int(iter)]
        available_moves = [m for m in possible_moves if m not in visited_points]
        nbSteps = 0
        i=0
        for i in range(0,iter):
            if len(available_moves) != 0 and int(iter) not in current_position and -int(iter) not in current_position:
                current_position = available_moves[Gen.lcg(0,len(available_moves))]
                visited_points.append(current_position)
                x[i] = current_position[0]
                y[i] = current_position[1]
                possible_moves = [self.move(current_position,dx=dx) 
                                for dx in range(-1,2) 
                                if -int(iter)<=current_position[0] + dx <=int(iter)]+  [self.move(current_position,dy=dy) for dy in range(-1,2) 
                                                                                                                                    if -int(iter) <= current_position[1]+dy<=int(iter)]
                available_moves = [m for m in possible_moves if m not in visited_points] 
                i = i+1
                nbSteps = nbSteps +1 
        
        Cox = float(x[-1] - x[0])**2.
        Coy = float(y[-1] - y[0])**2.
        distance = Cox + Coy
        return distance
    
    def create_window(self,Class,Return,Uni):
        window = tk.Toplevel(self)
        window.title("Graphique")
        fig = Figure(figsize = (6,4),dpi=96)
        ax = fig.add_subplot(111)
        
        canvasWidth = self.width *5
        canvasHeight = self.height *5
        self.newcanvas = tk.Canvas(window,width = canvasWidth, height = canvasHeight)
        self.newcanvas.grid(column = 0,row =0,rowspan = 8)
        ax.plot(Class,color='b',label='RANDOM')
        ax.plot(Return,color='r',label='NONREVERSING')
        ax.plot(Uni,color='g',label='SELF_AVOIDING')
        ax.legend(loc="upper right")
        ax.set_title('Graphique')
        ax.set_xlabel('Nombre de Steps')
        ax.set_ylabel('Distance mise bout à bout au carré')
        graph = FigureCanvasTkAgg(fig,master=window)
        self.newcanvas = graph.get_tk_widget()
        self.newcanvas.grid(row=0,column = 0,rowspan = 8)
        
    def ShowGraph(self):
        ClassicList = []
        ReturnList = []
        UniqueList = []
        for i in range(1,int(self.GraphEntry.get())):
            ClassicList.append(self.ClassicForGraph(i))
            ReturnList.append(self.ReturnForGraph(i))
            UniqueList.append(self.UniqueForGraph(i))
        self.create_window(ClassicList,ReturnList,UniqueList )
   
    def classicRandomWalk(self,Gen):
        x = numpy.zeros(int(self.ChoixPasSpinBox.get()))
        y=numpy.zeros(int(self.ChoixPasSpinBox.get()))
        for i in range(0,int(self.ChoixPasSpinBox.get())):
            val = int(Gen.lcg(0,4))
            if val == 0: 
                x[i] = x[i - 1] + 1
                y[i] = y[i - 1] 
            elif val == 1: 
                x[i] = x[i - 1] - 1
                y[i] = y[i - 1] 
            elif val == 2: 
                x[i] = x[i - 1] 
                y[i] = y[i - 1] + 1
            else: 
                x[i] = x[i - 1] 
                y[i] = y[i - 1] - 1
        fig = Figure(figsize = (6,4),dpi=96)
        ax = fig.add_subplot(111)
        ax.plot(x,y)
        graph = FigureCanvasTkAgg(fig,master=self)
        canvas = graph.get_tk_widget()
        canvas.grid(row=0,column = 0,rowspan = 8)
                        
    def SansRetourRandomWalk(self,Gen):
        x = numpy.zeros(int(self.ChoixPasSpinBox.get()))
        y=numpy.zeros(int(self.ChoixPasSpinBox.get()))
        PasAvant=(0,0)
        Modificate = (0,0)
        for i in range(0,int(self.ChoixPasSpinBox.get())):
            while True:
                val = int(Gen.lcg(0,4))
                if val == 0: 
                    Modificate = (1,0)
                    x[i] = x[i - 1] + 1
                    y[i] = y[i - 1] 
                elif val == 1: 
                    Modificate = (-1,0)
                    x[i] = x[i - 1] - 1
                    y[i] = y[i - 1] 
                elif val == 2: 
                    Modificate = (0,1)
                    x[i] = x[i - 1] 
                    y[i] = y[i - 1] + 1
                elif val == 3: 
                    Modificate = (0,-1)
                    x[i] = x[i - 1] 
                    y[i] = y[i - 1] - 1
                if PasAvant[0] + Modificate[0] != 0 or PasAvant[1] + Modificate[1] != 0:
                    PasAvant = Modificate
                    break

        fig = Figure(figsize = (6,4),dpi=96)
        ax = fig.add_subplot(111)
        ax.plot(x,y)     
        graph = FigureCanvasTkAgg(fig,master=self)
        canvas = graph.get_tk_widget()
        canvas.grid(row=0,column = 0,rowspan = 8)

                
    def move(self,pos,dx=0,dy=0):
        return [pos[0] + dx,pos[1]+ dy]
        
    def UniqueRandomWalk(self,Gen):
        x = numpy.zeros(int(self.ChoixPasSpinBox.get()))
        y=numpy.zeros(int(self.ChoixPasSpinBox.get()))
        current_position = [0,0]
        visited_points = current_position
        possible_moves = [self.move(current_position,dx=dx) for dx in range(-1,2) if -int(self.ChoixPasSpinBox.get())<=current_position[0] + dx <=int(self.ChoixPasSpinBox.get())]+  [self.move(current_position,dy=dy) for dy in range(-1,2) if -int(self.ChoixPasSpinBox.get()) <= current_position[1]+dy<=int(self.ChoixPasSpinBox.get())]
        available_moves = [m for m in possible_moves if m not in visited_points]
        nbSteps = 0
        i=0
        for i in range(0,int(self.ChoixPasSpinBox.get())):
            if len(available_moves) != 0 and int(self.ChoixPasSpinBox.get()) not in current_position and -int(self.ChoixPasSpinBox.get()) not in current_position:
                current_position = available_moves[Gen.lcg(0,len(available_moves))]
                visited_points.append(current_position)
                x[i] = current_position[0]
                y[i] = current_position[1]
                possible_moves = [self.move(current_position,dx=dx) 
                                for dx in range(-1,2) 
                                if -int(self.ChoixPasSpinBox.get())<=current_position[0] + dx <=int(self.ChoixPasSpinBox.get())]+  [self.move(current_position,dy=dy) for dy in range(-1,2) 
                                                                                                                                    if -int(self.ChoixPasSpinBox.get()) <= current_position[1]+dy<=int(self.ChoixPasSpinBox.get())]
                available_moves = [m for m in possible_moves if m not in visited_points]
                
                nbSteps = nbSteps +1
            else : 
                break
        fig = Figure(figsize = (6,4),dpi=96)
        ax = fig.add_subplot(111)
        ax.plot(x,y)
        graph = FigureCanvasTkAgg(fig,master=self)
        canvas = graph.get_tk_widget()
        canvas.grid(row=0,column = 0,rowspan = 8)
        
		
app = Application(None,130,130)
app.master.title("Random Walk Simulator")
app.mainloop()

