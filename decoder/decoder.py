from decoder.methods.recursive_descent import RecursiveDescent
from decoder.methods.operator_precedence import OperatorPrecedence
import numpy as np
class Decoder:
    lexemes = [
        "if",
        "THEN",
        "MOD",
        "DIV",
        "DIY",
        "*",
        ";",
        ":=",
        "=",
        "!=",
        "<",
        ">",
        "<=",
        ">=",
        "+",
        "-",
        "(",
        ")",
        "begin",
        "end",
        "var",
        ",",
        ":",
        "integer",
        "real"
    ]

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path

        self.wasCut = False
        self.buf = ""
        self.isLexeme = True
        self.isConst = True
        self.isIdent = True

        self.lexemesMap = {}
        for i, lexeme in enumerate(self.lexemes):
            self.lexemesMap[lexeme] = i + 2

        self.identifiers_map = {}

        self.ident_start_index = -1
        self.identifiers_matrix_cursor = -1
        self.identifiers_matrix = []
        self.hash_matrix = {}

        self.parseLexemes = []

    def set_input(self, path: str) -> None:
        self.input_path = path

    def set_output(self, path: str) -> None:
        self.output_path = path

    def hash_func(self, ident: str) -> int:
        return sum([ord(i) for i in ident])

    def cut(self) -> None:
        self.wasCut = True
        self.buf = self.buf[-1]
        self.isLexeme = True
        self.isConst = True
        self.isIdent = True

    def show_maps(self) -> None:
        print("Identifier: 0")
        print("Constant: 1")
        print(f"Lexemes: {self.lexemesMap}")
        print("Identifiers:")
        print(self.hash_matrix)
        print(np.array(self.identifiers_matrix))


    def is_lexeme(self) -> None:
        curLexeme = ""
        for lex in self.lexemes:
            if self.buf in lex:
                curLexeme = lex
                if self.buf == lex:
                    self.lexeme = lex
                # break
        if curLexeme == "":
            self.isLexeme = False

    def is_const(self) -> None:
        if self.buf.isdigit():
            self.const = self.buf
        else:
            self.isConst = False

    def is_ident(self) -> None:
        if not self.buf[0].isdigit():
            for c in [",", ".", ":", ";", "-", "=", "?", "!", "*", " ", "\n"]:
                if self.buf[-1] == c:
                    self.isIdent = False
                    break
        else:
            self.isIdent = False
        if self.isIdent:
            self.ident = self.buf

    def add_ident(self, ident: str) -> None:
        h = self.hash_func(ident)
        self.identifiers_matrix_cursor += 1
        self.identifiers_matrix.append([ident, 0, 0])

        if self.ident_start_index == -1:
            self.ident_start_index = self.identifiers_matrix_cursor

        if h not in self.hash_matrix:
            self.hash_matrix[h] = self.identifiers_matrix_cursor
        else:
            index = self.hash_matrix[h]
            while self.identifiers_matrix[index][2] != 0:
                index = self.identifiers_matrix[index][2]
            self.identifiers_matrix[index][2] = self.identifiers_matrix_cursor

        if ident not in self.identifiers_map:
            self.identifiers_map[ident] = len(self.identifiers_map)

    def set_type_ident(self, type):
        for i in range(self.ident_start_index, len(self.identifiers_matrix)):
            self.identifiers_matrix[i][1] = type
        self.ident_start_index = -1

    def decode(self) -> None:
        with open(self.input_path, "r") as f:
            with open(self.output_path, "w") as f_output:
                self.buf = ""

                self.isLexeme = True
                self.isIdent = True
                self.isConst = True

                def reset():
                    self.lexeme = ""
                    self.const = ""
                    self.ident = ""
                reset()

                self.wasCut = False
                while True:
                    if not self.wasCut:
                        ch = f.read(1)
                        if not ch:
                            break
                        self.buf += ch

                    # Проверка на лексему
                    self.is_lexeme()
                    # Проверка на константу
                    self.is_const()
                    # Проверка на идентификатор
                    self.is_ident()

                    if not self.isLexeme and not self.isConst and not self.isIdent:
                        if self.buf == "\n":
                            f_output.write("\n")
                        # Лексема
                        if self.lexeme != "":
                            f_output.write(str(self.lexemesMap[self.lexeme]) + " ")
                            if self.lexeme in ['integer', 'real']:
                                self.set_type_ident(self.lexeme)
                            self.parseLexemes.append(self.lexemesMap[self.lexeme])
                            reset()
                            self.cut()
                        # Константа
                        elif self.const != "":
                            f_output.write(f"1[{self.const}] ")
                            self.parseLexemes.append([1, int(self.const)])
                            reset()
                            self.cut()
                        # Идентификатор
                        elif self.ident != "":
                            self.add_ident(self.ident)
                            f_output.write(f'0[{self.identifiers_map[self.ident]}] ')
                            self.parseLexemes.append([0, self.identifiers_map[self.ident]])
                            reset()
                            self.cut()
                        else:
                            if self.wasCut and len(self.buf) == 1:
                                self.wasCut = False
                            elif len(self.buf) > 1:
                                reset()
                                self.cut()
                    elif self.wasCut:
                        self.wasCut = False
        # self.parseLexemes.append(0)

    def recursive_descent(self) -> None:
        rec_des = RecursiveDescent(lexemes=self.parseLexemes, lexemesMap=self.lexemesMap, identifiersMap=self.identifiers_map)
        rec_des.disassemble()

    def operator_precedence(self) -> None:
        oper_prec = OperatorPrecedence(lexemes=self.parseLexemes, lexemesMap=self.lexemesMap, identifiersMap=self.identifiers_map)
        oper_prec.disassemble()