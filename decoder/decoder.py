from decoder.methods.recursive_descent import RecursiveDescent
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
    ]

    def __init__(self):
        self.wasCut = False
        self.buf = ""
        self.isLexeme = True
        self.isConst = True
        self.isIdent = True

        self.lexemesMap = {}
        for i, lexeme in enumerate(self.lexemes):
            self.lexemesMap[lexeme] = i + 2

        self.identifiersMap = {}

        self.parseLexemes = []


    def cut(self):
        self.wasCut = True
        self.buf = self.buf[-1]
        self.isLexeme = True
        self.isConst = True
        self.isIdent = True

    def show_maps(self):
        print("Identifier: 0")
        print("Constant: 1")
        print(f"Lexemes: {self.lexemesMap}")
        print(f"Identifiers: {self.identifiersMap}")

    def is_lexeme(self):
        curLexeme = ""
        for lex in self.lexemes:
            if self.buf in lex:
                curLexeme = lex
                if self.buf == lex:
                    self.lexeme = lex
                # break
        if curLexeme == "":
            self.isLexeme = False

    def is_const(self):
        if self.buf.isdigit():
            self.const = self.buf
        else:
            self.isConst = False

    def is_ident(self):
        if not self.buf[0].isdigit():
            for c in [",", ".", ":", ";", "-", "=", "?", "!", "*", " ", "\n"]:
                if self.buf[-1] == c:
                    self.isIdent = False
                    break
        else:
            self.isIdent = False
        if self.isIdent:
            self.ident = self.buf

    def add_ident(self, ident):
        if ident not in self.identifiersMap:
            self.identifiersMap[ident] = len(self.identifiersMap)

    def decode(self):
        with open("data.txt", "r") as f:
            with open("output.txt", "w") as f_otput:
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
                            f_otput.write("\n")
                        # Лексема
                        if self.lexeme != "":
                            f_otput.write(str(self.lexemesMap[self.lexeme]) + " ")
                            self.parseLexemes.append(self.lexemesMap[self.lexeme])
                            reset()
                            self.cut()
                        # Константа
                        elif self.const != "":
                            f_otput.write(f"1 {self.const} ")
                            self.parseLexemes.append(1)
                            self.parseLexemes.append(int(self.const))
                            reset()
                            self.cut()
                        # Идентификатор
                        elif self.ident != "":
                            self.add_ident(self.ident)
                            f_otput.write(f'0 {self.identifiersMap[self.ident]} ')
                            self.parseLexemes.append(0)
                            self.parseLexemes.append(self.identifiersMap[self.ident])
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
        self.parseLexemes.append(0)

    def recursive_descent(self):
        rec_des = RecursiveDescent(lexemes=self.parseLexemes, lexemesMap=self.lexemesMap, identifiersMap=self.identifiersMap)
        rec_des.disassemble()