from lexico import TOKEN, Lexico
class Sintatico:
    def __init__(self, lexico):
        self.lexico = lexico

    def traduz(self):
        self.tokenLido = self.lexico.getToken() # o sintatico pede para o lexico token por token
        try: #ao receber o token ele vai na gramática e verifica se está de acordo com a gramática
            self.p() #esse é o método de ponto de partida que faz ele entrar na gramátic
            print('Traduzido com sucesso.')
        except:
            pass

    #o método que chama o consome, vai passar o lexema pra ser consumido. Entao aqui no metodo consome, é feita a verificação: o token que é pra ser consumido, é igual ao tokenLido do método traduz? Se sim, deu certo, se não, trata o erro aqui mesmo no consome "era esperado (tokenAtual) tal coisa mas veio tal coisa (tokenLido)"
    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token: #se o token consumido é igual ao token lido, pego um novo token pra analisar
            self.tokenLido = self.lexico.geToken()
        else: #trata o erro quando o token que era pra ser consumido não é igual ao token que foi lido
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f'Era esperado {msgTokenAtual} mas veio {msg}')
            raise Exception


