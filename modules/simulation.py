#This is where the simulation event are called and get executed
import matplotlib.pyplot as plt #
import cap as cp
import mollist as ml
import events as ev

from random import random
from math import e

def randomxp(m):
    t = random()
    return 1 - e**( - t / m )

#The dark setting enables graph dark mode and the GUI setting should only be set to True when this function is run by the gui module,
#otherwise there will be errors because the code to switch backend rendering is for spyder use only.
def simular(L = 8 , Na = 120 , Nb = 110 , Nc = 30 , Ht = 200 , Tdg = 1, k = 2 , Tr = 3 , Ta = 0.1 , Ts = 1, Dark = True, GUI = False):
    
    if GUI == False:
        
        #Changing backend rendering to qt5 (Interactable graph!! yay!!)
        from IPython import get_ipython
        get_ipython().run_line_magic("matplotlib","qt5")
    
    #Creating a mollist with the starting counts
    objList = ml.molList()
    objList.insert("A", Na)
    objList.insert("B", Nb)
    objList.insert("C", 0)
    
    #Initializing simulation space
    simulation = ev.simulation(objList,L)
    
    #Initializing cap
    cap = cp.cap()
    
    #Add first event
    cap.addEvent(cp.event(0, "Move"))

    #Initializing graph data
    graphData = [[0] , [[Na] ,[Nb] ,[0]], [[Na] ,[Nb] ,[0]], [[0] ,[0] ,[0]]]
    
    
    #Setting bool values
    extracting = False
    inserting = False
    
    while cap.currentEvent().time <= Ht:
        
        if cap.currentEvent().kind == "Move":
            
            simulation.globalMoveEvent(k)
            cap.addEvent(cp.event(cap.currentEvent().time + randomxp(Tr), "Reaction"))
            
        elif cap.currentEvent().kind == "Reaction":
            
            simulation.reactionEvent()
            cap.addEvent(cp.event(cap.currentEvent().time + randomxp(Tdg), "Move"))
            
        elif cap.currentEvent().kind == "Extraction":
            
            simulation.removeEvent('C')
            extracting = False
            
        elif cap.currentEvent().kind == "Insertion":
            
            simulation.insertEvent('A', round(Na/2))
            simulation.insertEvent('B', round(Nb/2)) 
            inserting = False
            
        if not extracting and simulation.totalMolCount.getCount('C') > Nc: 
            
            cap.addEvent(cp.event(cap.currentEvent().time + randomxp(Ts), "Extraction")) 
            extracting = True
            
        if not inserting and simulation.totalMolCount.getCount('A') < (Na / 2) and simulation.totalMolCount.getCount('B') < (Nb / 2):
        
            cap.addEvent(cp.event(cap.currentEvent().time + randomxp(Ts), "Insertion")) 
            inserting = True  
                
        cap.delCurrentEvent()

        #Graph x axis
        graphData[0].append(cap.currentEvent().time)
        
        #Graph y axis for current count in reactor
        graphData[1][0].append(simulation.totalMolCount.getCount('A'))
        graphData[1][1].append(simulation.totalMolCount.getCount('B'))
        graphData[1][2].append(simulation.totalMolCount.getCount('C'))
        
        #Graph y axis for total count inserted
        graphData[2][0].append(simulation.totalMolConsumed.getCount('A'))
        graphData[2][1].append(simulation.totalMolConsumed.getCount('B'))
        graphData[2][2].append(simulation.totalMolConsumed.getCount('C'))
        
        #Graph y axis for total count extracted
        graphData[3][0].append(simulation.totalMolRetrieved.getCount('A'))
        graphData[3][1].append(simulation.totalMolRetrieved.getCount('B'))
        graphData[3][2].append(simulation.totalMolRetrieved.getCount('C'))
        
    #Print outputs
    if GUI == True:
        
        return graphData,[str(graphData[2][0][-1]), str(graphData[2][1][-1]), str(graphData[3][2][-1])]
    
    else:
        
        print("A Consumido: " + str(graphData[2][0][-1])) 
        print("B Consumido: " + str(graphData[2][1][-1]))    
        print("C Obtido: " + str(graphData[3][2][-1]))
        
        printGraph(graphData, Dark)
    
def printGraph (graphData, Dark):
     
    #Tracing graph data
    maxTrace = 0
    
    for i1 in range(3):
        for i2 in range(3):
            
            if max(graphData[i1 + 1][i2]) > maxTrace:
                maxTrace = max(graphData[i1 + 1][i2])
        
    #Plot cosmetics
    if Dark:
        
        primaryColor = "#30353a"
        secondaryColor = "#202225"
        textColor = "white"
        
    else:
        
        primaryColor = "#f1f1f1"
        secondaryColor = "#d2d2d2"
        textColor = "black"
    
    #Set colors
    fig, ax = plt.subplots()
    fig.set_facecolor(primaryColor)
    fig.gca().set_facecolor(secondaryColor)
    ax.tick_params(colors = textColor)
    ax.tick_params(axis = 'x', colors = textColor)
    ax.tick_params(axis = 'y', colors = textColor)
    
    ax.grid(color = "#434C5E")
    
    ax.set_xlabel("Tempo", color = textColor)
    ax.set_ylabel("Quantidade de moléculas", color = textColor)

    #Plot Data
    ax.axis([0, max(graphData[0]), 0, maxTrace + 10])
    
    currentA, = ax.plot(graphData[0], graphData[1][0], color = "#efb48f", linestyle = "-", label = "A no reator", linewidth = 1)
    currentB, = ax.plot(graphData[0], graphData[1][1], color = "#94dceb", linestyle = "-", label = "B no reator", linewidth = 1)
    currentC, = ax.plot(graphData[0], graphData[1][2], color = "#cd79c8", linestyle = "-", label = "C no reator", linewidth = 1)
    
    totalA, = ax.plot(graphData[0], graphData[2][0], color = "#ff6e14", linestyle = "-", label = "A total gasto", linewidth = 1)
    totalB, = ax.plot(graphData[0], graphData[2][1], color = "#00c8f0", linestyle = "-", label = "B total gasto", linewidth = 1)
    totalC, = ax.plot(graphData[0], graphData[3][2], color = "#ff29f1", linestyle = "-", label = "C total extraido", linewidth = 1)
    
    #Initialize legend
    leg = plt.legend(loc = 2, facecolor = primaryColor)
    leg.get_frame().set_color(primaryColor)
    
    for text in leg.get_texts():
        
        text.set_color(textColor)
        
    ##Build interactable graph
    legLines = leg.get_lines()
    
    for legLine in legLines:
        
        legLine.set_picker(True)
        legLine.set_pickradius(5)
        
    graphDictionary = {
        0 : currentA,
        1 : currentB,
        2 : currentC,
        3 : totalA,
        4 : totalB,
        5 : totalC
        }
    
    #Handles the event for clicking on the labels
    def onClickEventHandler(event):
        
        clicked = event.artist
        visibility = clicked.get_visible()
        
        clicked.set_visible(not visibility)
        graphDictionary[legLines.index(clicked)].set_visible(not visibility)
        
        plt.draw()
        
    #Link labels to click event
    fig.canvas.mpl_connect('pick_event', onClickEventHandler)
    
    plt.show()
        

        
        
        