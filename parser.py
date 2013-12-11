import ply.lex as lex
import ply.yacc as yacc
import pprint

reserved_words = {
    'let': 'LET'
}

tokens = [
    "IDENTIFIER",
    "NUMBER",
    "OPERATOR",
    "LPAREN",
    "RPAREN"
] + list(reserved_words.values())

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r"\d+(\.\d+)*"
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = float(t.value)
    return t
    
t_OPERATOR = r'[\+-\^%\*/]'
t_LPAREN = '\('
t_RPAREN = '\)'

def t_error(t):
    raise TypeError("Invalid character: {}".format(t.value[0]))

t_ignore = r' '
    
lex.lex()

def p_program(p):
    '''
    program : let_expression
            | expression
    '''
    p[0] = {
        'type': 'program',
        'value': p[1]
    }

def p_let_expression(p):
    '''
    let_expression : LPAREN LET IDENTIFIER expression RPAREN
    '''
    p[0] = {
        'type': 'let_expression',
        'identifier': p[3],
        'expression': p[4]
    }

def p_expression(p):
    '''
    expression : LPAREN expression expression OPERATOR RPAREN
               | NUMBER
               | IDENTIFIER
    '''
    if len(p) == 6:
        p[0] = {
            'type': 'expression',
            'operand1': p[2],
            'operand2': p[3],
            'operator': p[4]
        }
    elif type(p[1]) == str:
        p[0] = {
            'type': 'identifier',
            'value': p[1]
        }
    else:
        p[0] = {
            'type': 'number',
            'value': p[1]
        }

def p_error(p):
    raise TypeError("Syntax error at {}".format(p.value))

yacc.yacc()

def lex_and_parse(string_in):
    return yacc.parse(string_in)

