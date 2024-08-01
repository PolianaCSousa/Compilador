

class Lexico:

    def __init__(self, arqFonte):
        self.arqFonte = arqFonte #objeto que contém o arquivo
        self.codigoFonte = self.arqFonte.read() #leu o arquivo, e agora ele é uma string. A partir daqui leremos o código fonte
        self.tamFonte = len(self.tamFonte) #recebe o tamanho do código (que nesse caso é uma string)
        self.indiceFonte = 0
        self.tokenLido = None #ele lerá um caractere por vez, e o léxico retornará para o sintático a quadrupla: (token, lexema, linha, coluna)
        self.linha = 1 #corresponde a linha atual do código fonte
        self.coluna = 0 #corresponde a coluna atual do código fonte

    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte #verifica se o programa chegou ao fim

    def getchar(self):
        if self.fimDoArquivo():
            return '\0'
        caractere = self.codigoFonte[self.indiceFonte]
        self.indiceFonte += 1
        if caractere == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return caractere