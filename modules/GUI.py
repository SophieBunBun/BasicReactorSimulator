from tkinter import ttk
from pathlib import PureWindowsPath

import os
import simulation


class inputBox:
    
    def __init__(self, parentFrame, _text, _row, _column):
        
        self.text = ttk.Label(parentFrame, text = _text, justify = "center")
        self.spinbox = ttk.Spinbox(parentFrame, from_ = 0, to = 9999, width = 12)
        self.spinbox.set(1)
        
        self.text.grid(row = _row, column = _column, padx = 5, pady = 5 if _row > 1 else (20, 5))
        self.spinbox.grid(row = _row + 1, column = _column, padx = 5, pady = 5)

    def getInt(self):
        
        return int(self.spinbox.get())
    
    def getFloat(self):
        
        return float(self.spinbox.get())

class GUI:
    
    #Initializing GUI
    def __init__(self):
        
        self.themelessMode = False
        self.rootInit()

        #Finish initializing GUI
        self.root.title("Simulador")
        self.root.geometry("410x400")
        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(width=False, height=False)
        
        #Create GUI interior frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill = "both", expand = 1)
        
        #Setting themes!
        if self.themelessMode == False:
            self.style = ttk.Style()
            self.themeVar = ttk.tkinter.BooleanVar()
        
        #Create all buttons
        self.buildUI()
        
        #Warn user of one drive boogie man if directory is contained in one drive
        if self.themelessMode == False:
            
            self.switchThemes()
              
        else:
            
            ttk.tkinter.messagebox.showwarning(title = "One drive detetado", message = "Está a correr o simulador numa pasta localizada numa diretiva conectada ao One Drive. Isto cria erros com o tcl e, consequentemente, com o carregamento dos pacotes de temas. Se quiser um menu mais bonito, retire a pasta do simulador desta diretiva e ponha-a noutra diretiva não associada ao One Drive. Obrigado.")
        
        #Run app
        self.root.mainloop()
        self.root.update()

    def rootInit(self):
        
        #Initializing Tkinter
        self.root = ttk.tkinter.Tk()

        #Try importing, if it errors, launch with no theme
        try:
            
            #Importing theme .tcl files using tcl evaluation
            #Getting windows path
            path = PureWindowsPath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "themes"))
    
            #Converting \ to /
            pathString = path.as_posix()
            print(pathString)
            
            #Ready packages
            self.root.tk.eval("""
                              set theme_directory %s
                              
                         package ifneeded breeze 0.6 \
                             [list source [file join $theme_directory breeze/breeze.tcl]]
                         package ifneeded breeze-dark 0.1 \
                             [list source [file join $theme_directory breeze-dark/breeze-dark.tcl]]
                                 """ % pathString)
    
            #Import packages
            self.root.tk.call("package", "require", "breeze")
            self.root.tk.call("package", "require", "breeze-dark")
            
        except:
            
            self.themelessMode = True

    def buildUI(self):
        
        #Creates all the buttons for the GUI
        self.widgets = []
        
        Texts = {
            0 : "(Na) Quantidade \n de A inicial",
            1 : "(Nb) Quantidade \n de B inicial",
            2 : "(Nc) Limiar de \n remoção de C",
            3 : "(Ht) Tempo de \n simulação",
            4 : "(Tdg) Modificador do \n tempo entre deslocamentos",
            5 : "(Tr) Modificador do \n tempo entre reações",
            6 : "(Ta) Modificador do \n tempo entre adições",
            7 : "(Ts) Modificador do \n tempo entre extrações",
            8 : "(k) Limite de \n deslocamento",
            9 : "(L) Tamanho \n do reator"
            }

        for i in range(10):
            
            self.widgets.append(inputBox(self.frame, Texts[i], (i // 3) * 2, i % 3 if i < 9 else 1))
        
        #Tcl error "fix"
        if self.themelessMode == False:
            
            self.widgets.append(ttk.Radiobutton(self.frame, text = "Dark theme", variable = self.themeVar, value = True, command = self.switchThemes))
            self.widgets.append(ttk.Radiobutton(self.frame, text = "Light theme", variable = self.themeVar, value = False, command = self.switchThemes))
            
        self.widgets.append(ttk.Button(self.frame, text = "Simular", width = 12, command = self.simulateHandlerEvent))

        for i in range(3 if self.themelessMode == False else 1):
            
            self.widgets[10 + i].grid(column = i + (0 if self.themelessMode == False else 1), row = 9, padx = 5, pady = 10)

    def switchThemes(self):
        
        #This switches the theme based on the bool value defined on the radio buttons
        Themes = {
            True : "breeze-dark",
            False : "breeze"
            }
        
        self.style.theme_use(Themes[self.themeVar.get()])

    def simulateHandlerEvent(self):
        
        #Handle simulation start
        try:
            
            graphData,Data = simulation.simular(
                Na = self.widgets[0].getInt(), Nb = self.widgets[1].getInt(), Nc = self.widgets[2].getInt(), Ht = self.widgets[3].getInt(),
                Tdg = self.widgets[4].getFloat(), Tr = self.widgets[5].getFloat(), Ta = self.widgets[6].getFloat(), Ts = self.widgets[7].getFloat(),
                k = self.widgets[8].getInt(), GUI = True)
            
        #If simulation fails
        except:
            
            ttk.tkinter.messagebox.showerror(title = "Erro de simulador", message = "Um ou mais inputs levam a um crash do simulador, verifique inputs.")
            self.root.update()
            
        else:
            
            InfoBox = ttk.tkinter.Toplevel()
            InfoBox.title("Resultados")
            InfoBox.geometry("250x120")
            
            frame = ttk.Frame(InfoBox)
            frame.pack(side = "top", fill = "both", expand = 1)
            
            infoTexts = []
            
            infoTexts.append(ttk.Label(frame, text = "A Consumido: " + str(Data[0])))
            infoTexts.append(ttk.Label(frame, text = "B Consumido: " + str(Data[1])))
            infoTexts.append(ttk.Label(frame, text = "C Extraido: " + str(Data[2])))
            
            for text in infoTexts:
                
                text.pack(side = "top", padx = 5, pady = 10)
            
            simulation.printGraph(graphData, Dark = self.themeVar.get() if self.themelessMode == False else False)
            
            
gui = GUI()
            
            