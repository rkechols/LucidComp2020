import string
from abc import ABC
from enum import Enum, auto
from typing import Dict, List


INT_SIZE = 256


class TokenType(Enum):
    EXT = auto()
    SET = auto()
    ADD = auto()
    JMP = auto()
    OUT = auto()
    ZERO = auto()
    ONE = auto()
    AMPERSAND = auto()
    DASH = auto()
    DIGIT_NON_BINARY = auto()
    WHITESPACE = auto()


class Token:
    def __init__(self, t: TokenType, value: str):
        self.t = t
        self.value = value

    def __str__(self) -> str:
        return f"({self.t.name},\"{self.value}\")"

    def __repr__(self) -> str:
        return self.__str__()


def tokenize(in_line: str) -> List[Token]:
    i = 0
    tokens = list()
    while i < len(in_line):
        c = in_line[i]
        if c in string.whitespace:
            start_i = i
            i += 1
            if i < len(in_line) and in_line[i] in string.whitespace:
                i += 1
            tokens.append(Token(TokenType.WHITESPACE, in_line[start_i:i]))
            continue
        elif c == "E":
            if in_line[i:(i + 3)] != "EXT":
                raise ValueError("Tokenizing Error: saw 'E' but was not 'EXT'")
            i += 3
            tokens.append(Token(TokenType.EXT, "EXT"))
            continue
        elif c == "S":
            if in_line[i:(i + 3)] != "SET":
                raise ValueError("Tokenizing Error: saw 'S' but was not 'SET'")
            i += 3
            tokens.append(Token(TokenType.SET, "SET"))
            continue
        elif c == "A":
            if in_line[i:(i + 3)] != "ADD":
                raise ValueError("Tokenizing Error: saw 'A' but was not 'ADD'")
            i += 3
            tokens.append(Token(TokenType.ADD, "ADD"))
            continue
        elif c == "J":
            if in_line[i:(i + 3)] != "JMP":
                raise ValueError("Tokenizing Error: saw 'J' but was not 'JMP'")
            i += 3
            tokens.append(Token(TokenType.JMP, "JMP"))
            continue
        elif c == "O":
            if in_line[i:(i + 3)] != "OUT":
                raise ValueError("Tokenizing Error: saw 'O' but was not 'OUT'")
            i += 3
            tokens.append(Token(TokenType.OUT, "OUT"))
            continue
        elif c == "0":
            i += 1
            tokens.append(Token(TokenType.ZERO, "0"))
            continue
        elif c == "1":
            i += 1
            tokens.append(Token(TokenType.ONE, "1"))
            continue
        elif c in string.digits:
            i += 1
            tokens.append(Token(TokenType.DIGIT_NON_BINARY, c))
            continue
        elif c == "&":
            i += 1
            tokens.append(Token(TokenType.AMPERSAND, "&"))
            continue
        elif c == "-":
            i += 1
            tokens.append(Token(TokenType.DASH, "-"))
            continue
    return tokens


class LittleInt:
    def __init__(self, i: int):
        self.value = i
        while self.value < INT_SIZE / -2:
            self.value += INT_SIZE
        while self.value >= INT_SIZE / 2:
            self.value -= INT_SIZE

    def __add__(self, other):
        if isinstance(other, LittleInt):
            return LittleInt(self.value + other.value)
        else:
            return LittleInt(self.value + other)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()


def evaluate_value(address_table: Dict[int, LittleInt], v: str) -> int:
    if v[0] == "&":
        address_num = evaluate_value(address_table, v[1:])
        return address_table[address_num].value
    else:
        return int(v)


class Command(ABC):
    pass


class SetCommand(Command):
    def __init__(self, receiving_address: str, value: str):
        if receiving_address[0] != "&":
            raise ValueError("Attempted to build SetCommand with a non-address value as first argument")
        self.receiving_address = receiving_address[1:]
        self.value = value


class AddCommand(Command):
    def __init__(self, receiving_address: str, value: str):
        if receiving_address[0] != "&":
            raise ValueError("Attempted to build AddCommand with a non-address value as first argument")
        self.receiving_address = receiving_address[1:]
        self.value = value


class JmpCommand(Command):
    def __init__(self, first_value: str, second_value: str):
        self.first_value = first_value
        self.second_value = second_value


class OutCommand(Command):
    def __init__(self, value: str, bit: bool):
        self.value = value
        self.bit = bit


