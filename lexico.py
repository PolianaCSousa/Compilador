from ttoken import TOKEN

'''
DÚVIDAS
- Em que momento o método getToken é chamado?
'''

class Lexico:

    def __init__(self, arqFonte):
        self.arqFonte = arqFonte #objeto que contém o arquivo
        self.codigoFonte = self.arqFonte.read() #leu o arquivo, e agora ele é uma string. A partir daqui leremos o código fonte
        self.tamFonte = len(self.tamFonte) #recebe o tamanho do código (que nesse caso é uma string)
        self.indiceFonte = 0
        self.tokenLido = None #ele lerá um caractere por vez, e o léxico retornará para o sintático a quadrupla: (token, lexema, linha, coluna)
        self.linha = 1 #corresponde a linha atual do código fonte
        self.coluna = 0 #corresponde a coluna atual do código fonte

    # verifica se o programa chegou ao fim
    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte

    #o método abaixo lê um caractere do arquivo, e atualiza a linha e a coluna
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

    #Esse método está deslendo um caractere
    def ungetchar(self, simbolo):
        if simbolo == '\n': #se ele leu um \n, ele volta uma linha e deslê esse \n
            self.linha -= 1

        if self.indiceFonte > 0: #se não é o primeiro caractere, ele volta o índice (se for o primeiro caractere, o índice permanece, para o primeiro caractere o índice é 0)
            self.indiceFonte -= 1

        self.coluna -= 1 #ele volta um coluna

    #esse método serve para testar se o token, lexema, linha e coluna estão corretos
    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        print(f'(tk={msg} lex="{lexema}" lin={linha} col={coluna})')

    def getToken(self):

        estado = 1
        simbolo = self.getchar()
        lexema = ''

        # descarta comentários (os comentários iniciam com //)
        if simbolo == '/':
            simbolo = self.getchar()
            if simbolo == '/':
                while simbolo in ['/', ' ', '\t', '\n']:
                    #descarta tudo o que vier depois de // até encontrar um \n
                    simbolo = self.getchar()
                    while simbolo != '\n':
                        simbolo = self.getchar()
                    #descarta linhas brancas e espaços em branco
                    while simbolo in [' ', '\t', '\n']:
                        simbolo = self.getchar()
            else:
                pass
                #vai para o estado que cuida das expressões

        #aqui vai começar a formar um lexema e classificá-lo em token
        linha = self.linha
        coluna = self.coluna

        # quando acha um lexema, interrompe o while e retorna o token, lexema, linha e coluna para quem chamou
        while(True):
            if estado == 1:
                #início do autômato
                if simbolo.isalpha():
                    estado = 2 # identificadores e palavras reservadas
                elif simbolo.isdigit():
                    estado = 3 # números (reais e inteiros)
                elif simbolo == '\'':
                    estado = 4 # strings
                elif simbolo == '(':
                    return (TOKEN.abrePar,'(',linha,coluna)

            lexema = lexema + simbolo
            simbolo = self.getchar()


