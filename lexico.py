from ttoken import TOKEN

'''
DÚVIDAS
- Em que momento o método getToken é chamado?
- As strings em Pascal começam apenas com aspas simples? ASPAS SIMPLES E DUPLAS
- Atribuição de variável e de constante é diferente para variáveis e constantes? No nosso caso, a gente criou so um token pra atribuicao, seria para := ?  https://pt.wikibooks.org/wiki/Pascal/Comandos_de_Atribui%C3%A7%C3%A3o
- Só pra confirmar: os operadores de soma e subtracao terão o mesmo token. Os operadadores de divisao, multiplicacao, e relacionais tambem SIM
- Pra que serve o token de erro que criamos, e como eu sei quando usá-lo? Já sei
- ERRO: 
  código:
  ;
  m 
  ele chega ao fim do arquivo depois de ler uma palavra reservada "m" e continua no estado 2 mas ele leu um fim de arquivo
'''

class Lexico:

    def __init__(self, arqFonte):
        self.arqFonte = arqFonte #objeto que contém o arquivo
        self.codigoFonte = self.arqFonte.read() #leu o arquivo, e agora ele é uma string. A partir daqui leremos o código fonte
        self.tamFonte = len(self.codigoFonte) #recebe o tamanho do código (que nesse caso é uma string)
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
        if simbolo == '\0':
            return
        if self.indiceFonte > 0: #se não é o primeiro caractere, ele volta o índice (se for o primeiro caractere, o índice permanece, para o primeiro caractere o índice é 0)
            self.indiceFonte -= 1

        self.coluna -= 1 #ele volta um coluna

    #esse método serve para testar se o token, lexema, linha e coluna estão corretos
    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        print(f'(tk={msg} lex="{lexema}" lin={linha} col={coluna})')

    #esse método é o coração do lexico, é onde implementamos o autômato que reconhece os lexemas (vai formando os lexemas caractere a caractere, e pega o token desse lexema)
    def getToken(self):

        estado = 1
        simbolo = self.getchar()
        lexema = ''

        while simbolo in ["/", " ", "\t", "\n"]:
            # descarta comentários (que iniciam com // até o fim da linha)
            if simbolo == "/":
                # lexema = lexema + simbolo
                simbolo = self.getchar()
                if simbolo == "/":
                    simbolo = self.getchar()

                    while simbolo != "\n":
                        simbolo = self.getchar()
                else:
                    # Se não for um comentário, o caractere '/' não deve ser descartado.
                    self.ungetchar(simbolo)  # retorna o caractere
                    simbolo = "/"
                    break
            # descarta linhas brancas e espaços
            while simbolo in [" ", "\t", "\n"]:
                simbolo = self.getchar()



        #aqui vai começar a formar um lexema e classificá-lo em token
        linha = self.linha
        coluna = self.coluna

        # quando acha um lexema, interrompe o while e retorna o token, lexema, linha e coluna para quem chamou
        while(True):
            # início do autômato
            if estado == 1:

                #os lexemas que possuem apenas um caracetere sao faceis de tratar, basta verificar se é o simbolo em questão, e retornar ele, o token dele, a linha e a coluna que ele está
                if simbolo == "(":
                    return (TOKEN.abrePar,'(',linha,coluna)
                elif simbolo == ")":
                    return (TOKEN.fechaPar,')',linha,coluna)
                elif simbolo == ";":
                    return (TOKEN.ptoVirgula,';',linha,coluna)
                elif simbolo == ",":
                    return (TOKEN.virgula,',',linha,coluna)
                elif simbolo == "[":
                    return (TOKEN.abreCol,'[',linha,coluna)
                elif simbolo == "]":
                    return (TOKEN.fechaCol,']',linha,coluna)
                elif simbolo == "+":
                    return (TOKEN.addop,'+',linha,coluna)
                elif simbolo == "-":
                    return (TOKEN.addop,'-',linha,coluna)
                elif simbolo == "*":
                    return (TOKEN.mulop,'*',linha,coluna)
                elif simbolo == "/":
                    return (TOKEN.mulop,'/',linha,coluna)
                elif simbolo == "=":
                    return(TOKEN.relop,'=',linha,coluna)
                elif simbolo == '\0':
                    return(TOKEN.eof,'<eof>',linha,coluna)

                #alguns lexemas mais complexos (quando vier uma palavra reservada por exemplo, preciso saber até onde ler pra pegar seu token)
                elif simbolo.isalpha():
                    estado = 2 # identificadores e palavras reservadas
                elif simbolo.isdigit():
                    estado = 3 # números (reais e inteiros)
                elif simbolo == '"':
                    estado = 4 # strings

                # outros lexemas precisam de tratamento. [Ex: Ao ler um <, ele pode ser <, <=, ou <> (diferente)]
                elif simbolo == ".":
                    estado = 5  # . ou ..
                elif simbolo == ":":
                    estado = 6  # : ou :=
                elif simbolo == ">":
                    estado = 7  # >, ou >=
                elif simbolo == "<":
                    estado = 8  # <, <= ou <>

                else: #caso o que foi lido não é nada válido na linguagem
                    lexema += simbolo
                    return(TOKEN.erro, lexema, linha, coluna)


            elif estado == 2: #identificadores e palavras reservadas (sao sequencias de letras ou letras intercaladas com numeros: while, nome, idade1)
                if simbolo.isalnum(): #permanece no estado 2 enquanto estiver lendo uma sequência alfanumerica
                    estado = 2
                #elif simbolo == '\0':
                 #   return(TOKEN.eof,'\0',linha,coluna)
                else: #quando o identificador ou palavra reservada acabar
                    self.ungetchar(simbolo)  #deslê o último simbolo lido (que não faz parte do identificador ou palavra reservada)
                    token = TOKEN.reservada(lexema) #pega o token do lexema, ou ele é reserva ou é um identificador (Dentro de TOKEN já tem essa verificação)
                    return (token,lexema,linha,coluna)


            elif estado == 3: # números (reais e inteiros)
                if simbolo.isdigit(): #lê numeros inteiros e permanece no 3 enquanto tiver lendo número
                    estado = 3
                elif simbolo == '.': #se achar um ponto, quer dizer que o número é real, portanto vai para o estado 31
                    estado = 31
                elif simbolo.isalpha():
                    lexema += simbolo
                    return (TOKEN.erro,lexema,linha,coluna)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.numInteger,lexema,linha,coluna)

            elif estado == 31:
                if simbolo.isdigit(): #se achou número depois do ponto, vai para o estado 32
                    estado = 32
                elif simbolo == '.': #leu o .. do vetor. entao precisamos devolver o número que foi lido, e dar um unget pra desler esse segundo ponto e o primeiro ponto
                    self.ungetchar(simbolo)
                    self.ungetchar(simbolo)
                    #lexeama = 1.
                    lexema = lexema[:-1] # lexema = lexema[:-1] também dá certo
                    return (TOKEN.numInteger, lexema, linha, coluna)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.erro,lexema,linha,coluna)

            elif estado == 32:
                if simbolo.isdigit(): #continua no estado 32 quando lê numeros
                    estado = 32
                elif simbolo.isalpha(): #se tiver alugma letra no meio do número ele retorna erro
                    lexema += simbolo
                    return (TOKEN.erro,lexema,linha,coluna)
                else: #o número acabou
                    self.ungetchar(simbolo)
                    return (TOKEN.numReal,lexema,linha,coluna)


            elif estado == 4: # strings
                #strings
                while(True):
                    if simbolo == '"': #aqui chegou ao fim da string
                        lexema += simbolo
                        return (TOKEN.string,lexema,linha,coluna)
                    if simbolo in ['\n','\0']: #se tiver uma quebra de linha no meio da string ou se estiver no fim do arquivo, é erro (o \n e o \0 é visto como um caractere so pelo assembly)
                        return (TOKEN.erro,lexema,linha,coluna)
                    if simbolo == '\\': #se a string tiver um \ no meio dela, ela será lida e o caractere depois dela será desligado (entao se vier um " depois dela, a gente pega)
                        lexema += simbolo
                        simbolo = self.getchar()
                        if simbolo in ['\n','\0']:
                            return (TOKEN.erro,lexema,linha,coluna)

                    lexema = lexema + simbolo
                    simbolo = self.getchar()


            elif estado == 5: #. ou ..
                if simbolo == ".":
                    return (TOKEN.ptopto,'..',linha,coluna)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.pto,'.',linha,coluna)


            elif estado == 6: # : ou :=
                if simbolo == "=":
                    return (TOKEN.assignop,':=',linha,coluna)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.doisPtos,':',linha,coluna)


            elif estado == 7: # >, ou >=
                if simbolo == "=":
                    return (TOKEN.relop,'>=',linha,coluna)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.relop,'>',linha,coluna)


            elif estado == 8: # <, <= ou <>
                if simbolo == "=":
                    return (TOKEN.relop,'<=',linha,coluna)
                elif simbolo == ">":
                    return (TOKEN.relop,'<>',linha,coluna)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.relop,'<',linha,coluna)




            lexema = lexema + simbolo
            #estado = 1
            simbolo = self.getchar()

    '''
     def testaLexico(self):
         self.tokenLido = self.getToken()
         (token, lexema, linha, coluna) = self.tokenLido
         while token != TOKEN.eof:
             self.imprimeToken(self.tokenLido)
             self.tokenLido = self.getToken()
             (token, lexema, linha, coluna) = self.tokenLido
     '''


