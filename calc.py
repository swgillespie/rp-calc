from parser import lex_and_parse
import sys
import readline

class Environment(dict):
    def __init__(self, initial_val={}):
        for key, value in initial_val.iteritems():
            self[key] = value

def evaluate(ast, env):
    if ast['type'] == 'program':
        for command in ast['value']:
            value = evaluate(command, env)
            if value is not None:
                print value
    elif ast['type'] == 'let_expression':
        ident = ast['identifier']
        env[ident] =  evaluate(ast['expression'], env)
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
    elif ast['type'] == 'defun_expression':
        ident = ast['fn_name']
        env[ident] = {
            'num_args' : len(ast['param_list']),
            'args' : ast['param_list'],
            'expression': ast['expression']
        }
    elif ast['type'] == 'function_call':
        ident = ast['fn_name']
        if ident not in env:
            raise TypeError("Function {} not defined".format(ident))
        env_val = env[ident]
        if type(env_val) != dict:
            raise TypeError("Variable {} is not callable".format(ident))
        if len(ast['args']) != env_val['num_args']:
            raise TypeError("Function {} expects {} arguments, got {}"
                            .format(ident, env_val['num_args'], len(ast['args'])))
        subenv = Environment(initial_val=env)
        for argument, binding in zip(ast['args'], env_val['args']):
            if argument['type'] == 'identifier':
                value = env.get(argument['value'])
                if value is None:
                    raise TypeError("Identifier {} referenced before assignment"
                                    .format(argument['value']))
            elif argument['type'] == 'expression' or argument['type'] == 'function_call':
                value = evaluate(argument, env)
            else:
                value = argument['value']
            subenv[binding] = value
        return evaluate(env_val['expression'], subenv)
    

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
                try:
                    evaluate(ast, env)
                except TypeError as e:
                    print "Runtime error: {}".format(e)

def script_eval(str_prog):
    env = Environment()
    ast = lex_and_parse(str_prog)
    evaluate(ast, env)
                        
def main():
    if len(sys.argv) not in [1, 2]:
        print "Usage: calc.py [filename]"
        sys.exit(1)
    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r') as f:
                script_eval(f.read())
        except IOError as e:
            print "Error: {}".format(e)
            sys.exit(1)
    else:
        print "Reverse Polish Calculator, by Sean Gillespie"
        print "now powered by lex and yacc!"
        print "Control-D to exit"
        repl()
        print ""
        print "Bye!"
        
if __name__ == '__main__':
    main()
