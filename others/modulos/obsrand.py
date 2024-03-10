# Modulo obsrand
# Disponibiliza uma função para gerar observações de uma variavel aleatoria
# com distribuicao exponencial
from random import random
from math import e

def exprandom(m):
    x=random()
    return 1-e**(-x/m)