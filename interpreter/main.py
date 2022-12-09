# Tokens types
from typing import cast


INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"


class Token(object):
    def __init__(self, type: str, value: str | int | None) -> None:
        # Token type
        self.type: str = type
        # Token value
        self.value: str | int | None = value

    def __str__(self) -> str:
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            TOKEN(PLUS, '+')
        """
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self) -> str:
        return self.__str__()


class Interpretor(object):
    def __init__(self, text: str) -> None:
        # cleint string input, e.g., "3+5"
        self.text: str = text
        # current index of scanning self.text
        self.pos: int = 0
        # Current token instance
        self.current_token: Token | None = None
        self.current_char: str | None = self.text[self.pos]

    def error(self) -> None:
        raise Exception("Error paarsing input")

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token | None:
        """Lexical analyzer/tokenizer

        This method is responsible for breaking a asentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            self.error()
        return Token(EOF, None)

    def eat(self, token_type: str) -> None:
        # Compare the current token type with the passed token
        # type and if they match then "eat" the curren token
        # and assign the next token to the self.current_token
        if self.current_token is not None and self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self) -> int:
        """Parser/Interpreter

        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        # set the current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single digit integer
        left = self.current_token
        assert left is not None
        self.eat(INTEGER)

        # The next token should be a '+' or '-' token
        op = self.current_token
        assert op is not None
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        # The last token should be a single digit integer
        right = self.current_token
        assert right is not None
        self.eat(INTEGER)

        left_digit = cast(int, left.value)
        right_digit = cast(int, right.value)
        if op.type == PLUS:
            return left_digit + right_digit
        else:
            return left_digit - right_digit


def main():
    while True:
        try:
            # Grab user input
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        interpretor = Interpretor(text)
        result = interpretor.expr()
        print(result)


if __name__ == "__main__":
    main()
