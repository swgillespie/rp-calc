## rp-calc - A small Lisp-esque calculator language

This project is a tiny little calculator with vague reverse Lisp-like syntax. It supports six binary operations: addition, subtraction, multiplication, division,
exponentiation, and modulo. It also supports the definition and reference of variables. Unlike many Reverse Polish calculators, this calculator is not stack-based; the input is tokenized and parsed into an abstract
syntax tree, which is then evaulated and printed.

For example,
```
>> (let x (* 238 (+ 3727 3828 )))
>> x
1798090
>> (let y 88)
>> y
88
>> (/ x y)
20432
```

It also can do floating point calculations...
```
>> (* 28.3938 25773.328)
731802.720566
>> (/ 100 2.0)
50.0
>> (/ 100 3.0)
33.3333333333
```
...and define functions
```
>> (defun square (x) (^ x 2))
>> (square 9)
81
```

Also, thanks to the wonderful thing that is yacc, the grammar is self documenting in parser.py.

### Running instructions
This project requires GNU bison and flex. Bison and flex come with Xcode's command line tools on Mac OS 
X, and may or may not come with Linux depending on your distro.

To run the calculator, clone this repo
```
git clone https://github.com/swgillespie/rp-calc.git
```
Then, 
```
pip install ply
python calc.py
```
will start the read-eval-print loop. This program was written under Python 2.7 and will most likely
throw syntax errors in Python 3.

This project is my first in what is hopefully a series of projects for me where I will attempt to build a compiler.
I will be working through a book over the next few months. Stay tuned if you are interested!
