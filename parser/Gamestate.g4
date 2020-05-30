// Define a grammar called Hello
grammar Gamestate;

configfile : assignment* ;

assignment : key=expression '=' value=expression ;

expression
    : STRING
    | ATOM
    | '{' (key=expression ('=' value=expression)?)* '}'
    ;

STRING : '"' (~["\\]+ ('\\' .)?)* '"' ;
ATOM : [-a-zA-Z0-9_.:]+ ;
WS : [ \t\r\n]+ -> skip ;