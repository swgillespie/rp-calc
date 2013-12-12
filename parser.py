import ply.lex as lex
import ply.yacc as yacc
import pprint

reserved_words = {
    'let': 'LET',
    'defun': 'DEFUN'
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
            | defun_expression
    '''
    p[0] = {
        'type': 'program',
        'value': p[1]
    }

def p_defun_expression(p):
    '''
    defun_expression : LPAREN DEFUN IDENTIFIER LPAREN param_list RPAREN expression RPAREN
    '''
    p[0] = {
        'type': 'defun_expression',
        'fn_name': p[3],
        'param_list': p[5],
        'expression': p[7]
    }

def p_param_list(p):
    '''
    param_list : IDENTIFIER param_list
               |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

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
    expression : LPAREN OPERATOR expression expression RPAREN
               | function_call
               | ident_or_num
    '''
    if len(p) == 6:
        p[0] = {
            'type': 'expression',
            'operand1': p[3],
            'operand2': p[4],
            'operator': p[2]
        }
    else:
        p[0] = p[1]
        
            

def p_ident_or_num(p):
    '''
    ident_or_num : NUMBER
                 | IDENTIFIER
    '''
    if type(p[1]) == str:
        p[0] = {
            'type': 'identifier',
            'value': p[1]
        }
    else:
        p[0] = {
            'type': 'number',
            'value': p[1]
        }

    
def p_function_call(p):
    '''
    function_call : LPAREN IDENTIFIER actual_param_list RPAREN
    '''
    p[0] = {
        'type': 'function_call',
        'fn_name': p[2],
        'args': p[3]
    }

def p_actual_param_list(p):
    '''
    actual_param_list : expression actual_param_list
                      |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]


def p_error(p):
    raise TypeError("Syntax error at {}".format(p.value))

yacc.yacc()

def lex_and_parse(string_in):
    return yacc.parse(string_in)

