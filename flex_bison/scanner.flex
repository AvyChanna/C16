%{

#include "parser.h"

%}

%option noyywrap
%option pointer

CT       "//"[^\n]*
WS       [ \n\r\t]+
ID       [_a-zA-Z][_a-zA-Z0-9]*
NUM      [0-9]+

%%

{CT}     {}
{WS}     {}

"mov"    { return INSTR_MOV; }
"add"    { return INSTR_ADD; }
"inc"    { return INSTR_INC; }
"jmp"    { return INSTR_JMP; }

"eax"    { return REG_EAX; }
"ebx"    { return REG_EBX; }
"ecx"    { return REG_ECX; }
"edx"    { return REG_EDX; }

{ID}     { return IDENTIFIER; }
{NUM}    { return NUMBER; }

","      { return COMMA; }
":"      { return COLON; }
";"      { return SEMICOLON; }

.        { yyerror("syntax error"); }