from enum import IntEnum

class TOKEN(IntEnum):
    erro = 1
    eof = 2
    PROGRAM = 3
    id = 4
    abrePar = 5
    fechaPar = 6
    ptoVirgula = 7
    pto = 8
    virgula = 9
    VAR = 10
    doisPtos = 11 # :
    ARRAY = 12
    abreCol = 13
    fechaCol = 14
    ptopto = 15  # ..
    OF = 16
    INTEGER = 17
    REAL = 18
    FUNCTION = 19
    PROCEDURE = 20 # função que retorna void
    BEGIN = 21
    END = 22
    assignop = 23 # atrib
    WHILE = 24
    DO = 25
    IF = 26
    THEN = 27
    ELSE = 28
    relop = 29 # operador relacional (>, <, >=, <=, ==, <>)
    addop = 30 # soma e subtração (+ e -)
    mulop = 31 # multiplicação (*), divisão (/) e mod
    numReal = 32
    numInteger = 33
    NOT = 34

    @classmethod
    def msg(cls, token):
        nomes = {
            1:'erro',
            2:'<eof>',
            3:'program',
            4:'ident',
            5:'(',
            6:')',
            7:';',
            8:'.',
            9:',',
            10:'var',
            11:':',
            12:'array',
            13:'[',
            14:']',
            15:'..',
            16:'of',
            17:'inteiro',
            18:'real',
            19:'function',
            20:'procedure',
            21:'begin',
            22:'end',
            23:':=',
            24:'while',
            25:'do',
            26:'if',
            27:'then',
            28:'else',
            29:'operador relacional',
            30:'operador + ou -',
            31:'operador * , /, div, mod',
            32:'número real',
            33:'número inteiro',
            34:'not'
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'program': TOKEN.PROGRAM,
            'var': TOKEN.VAR,
            'array': TOKEN.ARRAY,
            'of': TOKEN.OF,
            'integer': TOKEN.INTEGER,
            'real': TOKEN.REAL,
            'function': TOKEN.FUNCTION,
            'procedure': TOKEN.PROCEDURE,
            'begin': TOKEN.BEGIN,
            'end': TOKEN.END,
            'while': TOKEN.WHILE,
            'do': TOKEN.DO,
            'if': TOKEN.IF,
            'then': TOKEN.THEN,
            'else': TOKEN.ELSE,
            'div': TOKEN.mulop,
            'mod': TOKEN.mulop,
            'not': TOKEN.NOT
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.id

