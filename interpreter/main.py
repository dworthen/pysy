# Tokens types
from typing import cast


INTEGER, PLUS, EOF = "INTEGER", "PLUS", "EOF"


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

    def error(self) -> None:
        raise Exception("Error paarsing input")

    def __is_end_of_file(self) -> bool:
        return self.pos >= len(self.text)

    def get_next_token(self) -> Token | None:
        """Lexical analyzer/tokenizer

        This method is responsible for breaking a asentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # End of the file?
        if self.__is_end_of_file():
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == "+":
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()
        return None

    def eat(self, token_type: str) -> None:
        # Compare the current token type with the passed token
        # type and if they match then "eat" the curren token
        # and assign the next token to the self.current_token
        if self.current_token is not None and self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self) -> int:
        """expr -> INTEGER PLUS INTEGER"""
        # set the current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single digit integer
        left = self.current_token
        assert left is not None
        self.eat(INTEGER)

        # The next token should be a '+' token
        self.eat(PLUS)

        # The last token should be a single digit integer
        right = self.current_token
        assert right is not None
        self.eat(INTEGER)

        result = cast(int, left.value) + cast(int, right.value)
        return result


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
