import string
try:
    import readline
except ImportError:
    pass
    
class SyntaxError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def tokenize(string_in):
    tokens = []
    stack = []
    for char in string_in:
        if char in string.whitespace:
            if stack == []:
                pass
            else:
                token = ''.join(stack)
                tokens.append(token)
                stack = []
        elif char in ['(', ')', '+', '-', '*', '/', '^', '%']:
            tokens.append(char)
        elif char in string.digits:
            stack.append(char)
        else:
            raise SyntaxError("Character not allowed: {}".format(char))
    if len(stack) != 0:
        raise SyntaxError("Unexpected EOF while parsing, number stack not empty")
    return tokens

def parse(tokens):
    return expression(tokens)
    
def expression(tokens):
    ast = {
        'type': 'expression',
        'operand1': None,
        'operand2': None,
        'operator': None
    }
    token = tokens.pop(0)
    if token != '(':
        raise SyntaxError('Invalid Start of Expression; Expected {}, Got {}'.format('(', token))
    for i in range(4):
        token = tokens.pop(0)
        if i == 3:
            if token != ')':
                raise SyntaxError('Expected {}, got {}'.format(')', token))
        elif i == 2:
            if token not in ['+', '-', '*', '/', '^', '%']:
                raise SyntaxError("Expected operand, got {}".format(token))
            ast['operator'] = token
        elif token not in ['(', ')', '+', '-', '*', '/', '^', '%']:
            tokens.insert(0, token)
            ast['operand{}'.format(i + 1)] = number(tokens)
        elif token == '(':
            tokens.insert(0, token)
            ast['operand{}'.format(i + 1)] = expression(tokens)
        else:
            raise SyntaxError('Invalid operand: expected an expression, got symbol {}'.format(token))
    return ast

def number(tokens):
    try:
        str2int = int(tokens.pop(0))
    except Exception as e:
        raise SyntaxError('Token cast to int failed: {}'.format(e))
    else:
        return {
            'type': 'number',
            'value': str2int
        }

def evaluate(ast):
    if ast['type'] == 'number':
        return ast['value']
    elif ast['type'] == 'expression':
        op1 = evaluate(ast['operand1'])
        op2 = evaluate(ast['operand2'])
        op_func = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '/': lambda x, y: x / float(y),
            '*': lambda x, y: x * y,
            '^': lambda x, y: x ** y,
            '%': lambda x, y: x % y
        }.get(ast['operator'])
        return op_func(op1, op2)

def repl(prompt=">> "):
    running = True
    while running:
        try:
            input = raw_input(prompt)
        except EOFError:
            # control-D was pressed
            running = False
        else:
            try:
                if input == '':
                    continue
                tokens = tokenize(input)
                ast = parse(tokens)
            except SyntaxError as e:
                print "SyntaxError: {}".format(e)
                continue
            print evaluate(ast)
    print "\nBye!"

def main():
    print "Reverse Polish Calculator, by Sean Gillespie"
    print "Control-D to exit"
    repl()

if __name__ == '__main__':
    main()