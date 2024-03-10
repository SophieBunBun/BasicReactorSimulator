# Modulo cap
# Disponibiliza as operacoes necessarias para a criacao e
# manipulacao da Cadeia de Acontecimentos Pendentes
import sys
sys.path.append('C:\\Users\\gusta\\OneDrive\\Ambiente de Trabalho\\LEQ\\CP\\Projeto\\módulos')

import event_manip as event

def newc():
    return []
    
def addE(c,e):
    return [e1 for e1 in c if event.time(e1)<event.time(e)]+[e]+\
           [e1 for e1 in c if event.time(e1)>event.time(e)]

def delE(c):
    if len(c)>0:
        return c[1:]
    else:
        print("Erro de delE! A cap está vazia")

def nextE(c):
    if len(c)>0:
        return c[0]
    else:
        print("Erro de nextE! A cap está vazia")
        
def showE(c):
    for e in c:
        print(event.time(e), event.kind(e))   