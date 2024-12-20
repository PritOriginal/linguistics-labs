from typing import List


class RecursiveDescent:
    def __init__(self, lexemes: List, lexemesMap, identifiersMap):
        self.lexemes = lexemes
        self.lexemes.append(0)
        self.lexemesMap = lexemesMap
        self.identifiersMap = identifiersMap

        self.cursor = 0

    def disassemble(self):
        if self.operators_section():
            print(True)
        else:
            print(False)

    # <раздел операторов> -> <оператор> {; <оператор>}
    def operators_section(self) -> bool:
        succeeded = False
        if self.operator():
            while self.lexemes[self.cursor] == self.lexemesMap[";"]:
                print(self.lexemes[self.cursor])
                succeeded = True
                self.cursor += 1
                if not self.operator():
                    succeeded = False

        return succeeded

    # <оператор> -> <присваивание> / <условный оператор>
    def operator(self) -> bool:
        succeeded = False
        if self.assignment() or self.conditional_operator():
            succeeded = True
        return succeeded

    # <присваивание> -> ид := <арифмитическое выражение>
    def assignment(self) -> bool:
        succeeded = False
        if type(self.lexemes[self.cursor]) is list and self.lexemes[self.cursor][0] == 0:
            indent_id = self.lexemes[self.cursor][1]
            print(f"0 {indent_id}")
            self.cursor += 1
            if self.lexemes[self.cursor] == self.lexemesMap[":="]:
                print(self.lexemes[self.cursor])
                self.cursor += 1
                if self.arithmetic_expression():
                    succeeded = True
        return succeeded

    # <условный оператор> -> if <условное выражение> THEN <тело условия>
    def conditional_operator(self) -> bool:
        succeeded = False
        if self.lexemes[self.cursor] == self.lexemesMap["if"]:
            print(self.lexemes[self.cursor])
            self.cursor += 1
            if self.conditional_expression():
                if self.lexemes[self.cursor] == self.lexemesMap["THEN"]:
                    print(self.lexemes[self.cursor])
                    self.cursor += 1
                    if self.condition_body():
                        succeeded = True
        return succeeded

    # <условное выражение> -> <арифмитическое выражение> < / > / >= / <= / = / != <арифмитическое выражение>
    def conditional_expression(self) -> bool:
        succeeded = False
        if self.arithmetic_expression():
            current_lexeme = self.lexemes[self.cursor]
            if (current_lexeme == self.lexemesMap["<"] or
                    current_lexeme == self.lexemesMap[">"] or
                    current_lexeme == self.lexemesMap[">="] or
                    current_lexeme == self.lexemesMap["<="] or
                    current_lexeme == self.lexemesMap["="] or
                    current_lexeme == self.lexemesMap["!="]):
                print(self.lexemes[self.cursor])
                self.cursor += 1
                if self.arithmetic_expression():
                    succeeded = True
        return succeeded

    # <тело условия> -> <оператор> / begin <раздел операторов> end
    def condition_body(self) -> bool:
        succeeded = False
        if self.operator():
            succeeded = True
        elif self.lexemes[self.cursor] == self.lexemesMap["begin"]:
            print(self.lexemes[self.cursor])
            self.cursor += 1
            if self.operators_section():
                if self.lexemes[self.cursor] == self.lexemesMap["end"]:
                    print(self.lexemes[self.cursor])
                    self.cursor += 1
                    succeeded = True
        return succeeded

    # <арифмитическое выражение> -> <слагаемое> {+ <слагаемое>} {- <слагаемое>}
    def arithmetic_expression(self) -> bool:
        succeeded = False
        if self.summand():
            succeeded = True
            while (self.lexemes[self.cursor] == self.lexemesMap["+"] or
                   self.lexemes[self.cursor] == self.lexemesMap["-"]):
                print(self.lexemes[self.cursor])
                self.cursor += 1
                if not self.summand():
                    succeeded = False
        return succeeded

    # <слагаемое> -> <значение> {* <значение>} {DIV <значение>} {MOD <значение>} {DIY <значение>}
    def summand(self) -> bool:
        succeeded = False
        if self.value():
            succeeded = True
            while (self.lexemes[self.cursor] == self.lexemesMap["*"] or
                   self.lexemes[self.cursor] == self.lexemesMap["DIV"] or
                   self.lexemes[self.cursor] == self.lexemesMap["MOD"] or
                   self.lexemes[self.cursor] == self.lexemesMap["DIY"]):
                print(self.lexemes[self.cursor])
                self.cursor += 1
                if not self.value():
                    succeeded = False
        return succeeded

    # <значение>: <значение> -> ид / конст / ( <арифметическое выражение> )
    def value(self) -> bool:
        succeeded = False
        if type(self.lexemes[self.cursor]) is list:
            data = self.lexemes[self.cursor][1]
            print(f"{self.lexemes[self.cursor][0]} {data}")
            self.cursor += 1
            succeeded = True
        elif self.lexemes[self.cursor] == self.lexemesMap["("]:
            print(self.lexemes[self.cursor])
            self.cursor += 1
            if self.arithmetic_expression():
                if self.lexemes[self.cursor] == self.lexemesMap[")"]:
                    print(self.lexemes[self.cursor])
                    self.cursor += 1
                    succeeded = True
        return succeeded
