#---------------------------------------------------
# Tradutor para a linguagem Mini Pascal
#
# Aluna: Poliana Cristina de Sousa
#---------------------------------------------------
from lexico import Lexico

class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)

    #Função que será implementada no sintático depois
    def traduz(self):
        self.sintatico.traduz()

    def finaliza(self):
        self.arq.close()

# inicia a traducao
if __name__ == '__main__':
    x = Tradutor('programaTeste.txt')
    x.inicializa()
    #x.traduz()
    #x.sintatico.testaLexico()
    x.finaliza()

