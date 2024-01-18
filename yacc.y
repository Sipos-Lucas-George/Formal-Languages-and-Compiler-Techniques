%{
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yylineno;
extern char* yytext;

void yyerror(const char *s) {
    fprintf(stderr, "Error at line %d: %s\n", yylineno, s);
}

%}

%token IDENTIFIER INT_CONST STRING_CONST
%token PLUS MINUS MULTIPLY DIVIDE MODULO
%token ASSIGN EQ LT GT LE GE
%token LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET COMMA SEMICOLON
%token INT STRING READ WRITE IF ELIF ELSE FOR EXIT MAX

%%
/* Production rules */

program
    : composed_stmt
    ;

composed_stmt
    : statement
    | statement composed_stmt
    ;

statement
    : declaration
    | assign_stmt
    | io_stmt
    | if_stmt
    | for_stmt
    | exit_stmt
    ;

declaration
    : type IDENTIFIER SEMICOLON
    | type array SEMICOLON
    ;

array
    : IDENTIFIER LBRACKET INT_CONST RBRACKET
    ;

assign_stmt
    : IDENTIFIER ASSIGN expression SEMICOLON
    ;

io_stmt
    : read_stmt
    | write_stmt
    ;

read_stmt
    : READ LPAREN seq_read RPAREN SEMICOLON
    ;

write_stmt
    : WRITE LPAREN seq_write RPAREN SEMICOLON
    ;

seq_read
    : IDENTIFIER
    | array
    | IDENTIFIER COMMA seq_read
    | array COMMA seq_read
    ;

seq_write
    : seq_read
    | seq_expression
    ;

seq_expression
    : expression
    | expression COMMA seq_expression
    ;

expression
    : INT_CONST
    | STRING_CONST
    | array_index
    | max_expression
    ;

array_index
    : IDENTIFIER LBRACKET INT_CONST RBRACKET
    ;

max_expression
    : MAX LPAREN expression COMMA expression RPAREN
    ;

if_stmt
    : IF LPAREN condition RPAREN LBRACE composed_stmt RBRACE
    | IF LPAREN condition RPAREN LBRACE composed_stmt RBRACE elif_stmt
    | IF LPAREN condition RPAREN LBRACE composed_stmt RBRACE ELSE LBRACE composed_stmt RBRACE
    ;

elif_stmt
    : ELIF LPAREN condition RPAREN LBRACE composed_stmt RBRACE
    | ELIF LPAREN condition RPAREN LBRACE composed_stmt RBRACE elif_stmt
    ;

for_stmt
    : FOR LPAREN IDENTIFIER ASSIGN INT_CONST SEMICOLON IDENTIFIER comparison INT_CONST SEMICOLON IDENTIFIER ASSIGN INT_CONST RPAREN LBRACE composed_stmt RBRACE
    ;

exit_stmt
    : EXIT LPAREN INT_CONST RPAREN SEMICOLON
    ;

condition
    : expression comparison expression
    ;

comparison
    : EQ
    | LT
    | GT
    | LE
    | GE
    ;

type
    : INT
    | STRING
    ;

%%

//int main() {
//    printf("Starting the parser...\n");
//    if (yyparse() == 0) {
//        printf("Parsing complete!\n");
//    } else {
//        printf("Parsing failed.\n");
//   }
//   return 0;
//}

