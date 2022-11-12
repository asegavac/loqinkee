from dataclasses import dataclass
import re
from typing import Dict, List, Any

VAR_TOKEN_START = "{{"
VAR_TOKEN_END = "}}"
BLOCK_TOKEN_START = "{%"
BLOCK_TOKEN_END = "%}"
TOK_REGEX = re.compile(
    r"(%s.*?%s|%s.*?%s)"
    % (VAR_TOKEN_START, VAR_TOKEN_END, BLOCK_TOKEN_START, BLOCK_TOKEN_END)
)


class LoqinkeeException(Exception):
    pass


class VariableDoesNotExistError(Exception):
    pass


class CannotRenderVariable(Exception):
    pass


def _resolve(path: List[str], context):
    if path[0].isnumeric():
        if not isinstance(context, list):
            raise VariableDoesNotExistError(f"cannot use number in path of non-list")
        if len(context) <= int(path[0]):
            raise VariableDoesNotExistError(f"number out of bounds")
        value = value = context[int(path[0])]
    else:
        if path[0] not in context:
            raise VariableDoesNotExistError(f"{path[0]} does not exist")
        value = context[path[0]]
    if len(path) == 1:
        if isinstance(value, int):
            return str(value)
        if isinstance(value, str):
            return value
        else:
            raise CannotRenderVariable("{path[0]} must be str or int")
    if isinstance(value, dict) or isinstance(value, list):
        return _resolve(path[1:], value)
    else:
        raise CannotRenderVariable("{path[0]} must be str or int")


@dataclass
class TextFragment:
    text: str

    def render(self, context):
        return self.text


@dataclass
class VariableFragment:
    contents: str

    def render(self, context: Dict):
        path = self.contents.split(".")
        try:
            return _resolve(path, context)
        except VariableDoesNotExistError:
            raise VariableDoesNotExistError(f"'{contents}' does not exist.")
        except CannotRenderVariable:
            raise CannotRenderVariable(
                f"Cannot render '{contents}', only strings and ints can be rendered."
            )


@dataclass
class BlockFragment:
    contents: str

    def render(self, context: Dict):
        raise NotImplementedError


def render(template: str, data: Any):
    tokens = TOK_REGEX.split(template)
    ast = []
    for token in tokens:
        if token.startswith(VAR_TOKEN_START):
            ast.append(VariableFragment(token[2:-2].strip()))
        elif token.startswith(BLOCK_TOKEN_START):
            ast.append(BlockFragment(token[2:-2]))
        else:
            ast.append(TextFragment(token))
    return "".join([fragment.render(data) for fragment in ast])
