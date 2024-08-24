# Classe sintatica

from lexico import TOKEN, Lexico
from semantico import Semantico


class Sintatico:

    def _init_(self, lexico):

        self.lexico = lexico
        self.semantico = Semantico(self)
        # self.nomeAlvo = 'alvo.out'
        # self.semantico = Semantico(self.nomeAlvo)

    def traduz(self):

        self.tokenLido = self.lexico.getToken()

        try:
            self.program()
            print('Traduzido com sucesso.')
        except:
            pass
        # self.semantico.finaliza()

    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token:
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f'Era esperado {msgTokenAtual} mas veio {msg}')
            raise Exception

    # --------------------------------------------------------------------------------------------------------------------
    def program(self):
        # <program> -> program id () ; <declarations> <subprogram_declarations> <compound_statement> .
        self.consome(TOKEN.PROGRAM)
        self.consome(TOKEN.id)
        self.consome(TOKEN.abrePar)
        # na prática nós não vamos receber parâmetros do programa, portanto, não precisa implementar o identifier_list dentro do ()
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
        self.declarations()
        self.subprogram_declarations()
        self.compound_statement()
        self.consome(TOKEN.pto)

    # --------------------------------------------------------------------------------------------------------------------
    def identifier_list(self):
        # <identifier_list> -> id <resto_identifier_list>
        nome = self.tokenLido[1]
        self.consome(TOKEN.id)
        lista = [nome]
        lista2 = self.resto_identifier_list()
        return lista + lista2

    # ------------------------------------------------------------------------------------------------------------------
    def resto_identifier_list(self):
        # <resto_identifier_list> -> , id <resto_identifier_list> | LAMBDA

        if self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            return self.identifier_list()
        else:
            return []

    # ------------------------------------------------------------------------------------------------------------------
    def declarations(self):
        # <declarations> -> var <identifier_list> : <type> ; <declarations> | LAMBDA

        if self.tokenLido[0] == TOKEN.VAR:
            self.consome(TOKEN.VAR)
            nomes = self.identifier_list()
            self.consome(TOKEN.doisPontos)
            tipo = self.type()
            self.consome(TOKEN.ptoVirg)
            self.semantico.declara(nomes, tipo)
            self.declarations()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def type(self):
        # <type> -> <standard_type> | array [ num .. num ] of <standard_type>
        if self.tokenLido[0] == TOKEN.ARRAY:
            self.consome(TOKEN.ARRAY)
            self.consome(TOKEN.abreColchete)
            self.consome(TOKEN.num_inteiro)
            self.consome(TOKEN.ptoPto)
            self.consome(TOKEN.num_inteiro)
            self.consome(TOKEN.fechaColchete)
            self.consome(TOKEN.OF)
            tipo = self.standard_type()
            return (TOKEN.ARRAY, tipo)
        else:
            return self.standard_type()

    # ------------------------------------------------------------------------------------------------------------------
    def standard_type(self):
        # <standard_type> -> integer | real
        if self.tokenLido[0] == TOKEN.INTEGER:
            self.consome(TOKEN.INTEGER)
            return TOKEN.INTEGER
        else:
            self.consome(TOKEN.REAL)
            return TOKEN.REAL

    # ------------------------------------------------------------------------------------------------------------------
    def subprogram_declarations(self):
        # <subprogram_declarations> -> <subprogram_declaration> ; <subprogram_declarations> | LAMBDA

        if self.tokenLido[0] == TOKEN.BEGIN:
            pass
        else:
            self.subprogram_declaration()
            self.consome(TOKEN.ptoVirg)
            self.subprogram_declarations()

    # ------------------------------------------------------------------------------------------------------------------
    def subprogram_declaration(self):
        # <subprogram_declaration> -> <subprogram_head> <declarations> <compound_statement>
        self.subprogram_head()
        self.declarations()
        self.compound_statement()

    # ------------------------------------------------------------------------------------------------------------------
    def subprogram_head(self):
        # <subprogram_head> -> function id <arguments> : <standard_type> ; | procedure id <arguments> ;
        if self.tokenLido[0] == TOKEN.FUNCTION:
            self.consome(TOKEN.FUNCTION)
            nomeFuncao = self.tokenLido[1]
            self.consome(TOKEN.id)
            self.semantico.declara(nomeFuncao, TOKEN.FUNCTION)
            self.arguments()
            self.consome(TOKEN.doisPontos)
            self.standard_type()
            self.consome(TOKEN.ptoVirg)
        else:
            self.consome(TOKEN.PROCEDURE)
            nomeProcedimento = self.tokenLido[1]
            self.consome(TOKEN.id)
            self.semantico.declara(nomeProcedimento, TOKEN.PROCEDURE)
            self.arguments()
            self.consome(TOKEN.ptoVirg)

    # ------------------------------------------------------------------------------------------------------------------
    def arguments(self):
        # <arguments> -> ( <parameter_list> ) | LAMBDA
        if self.tokenLido[0] == TOKEN.abrePar:
            self.consome(TOKEN.abrePar)
            self.parameter_list()
            self.consome(TOKEN.fechaPar)
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def parameter_list(self):
        # <parameter_list> -> <identifier_list> : <type> <resto_parameter_list>
        self.identifier_list()
        self.consome(TOKEN.doisPontos)
        self.type()
        self.resto_parameter_list()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_parameter_list(self):
        # <resto_parameter_list> ->; <identifier_list> : < type > <resto_parameter_list> | LAMBDA
        if self.tokenLido[0] == TOKEN.ptoVirg:
            self.consome(TOKEN.ptoVirg)
            self.identifier_list()
            self.consome(TOKEN.doisPontos)
            self.type()
            self.resto_parameter_list()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def compound_statement(self):
        # <compound_statement> -> begin <optional_statements> end
        self.consome(TOKEN.BEGIN)
        self.optional_statements()
        self.consome(TOKEN.END)

    # ------------------------------------------------------------------------------------------------------------------
    def optional_statements(self):
        # <optional_statements> -> <statement_list> | LAMBDA
        if self.tokenLido[0] == TOKEN.END:
            pass
        else:
            self.statement_list()

    # ------------------------------------------------------------------------------------------------------------------
    def statement_list(self):
        # <statement_list> -> <statement> <resto_statement_list>
        self.statement()
        self.resto_statement_list()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_statement_list(self):
        # <resto_statement_list> -> ; <statement> <resto_statement_list> | LAMBDA
        if self.tokenLido[0] == TOKEN.ptoVirg:
            self.consome(TOKEN.ptoVirg)
            self.statement()
            self.resto_statement_list()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def statement(self):
        # <statement> -> <variable> assignop <expression> | <procedure_statement> | <compound_statement> | <if_statement> | while <expression> do <statement> | <inputOutput>
        if self.tokenLido[0] == TOKEN.id:
            nome = self.tokenLido[1]
            if self.semantico.existe_id(nome):
                tipo = self.semantico.consulta_tipo_id(nome)
                if tipo in [TOKEN.INTEGER, TOKEN.REAL]:
                    self.variable()
                    self.consome(TOKEN.assignop)
                    self.expression()
                else:
                    self.procedure_statement()
            else:
                msg = 'Idenficador ' + nome + ' não declarado.'
                self.semantico.erroSemantico(msg)

        elif self.tokenLido[0] == TOKEN.BEGIN:
            self.compound_statement()

        elif self.tokenLido[0] == TOKEN.IF:
            self.if_statement()

        elif self.tokenLido[0] == TOKEN.RETURN:
            self.consome(TOKEN.RETURN)
            self.expression()

        elif self.tokenLido[0] == TOKEN.WHILE:
            # while <expression> do <statement>
            self.consome(TOKEN.WHILE)
            self.expression()
            self.consome(TOKEN.DO)
            self.statement()

        else:
            # self.tokenLido[0] in [TOKEN.READ, TOKEN.READLN, TOKEN.WRITE, TOKEN.WRITELN]:
            self.inputOutput()

    # ------------------------------------------------------------------------------------------------------------------
    def if_statement(self):
        # <if_statement> -> if <expression> then <statement> <opc_else>

        self.consome(TOKEN.IF)
        self.expression()
        self.consome(TOKE.then)
        self.statement()
        self.opc_else()

    # ------------------------------------------------------------------------------------------------------------------
    def opc_else(self):
        # <opc_else> -> else < statement > | LAMBDA
        if self.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.statement()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def variable(self):
        # <variable> -> id <opc_index>
        self.consome(TOKEN.id)
        self.opc_index()

    # ------------------------------------------------------------------------------------------------------------------
    def opc_index(self):
        # <opc_index> -> [ <expression> ] | LAMBDA

        if self.tokenLido[0] == TOKEN.abreColchete:
            self.consome(TOKEN.abreColchete)
            self.expression
            self.consome(TOKEN.fechaColchete)
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def procedure_statement(self):
        # <procedure_statement> -> id <opc_parameters>
        self.consome(TOKEN.id)
        self.opc_parameters()

    # ------------------------------------------------------------------------------------------------------------------
    def opc_parameters(self):
        # <opc_parameters> -> ( <expression_list> ) | LAMBDA
        if self.tokenLido[0] == TOKEN.abrePar:
            self.consome(TOKEN.abrePar)
            self.expression_list
            self.consome(TOKEN.fechaPar)
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def expression_list(self):
        # <expression_list> -> <expression> <resto_expression_list>
        self.expression()
        self.resto_expression_list()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_expression_list(self):
        # <resto_expression_list> -> , <expression> <resto_expression_list> | LAMBDA
        if self.tokenLido[0] == TOKEN.ptoVirg:
            self.consome(TOKEN.ptoVirg)
            self.expression()
            self.resto_expression_list()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def expression(self):
        # <expression> -> <simple_expression> <resto_expression>
        self.simple_expression()
        self.resto_expression()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_expression(self):
        # <resto_expression> -> relop <simple_expression> <resto_expression> | LAMBDA
        while self.tokenLido[0] == TOKEN.relop:
            self.simple_expression()
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def simple_expression(self):
        # <simple_expression> -> <term> <resto_simple_expression>
        self.term()
        self.resto_simple_expression()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_simple_expression(self):
        # <resto_simple_expression> -> addop <term> <resto_simple_expression> | LAMBDA
        if self.tokenLido[0] == TOKEN.addop:
            self.consome(TOKEN.addop)
            self.term()
            self.resto_simple_expression()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def term(self):
        # <term> -> <uno> <resto_term>
        self.uno
        self.resto_term()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_term(self):
        # <resto_term> -> mulop <uno> <resto_term> | LAMBDA
        if self.tokenLido[0] == TOKEN.mulop:
            self.consome(TOKEN.mulop)
            self.uno()
            self.resto_term()
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def uno(self):
        # <uno> -> <factor> | addop <factor>
        if self.tokenLido[0] in [TOKEN.id, TOKEN.num_inteiro, TOKEN.num_real, TOKEN.abrePar, TOKEN.NOT]:
            self.factor()
        else:
            self.consome(TOKEN.addop)
            self.factor()

    # ------------------------------------------------------------------------------------------------------------------
    def factor(self):
        # <factor> -> id <resto_id> | num | ( <expression> ) | not <factor>
        if self.tokenLido[0] == TOKEN.id:
            self.consome(TOKEN.id)
            self.resto_id()
        elif self.tokenLido[0] == TOKEN.num_inteiro:
            self.consome(TOKEN.num_inteiro)
        elif self.tokenLido[0] == TOKEN.num_real:
            self.consome(TOKEN.num_real)
        elif self.tokenLido[0] == TOKEN.abrePar:
            self.consome(TOKEN.abrePar)
            self.expression()
            self.consome(TOKEN.fechaPar)
        else:
            # self.tokenLido[0] == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.factor()

    # ------------------------------------------------------------------------------------------------------------------
    def resto_id(self, token_id):
        if self.tokenLido[0] == TOKEN.abrePar:
            tipo_id = self.semantico.consulta_tipo_id(token_id[1])
            if tipo_id != TOKEN.FUNCTION:
                msg = 'O identificador ' + token_id[1] + ' não é uma função.'
                self.semantico.erroSemantico(msg)
            self.consome(TOKEN.abrePar)
            self.expression_list()
            self.consome(TOKEN.fechaPar)
        else:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def inputOutput(self):
        # <inputOutput> --> writeln(<outputs>) | write(<outputs>) | read(id) | readln(id)
        if self.tokenLido[0] == TOKEN.WRITELN:
            self.consome(TOKEN.WRITELN)
            self.consome(TOKEN.abrePar)
            self.outputs()
            self.consome(TOKEN.fechaPar)
        elif self.tokenLido[0] == TOKEN.WRITE:
            self.consome(TOKEN.WRITE)
            self.consome(TOKEN.abrePar)
            self.outputs()
            self.consome(TOKEN.fechaPar)
        elif self.tokenLido[0] == TOKEN.READ:
            self.consome(TOKEN.READ)
            self.consome(TOKEN.abrePar)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechaPar)
        else:
            # self.tokenLido[0] == TOKEN.READLN:
            self.consome(TOKEN.READLN)
            self.consome(TOKEN.abrePar)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechaPar)

    # ------------------------------------------------------------------------------------------------------------------
    def outputs(self):
        # <outputs> --> <out> <restoOutputs>
        self.out()
        self.restoOutputs()

    # ------------------------------------------------------------------------------------------------------------------
    def restoOutputs(self):
        # <restoOutputs> --> , <out> <restoOutputs> | LAMBDA
        while self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.out()
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def out(self):
        # <out> --> num | id | string
        if self.tokenLido == TOKEN.num_inteiro:
            self.consome(TOKEN.num_inteiro)
        elif self.tokenLido == TOKEN.num_real:
            self.consome(TOKEN.num_real)
        elif self.tokenLido == TOKEN.id:
            self.consome(TOKEN.id)
        else:
            # self.tokenLido == TOKEN.string:
            self.consome(TOKEN.string)