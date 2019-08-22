%{

#include <stdio.h>

int    yylex(void);
void   yyerror(const char *);
FILE * yyin;

%}

%token INSTR_MOV INSTR_ADD INSTR_INC INSTR_JMP
%token REG_EAX REG_EBX REG_ECX REG_EDX
%token IDENTIFIER NUMBER COMMA COLON SEMICOLON

%start program

%%

register_name
   : REG_EAX
   | REG_EBX
   | REG_ECX
   | REG_EDX
   ;

label
   : IDENTIFIER COLON
   ;

instruction_mov
   : INSTR_MOV register_name COMMA register_name SEMICOLON
   | INSTR_MOV register_name COMMA NUMBER SEMICOLON
   ;

instruction_add
   : INSTR_ADD register_name COMMA register_name COMMA register_name SEMICOLON
   | INSTR_ADD register_name COMMA register_name COMMA NUMBER SEMICOLON
   ;

instruction_inc
   : INSTR_INC register_name SEMICOLON
   ;

instruction_jmp
   : INSTR_JMP IDENTIFIER SEMICOLON
   ;

instruction
   : instruction_mov
   | instruction_add
   | instruction_inc
   | instruction_jmp
   ;

program
   : instruction
   | label
   | program instruction
   | program label
   ;

%%

void yyerror(const char * message)
{
   printf(message);
}

int main(int argc, char **argv)
{
   if(argc == 2)
   {
      if((yyin = fopen(argv[1], "rb")) != NULL)
      {
         yyparse();
         fclose(yyin);
      }
   }

   return 0;
}