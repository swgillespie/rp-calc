## Reverse Polish Calculator

This project is a tiny little calculator with vague reverse Lisp-like syntax. It supports six binary operations: addition, subtraction, multiplication, division,
exponentiation, and modulo. Unlike many Reverse Polish calculators, this calculator is not stack-based; the input is tokenized and parsed into an abstract
syntax tree, which is then evaulated and printed.

For example,
```
>> (29 9 +)
38
>> ((19 18 *) (44 32 +) +)
418
```

This calculator is governed by a simple grammar:
```
expression -> (<expression> <expression> <operator>)
            | <number>

number     -> [\d+]
operator   -> +, -, / *, ^, %
```
Tokens are built into an abstract syntax tree by recursive descent parsing. 

### Running instructions
To run the calculator, clone this repo
```
git clone https://github.com/swgillespie/rp-calc.git
```
Then, 
```
python calc.py
```
will start the read-eval-print loop. This program was written under Python 2.7 and will most likely
throw syntax errors in Python 3.

### Viewing the AST
If you're so inclined, you can import calc as a module instead to play with the helper functions:
```
>>> import calc, pprint
>>> tokens = calc.tokenize('((29 9 -) 4 +)')
>>> tokens
['(', '(', '29', '9', '-', ')', '4', '+', ')']
>>> ast = calc.parse(tokens)
>>> pprint.pprint(ast)
{'operand1': {'operand1': {'type': 'number', 'value': 29},
              'operand2': {'type': 'number', 'value': 9},
              'operator': '-',
              'type': 'expression'},
 'operand2': {'type': 'number', 'value': 4},
 'operator': '+',
 'type': 'expression'}
>>> calc.evaluate(ast)
24
```

This project is my first in what is hopefully a series of projects for me where I will attempt to build a compiler.
I will be working through a book over the next few months. Stay tuned if you are interested!