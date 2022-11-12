from lark import Lark, Transformer


@dataclass
class Expression:
    expression: Union[LiteralInt, LiteralFloat, FunctionCall, VariableUsage, Operation]


loqinkee_grammar = r"""
    text : /.*?/

    literal_float : SIGNED_FLOAT
    literal_int : SIGNED_INT
    identifier : CNAME

    plus : "+"
    minus : "-"
    mult : "*"
    div : "/"

    function_call : expression "(" [expression ("," expression)*] ")"

    add_expression : expression plus factor
    sub_expression : expression minus factor
    mult_expression : expression mult term
    div_expression : expression div term

    variable_usage : identifier

    expression : add_expression
           | sub_expression
           | factor

    factor : mult_expression
           | div_expression
           | term

    term : literal_int
         | literal_float
         | variable_usage
         | function_call
         | "(" expression ")"

    print : "{{" expression "}}"
    for_loop : "{%" "for" assignment "in" expression "%}" template "{%" "endfor" "%}"
    if_statement : "{%" "if" expression "%}" template "{%" "endif" "%}"

    variable_usage : identifier

    expression : variable_usage

    not : "not" expression

    assignment : identifier

    template_item : print
                  | for_loop
                  | if_statement
                  | text

    template : (template_item)*
"""

class TreeToLoqinkee(Transformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def identifier(self, i) -> str:
        (i,) = i
        return str(i)

    def text(self, i) -> str:
        (i,) = i
        return str(i)
