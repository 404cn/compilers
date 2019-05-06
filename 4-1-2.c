/* 
G[statements]:
statements->expression; statments | 空
experssion->term expression'
expression'->+term expression' | 空
term->factor term'
term'->*factor term' | 空
factor->num_or_id | (expression)
*/

#include <stdio.h>

statments()
{
    expression();

    if (match(";"))
    {
        advance();
    }
    else
    {
        fprintf(stderr, "%d: Inserting missing semicolon\n", yylineno);
    }

    if (!match(EOI))
    {
        statements();
    }
}

expression()
{
    term();
    expr_prime();
}

expr_prime()
{
    if (match("+"))
    {
        advance();
        term();
        expr_prime();
    }
}

term()
{
    factor();
    term_prime();
}

term_prime()
{
    if (match("*"))
    {
        advance();
        factor();
        term_prime();
    }
}

factor()
{
    // NUM_OR_ID: 运算对象
    if (match(NUM_OR_ID))
    {
        advance();
    }
    else if(match("("))
    {
        advance();
        expression();
        if (match(")"))
        {
            advance();
        }
        else
        {
            fprintf(stderr, "%d: Mismatched parentesis\n", yylineno);
        }
    }
    else
    {
        fprintf(stderr, "%d: Number or identifier expected\n", yylineno);
    }
}

