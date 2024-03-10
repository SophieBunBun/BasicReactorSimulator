import matplotlib.pyplot as plt
import cap
import mollist as ml
import events as ev
import event_manip as em
import obsrand

Na=int(input('força, Na: '))
Nb=int(input('nº de B: '))

objList=ml.molList()
objList.insert("A", Na)
objList.insert("B", Nb)
objList.insert("C", 0)


def simular(L,objList,Nc,Ht,Tdg,k,Tr,Ta,Ts):
    simulacao=ev.simulation(objList,L)
    
    c=cap.newc()
    ce=em.evt(0,'mov')
    ct=em.time(ce)
    ck=em.kind(ce)
    xtrace=[0]
    yAtrace=[Na]
    yBtrace=[Nb]
    yCtrace=[0]
    
    while ct<=Ht:
        
        if ck=='mov':
            
            simulacao.globalMoveEvent(k)
            
            #c=cap.addE(c,em.evt(ct+obsrand.exprandom(Tdg),'mov'))
            c=cap.addE(c,em.evt(ct+obsrand.exprandom(Tr),'reac'))
            
            
        elif ck=='reac':
            
            simulacao.reactionEvent()
            c=cap.addE(c,em.evt(ct+obsrand.exprandom(Tdg),'mov'))
            
        #if ck=='extr':
            
            #print("extracting")
         #   simulacao.removeEvent('C', -1)
            
        #if ck == 'adic':
            
        #    print("adding")
         #   simulacao.insertEvent('A', round(Na/2))
          #  simulacao.insertEvent('B', round(Nb/2))   
            
        if simulacao.totalMolCount.getCount('C') > Nc: 
            
            c=cap.addE(c,em.evt(ct+obsrand.exprandom(Ts),'extr'))   
            simulacao.removeEvent('C', -1)
            
        if simulacao.totalMolCount.getCount('A') < (Na / 2) and simulacao.totalMolCount.getCount('B') < (Nb / 2): #Adição de reagente
        
            c=cap.addE(c,em.evt(ct+obsrand.exprandom(Ta),'adic'))
            simulacao.insertEvent('A', round(Na/2))
            simulacao.insertEvent('B', round(Nb/2))  
                
            
            
            
        ce=cap.nextE(c)
        ct = em.time(ce)
        ck = em.kind(ce)
        c=cap.delE(c)
        xtrace.append(ct)
        yAtrace.append(simulacao.totalMolCount.getCount('A'))
        yBtrace.append(simulacao.totalMolCount.getCount('B'))
        yCtrace.append(simulacao.totalMolCount.getCount('C'))
        
        #yAtrace.append(simulacao.totalMolConsumed.getCount('A'))
        #yBtrace.append(simulacao.totalMolConsumed.getCount('B'))
        #yCtrace.append(simulacao.totalMolRetrieved.getCount('C'))
            
    print(simulacao.totalMolRetrieved.getCount('C')) 
    print('feito :))')
    
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de cenas')
    if max(yAtrace)>max(yBtrace):
        b=max(yAtrace)
    else:
        b=max(yBtrace)
    plt.axis([0, max(xtrace), 0, b+10])
    
    
    plt.plot(xtrace,yBtrace,'-')
    plt.plot(xtrace,yAtrace,'-')
    plt.plot(xtrace,yCtrace,'-')
    
    
    
    
    
    