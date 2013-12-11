from parser import lex_and_parse
import readline

class Environment(dict):
    def __init__(self, initial_val={}):
        for key, value in initial_val.iteritems():
            self[key] = value

def evaluate(ast, env):
    if ast['type'] == 'program':
        return evaluate(ast['value'], env)
    elif ast['type'] == 'let_expression':
        ident = ast['identifier']
        env[ident] = evaluate(ast['expression'], env)
        return None
    elif ast['type'] == 'expression':
        op1 = evaluate(ast['operand1'], env)
        op2 = evaluate(ast['operand2'], env)
        op_func = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y,
            '%': lambda x, y: x % y
        }.get(ast['operator'])
        return op_func(op1, op2)
    elif ast['type'] == 'number':
        return ast['value']
    elif ast['type'] == 'identifier':
        if not ast['value'] in env:
            raise TypeError("Identifier {} referenced before assignment".format(ast['value']))
        else:
            return env[ast['value']]

def repl(prompt=">> "):
    running = True
    env = Environment()
    while running:
        try:
            input_str = raw_input(prompt)
            if input_str == '':
                continue
        except EOFError:
            running = False
        else:
            try:
                ast = lex_and_parse(input_str)
            except TypeError as e:
                print "Syntax error: {}".format(e)
            else:
                result = evaluate(ast, env)
                if result is not None:
                    print result

def main():
    print "Reverse Polish Calculator, by Sean Gillespie"
    print "now powered by lex and yacc!"
    print "Control-D to exit"
    repl()
    print ""
    print "Bye!"
        
if __name__ == '__main__':
    main()