class ExtCommand(Command):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0

    def match(self, t: TokenType) -> str:
        if self.tokens[self.index].t != t:
            raise ValueError(f"Match failed! Expected {t.name} but got {self.tokens[self.index].t.name}")
        to_return = self.tokens[self.index].value
        self.index += 1
        return to_return

    def skip_whitespace(self):
        while self.index < len(self.tokens) and self.tokens[self.index].t == TokenType.WHITESPACE:
            self.index += 1

    def parse_address(self) -> str:
        self.match(TokenType.AMPERSAND)
        v = self.parse_value()
        return "&" + v

    def parse_digit(self) -> str:
        if self.tokens[self.index].t == TokenType.ZERO:
            return self.match(TokenType.ZERO)
        elif self.tokens[self.index].t == TokenType.ONE:
            return self.match(TokenType.ONE)
        elif self.tokens[self.index].t == TokenType.DIGIT_NON_BINARY:
            return self.match(TokenType.DIGIT_NON_BINARY)
        else:
            raise ValueError(f"Parse digit failed! Got type {self.tokens[self.index].t.name}")

    def parse_num(self) -> str:
        token_values = list()
        if self.tokens[self.index].t == TokenType.DASH:
            token_values.append(self.match(TokenType.DASH))
        token_values.append(self.parse_digit())
        while self.index < len(self.tokens) and self.tokens[self.index].t in [TokenType.ZERO, TokenType.ONE, TokenType.DIGIT_NON_BINARY]:
            token_values.append(self.parse_digit())
        return "".join(token_values)

    def parse_value(self) -> str:
        if self.tokens[self.index].t == TokenType.AMPERSAND:
            return self.parse_address()
        else:
            return self.parse_num()

    def parse_bit(self) -> bool:
        if self.tokens[self.index].t == TokenType.ZERO:
            self.match(TokenType.ZERO)
            return False
        elif self.tokens[self.index].t == TokenType.ONE:
            self.match(TokenType.ONE)
            return True
        else:
            raise ValueError(f"Parsing bit failed! Got token type {self.tokens[self.index].t.name}")

    def parse_set_command(self) -> SetCommand:
        self.match(TokenType.SET)
        self.skip_whitespace()
        a = self.parse_address()
        self.skip_whitespace()
        v = self.parse_value()
        self.skip_whitespace()
        return SetCommand(a, v)

    def parse_add_command(self) -> AddCommand:
        self.match(TokenType.ADD)
        self.skip_whitespace()
        a = self.parse_address()
        self.skip_whitespace()
        v = self.parse_value()
        self.skip_whitespace()
        return AddCommand(a, v)

    def parse_jmp_command(self) -> JmpCommand:
        self.match(TokenType.JMP)
        self.skip_whitespace()
        v1 = self.parse_value()
        self.skip_whitespace()
        v2 = self.parse_value()
        self.skip_whitespace()
        return JmpCommand(v1, v2)

    def parse_out_command(self) -> OutCommand:
        self.match(TokenType.OUT)
        self.skip_whitespace()
        v = self.parse_value()
        self.skip_whitespace()
        b = self.parse_bit()
        self.skip_whitespace()
        return OutCommand(v, b)

    def parse_command(self) -> Command:
        self.index = 0
        self.skip_whitespace()
        if self.tokens[self.index].t == TokenType.EXT:
            return ExtCommand()
        elif self.tokens[self.index].t == TokenType.SET:
            return self.parse_set_command()
        elif self.tokens[self.index].t == TokenType.ADD:
            return self.parse_add_command()
        elif self.tokens[self.index].t == TokenType.JMP:
            return self.parse_jmp_command()
        elif self.tokens[self.index].t == TokenType.OUT:
            return self.parse_out_command()
        else:
            raise ValueError(f"First token of a command (after whitespace) was not valid: {self.tokens[self.index].t.name}")


class Interpreter:
    def __init__(self, command_list: List[Command]):
        self.command_list = command_list
        self.address_table: Dict[int, LittleInt] = dict()
        self.set_next_to_execute(0)
    
    def set_next_to_execute(self, i: int):
        self.address_table[0] = LittleInt(i)
    
    def get_next_to_execute(self) -> int:
        return self.address_table[0].value
    
    def increment_next_to_execute(self):
        self.set_next_to_execute(self.get_next_to_execute() + 1)

    def execute_next(self):
        command = self.command_list[self.get_next_to_execute()]
        self.increment_next_to_execute()
        # SET
        if isinstance(command, SetCommand):
            receiving_address_int = evaluate_value(self.address_table, command.receiving_address)
            value_to_set = evaluate_value(self.address_table, command.value)
            self.address_table[receiving_address_int] = LittleInt(value_to_set)
        # ADD
        elif isinstance(command, AddCommand):
            address_to_change = evaluate_value(self.address_table, command.receiving_address)
            first_num = evaluate_value(self.address_table, "&" + command.receiving_address)
            second_num = evaluate_value(self.address_table, command.value)
            self.address_table[address_to_change] = LittleInt(first_num + second_num)
        # JMP
        elif isinstance(command, JmpCommand):
            if evaluate_value(self.address_table, command.first_value) == 0:
                line_to_evaluate = evaluate_value(self.address_table, command.second_value)
                self.set_next_to_execute(line_to_evaluate)
        # OUT
        elif isinstance(command, OutCommand):
            to_print = evaluate_value(self.address_table, command.value)
            if command.bit:  # just a digit
                print(to_print, end="")
            else:  # ASCII
                print(chr(to_print), end="")
        # EXT
        elif isinstance(command, ExtCommand):
            exit()
        # unknown
        else:
            raise ValueError(f"Interpreter did not recognize command of class {command.__class__.__name__}")

    def run(self):
        self.set_next_to_execute(0)
        while True:
            self.execute_next()


if __name__ == "__main__":
    n_lines = int(input())
    commands = list()
    for _ in range(n_lines):
        tokens_list = tokenize(input())
        parser = Parser(tokens_list)
        command_ = parser.parse_command()
        commands.append(command_)
    interpreter = Interpreter(commands)
    interpreter.run()
