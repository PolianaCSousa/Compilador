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



    #-------------------------------- Implementando a gramática --------------------------------

    #<program> -> program id ( <identifier_list> ) ; <declarations> <subprogram_declarations> <compound_statement> .
    def program(self):
        self.consome(TOKEN.PROGRAM)
        self.consome(TOKEN.id)
        self.consome(TOKEN.abrePar)
        self.identifier_list()
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirgula)
        self.declarations()
        self.subprogram_declarations()
        self.compound_statement()
        self.consome(TOKEN.pto)

    #<identifier_list> -> id <resto_identifier_list>
    def identifier_list(self):
        self.consome(TOKEN.id)
        self.resto_identifier_list()

    #<resto_identifier_list> ->, id < resto_identifier_list > | LAMBDA
    def resto_identifier_list(self):
        if self.tokenLido[0] == TOKEN.virgula:
            self.consome(TOKEN.virgula)
            self.consome(TOKEN.id)
            self.resto_identifier_list()
        else:
            pass
    #<declarations> -> var <identifier_list> : <type> ; <declarations> | LAMBDA
    def declarations(self):
        if self.tokenLido[0] == TOKEN.VAR:
            self.consome(TOKEN.VAR)
            self.identifier_list()
            self.consome(TOKEN.doisPtos)
            self.type()
            self.consome(TOKEN.ptoVirgula)
            self.declarations()
        else:
            pass

    #<type> -> <standard_type> | array [ num .. num ] of <standard_type>
    def type(self):
        if self.tokenLido[0] == TOKEN.ARRAY:
            self.consome(TOKEN.ARRAY)
            self.consome(TOKEN.abreCol)
            self.consome(TOKEN.numInteger)
            self.consome(TOKEN.ptopto)
            self.consome(TOKEN.numInteger)
            self.consome(TOKEN.fechaCol)
            self.consome(TOKEN.OF)
            self.standard_type()
        else:
            self.standard_type()

    #<standard_type> -> integer | real
    def standard_type(self): #CONFIRMAR
        if self.tokenLido[0] == TOKEN.numInteger:
            self.consome(TOKEN.numInteger)
        else:
            self.consome(TOKEN.numReal)

    #SUBPROGRAM DECLARION?
    #<subprogram_declarations> -> <subprogram_declarion> ; <subprogram_declarations> | LAMBDA
    def subprogram_declarations(self):
        if self.tokenLido[0] == TOKEN.BEGIN:
            pass
        else:
            self.subprogram_declaration()
            self.consome(TOKEN.ptoVirgula)
            self.subprogram_declarations()

    #<subprogram_declaration> -> <subprogram_head> <declarations> <compound_statement>
    def subprogram_declaration(self):
        self.subprogram_head()
        self.declarations()
        self.compound_statement()

    #<subprogram_head> -> function id <arguments> : <standard_type> ; | procedure id <arguments> ;
    def subprogram_head(self):
        if self.tokenLido[0] == TOKEN.FUNCTION:
            self.consome(TOKEN.FUNCTION)
            self.consome(TOKEN.id)
            self.arguments()
            self.consome(TOKEN.doisPtos)
            self.standard_type()
            self.consome(TOKEN.ptoVirgula)
        else:
            self.consome(TOKEN.PROCEDURE)
            self.consome(TOKEN.id)
            self.arguments()
            self.consome(TOKEN.ptoVirgula)

    #<arguments> -> ( <parameter_list> ) | LAMBDA
    def arguments(self):
        if self.tokenLido[0] == TOKEN.abrePar:
            self.consome(TOKEN.abrePar)
            self.parameter_list()
            self.consome(TOKEN.fechaPar)
        else:
            pass

    #<parameter_list> -> <identifier_list> : <type> <resto_parameter_list>
    def parameter_list(self):
        self.identifier_list()
        self.consome(TOKEN.doisPtos)
        self.type()
        self.resto_parameter_list()

    #<resto_parameter_list> -> ; <identifier_list> : <type> <resto_parameter_list> | LAMBDA
    def resto_parameter_list(self):
        if self.tokenLido[0] == TOKEN.ptoVirgula:
            self.consome(TOKEN.ptoVirgula)
            self.identifier_list()
            self.consome(TOKEN.doisPtos)
            self.type()
            self.resto_parameter_list()
        else:
            pass

    #<compound_statement> -> begin <optional_statements> end
    def compound_statement(self):
        self.consome(TOKEN.BEGIN)
        self.optional_statements()
        self.consome(TOKEN.END)

    #CONFIRMAR SE ESTÁ CERTO OLHANDO O PREDICT
    #< optional_statements > -> < statement_list > | LAMBDA
    def optional_statements(self):
        if self.tokenLido[0] == TOKEN.END:
            pass
        else:
            self.statement_list()

    #<statement_list> -> <statement> <resto_statement_list>
    def statement_list(self):
        pass

    #< resto_statement_list > ->; < statement > < resto_statement_list > | LAMBDA
    def resto_statement_list(self):
        pass

    #<statement> -> <variable> assignop <expression> |<procedure_statement> | <compound_statement> | <if_statement> | while <expression> do <statement> | <inputOutput>
    def statement(self):
        pass

    #<if_statement> -> if <expression> then <statement> <opc_else>
    def if_statement(self):
        pass

    #<opc_else> -> else <statement> | LAMBDA
    def opc_else(self):
        pass

    #<variable> -> id <opc_index>
    def variable(self):
        pass

    #<opc_index> -> [ <expression> ] | LAMBDA
    def opc_index(self):
        pass

    #<procedure_statement> -> id <opc_parameters>
    def procedure_statement(self):
        pass

    #<opc_parameters> -> ( <expression_list> ) | LAMBDA
    def opc_parameters(self):
        pass

    #<expression_list> -> <expression> <resto_expression_list>
    def expression_list(self):
        pass

    #<resto_expression_list> -> , <expression> <resto_expression_list> | LAMBDA
    def resto_expression_list(self):
        pass

    #<expression> -> <simple_expression> <resto_expression>
    def expression(self):
        pass

    #<resto_expression> -> relop <simple_expression> <resto_expression> | LAMBDA
    def resto_expression(self):
        pass

    #<simple_expression> -> <term> <resto_simple_expression>
    def simple_expression(self):
        pass

    #<resto_simple_expression> -> addop <term> <resto_simple_expression> | LAMBDA
    def resto_simple_expression(self):
        pass

    #<term> -> <uno> <resto_term>
    def term(self):
        pass

    #<resto_term> -> mulop <uno> <resto_term> | LAMBDA
    def resto_term(self):
        pass

    #<uno> -> <factor> | addop <factor>
    def uno(self):
        pass

    #<factor> -> id <resto_id> | num | ( <expression> ) | not <factor>
    def factor(self):
        pass

    #<resto_id> -> ( <expression_list> ) | LAMBDA
    def resto_id(self):
        pass

    #<inputOutput> -> writeln(<outputs>) ; | write(<outputs>) ; | read(id) ; | readln(id) ;
    def inputOutput(self):
        pass

    #<outputs> -> <out> <restoOutputs>
    def outputs(self):
        pass

    #<restoOutputs> -> , <out> <restoOutputs> | LAMBDA
    def restoOutputs(self):
        pass

    #<out> -> num | id | string
    def out(self):
        pass