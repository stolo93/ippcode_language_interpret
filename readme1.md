Documentation of Project Implementation for IPP 2022/2023
Name and surname: Samuel Stolarik
Login: xstola03

## Usage

The program parse.php expects a IPPcode23 source code and proceeds with lexical and syntactic analysis. 
If the source program given is syntactically correct it will be printed to standard output in XML form as described bellow.

To print help message run:
> php8.1 parse.php --help

To perform syntactic analysis and convert IPPcode23 source code to XML run:
> php8.1 parse.php --source source_code

or
> php8.1 parse.php

To read the source code from standard input

### Output XML description

The final XML which is printed to standard output consists of a header and root element `program`, 
which then aggregates each given instruction as a child element and uses element attributes to store
instruction parameters.

##### Example

IPPcode23 source code:
```
DEFVAR GF@counter
MOVE GF@counter string@
LABEL while
JUMPIFEQ end GF@counter string@aaa
WRITE string@\010
CONCAT GF@counter GF@counter string@a
JUMP while
LABEL end
```

XML representation:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode23">
    <instruction order="1" opcode="DEFVAR">
        <arg1 type="var">GF@counter</arg1>
    </instruction>
    <instruction order="2" opcode="MOVE">
        <arg1 type="var">GF@counter</arg1>
        <arg2 type="string"/>
    </instruction>
    <instruction order="3" opcode="LABEL">
        <arg1 type="label">while</arg1>
    </instruction>
    <instruction order="4" opcode="JUMPIFEQ">
        <arg1 type="label">end</arg1>
        <arg2 type="var">GF@counter</arg2>
        <arg3 type="string">aaa</arg3>
    </instruction>
    <instruction order="5" opcode="WRITE">
        <arg1 type="string">\010</arg1>
    </instruction>
    <instruction order="6" opcode="CONCAT">
        <arg1 type="var">GF@counter</arg1>
        <arg2 type="var">GF@counter</arg2>
        <arg3 type="string">a</arg3>
    </instruction>
    <instruction order="7" opcode="JUMP">
        <arg1 type="label">while</arg1>
    </instruction>
    <instruction order="8" opcode="LABEL">
        <arg1 type="label">end</arg1>
    </instruction>
</program>
```

## Implementation

Program parse.php is implemented in `php 8.1` and uses `SimpleXML` and `DOM` libraries.

## Syntactic and lexical analysis

Syntactic analysis is implemented using a `switch-case` statement which chooses the correct grammar rule based on the instruction given and then performs lexical analysis of the parameters expected.

### Syntactic analysis
In the implementation, inside the `switch-case` we merged all grammar rules which generate the same string.

[//]: # (Next part is taken from the assignment. However, in my opinion it makes sense to state the grammar rules in the documentation)
#### Grammar rules
`<program> -> .IPPcode23 <statement>`\
`<statement> -> <statement> <statement>`\
`<statement> -> ""`\
`<statemenst> -> MOVE ⟨var⟩ ⟨symb⟩`\
`<statemenst> -> CREATEFRAME`\
`<statemenst> -> PUSHFRAME`\
`<statemenst> -> POPFRAME`\
`<statemenst> -> DEFVAR <var>`\
`<statemenst> -> CALL <label>`\
`<statemenst> -> RETURN`\
`<statemenst> -> PUSHS <symb>`\
`<statemenst> -> POPS <var>`\
`<statemenst> -> ADD|SUB|MUL|DIV|IDIV <var> <symb> <symb>`\
`<statemenst> -> LT|GT|EQ <var> <symb> <symb>`\
`<statemenst> -> AND|OR|NOT <var> <symb> <symb>`\
`<statemenst> -> INT2CHAR <var> <symb>`\
`<statemenst> -> STRI2INT <var> <symb> <symb>`\
`<statemenst> -> READ <var> <type>`\
`<statemenst> -> WRITE <symb>`\
`<statemenst> -> CONCAT <var> <symb> <symb>`\
`<statemenst> -> STRLEN <var> <symb>`\
`<statemenst> -> GETCHAR <var> <symb> <symb>`\
`<statemenst> -> SETCHAR <var> <symb> <symb>`\
`<statemenst> -> TYPE <var> <symb>`\
`<statemenst> -> LABEL <label>`\
`<statemenst> -> JUMB <label>`\
`<statemenst> -> JUMPIFEQ <label> <symb> <symb>`\
`<statemenst> -> JUMPIFNEQ <label> <symb> <symb>`\
`<statemenst> -> EXIT <symb>`\
`<statemenst> -> DPRING <symb>`\
`<statemenst> -> BREAK`

### Lexical analysis

Lexical analysis is implemented using `string comparison` and `regular expression matching`.

#### Instructions
Lexical analysis of instructions is implemented using a simple string comparison as we know the full domain of available instructions.

#### Variables
For variables, firstly the frame and name are separated using the first found '@' symbol and than regex matching is performed with both.

For frame matching:
```regexp
/^((gf)|(lf)|(tf))$/i
```
and for variable names:
```regexp
/^[_,\-,$,&,%,*,!,?,a-z,A-Z][_,\-,$,&,%,*,!,?,a-z,A-Z,0-9]*$/
```

#### Labels
Labels are also matched with regular expression, as shown bellow.
```regexp
/^[_,\-,$,&,%,*,!,?,a-z,A-Z][_,\-,$,&,%,*,!,?,a-z,A-Z,0-9]*$/
```

#### Symbols

For lexical analysis of symbols we first try to match the symbol with the regular expressions used for variables (as symbol might also be a variable). If that is not the case we perform following:

Firstly, type is separated based on the position of '@' symbol, later we analyse the symbol name based on the type acquired, again deciding using a `switch-case` statement.

##### int
For integers, we check four types:
* decimal
* hexadecimal
* octal
* binary

all combined into one regular expression:
```regexp
/^(([+,-]{0,1}[1-9][0-9]*(_[0-9]+)*|0)|(0[xX][0-9a-fA-F]+(_[0-9a-fA-F]+)*)|(0[oO]?[0-7]+(_[0-7]+)*)|(0[bB][01]+(_[01]+)*))$/
```

##### bool
Symbol of type bool can be either true or false, therefore the regular expression is simple
```regexp
/^((true)|(false))$/i
```

#### string
A string in IPPcode23 must not contain '\' and '#'. Hashtags are already taken care of because they are deleted while removing comments. For backslashes, however we find every occurrence and try to match it and next three symbols against this simple escape sequence regular expression.
```regexp
/^\\\\\d{3}$/
```
which matches one backslash and three numbers.

## XML generator

For generating the output XML we use `SimpleXML` with `<program>` as the root element to which we add instructions as sub elements with parameters as their attributes.

Lastly, for printing formatted XML we use `DOMDocument` object and its `formatOutput` attribute.

See:

[SimpleXML](https://www.php.net/manual/en/book.simplexml.php)

[DOM](https://www.php.net/manual/en/book.dom.php)
