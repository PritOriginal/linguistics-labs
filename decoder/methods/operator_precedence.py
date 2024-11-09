class OperatorPrecedence:
    def __init__(self, lexemes, lexemesMap: dict, identifiersMap):
        self.lexemes = lexemes
        self.lexemesMap = lexemesMap
        self.identifiersMap = identifiersMap

        self.matrix = None
        self.init_matrix()

    def init_matrix(self):
        with open('gramma_operator_precedence.md', 'r', encoding='utf8') as f:
            self.matrix: dict[int, dict[int, str]] = {}
            header: list[int] = []
            for line in f.readlines():
                if line[0] == '|' and line[1] != ':':
                    line = line.strip()
                    row = line.strip('|').split('|')
                    for i in range(len(row)):
                        row[i] = row[i].strip().strip('`')

                    if len(header) == 0:
                        header = row[1:]
                        for i in range(len(header)):
                            if header[i] == 'ид':
                                header[i] = 0
                            elif header[i] == 'конст':
                                header[i] = 1
                            else:
                                header[i] = self.lexemesMap[header[i]]
                    else:
                        lexeme = row[0]
                        data = row[1:]
                        matrix_row: dict[int, str] = {}
                        for i, l in enumerate(data):
                            if l != '':
                                matrix_row[header[i]] = l
                        if lexeme == 'ид':
                            lexeme_num = 0
                        elif lexeme == 'конст':
                            lexeme_num = 1
                        else:
                            lexeme_num = self.lexemesMap[lexeme]
                        self.matrix[lexeme_num] = matrix_row

    def _get_lexeme(self, i: int) -> int:
        if type(self.lexemes[i]) is list:
            return self.lexemes[i][0]
        return self.lexemes[i]

    def disassemble(self):
        k = len(self.lexemes)
        n1, n2 = 0, 0
        while True:
            i = 1
            s = '<'
            while i < k:
                n1 = self._get_lexeme(i - 1)
                n2 = self._get_lexeme(i)
                s += str(n1) + self.matrix[n1][n2]
                if self.matrix[n1][n2] == '>':
                    break
                i += 1

            s += str(n2) + '>'
            print(s)
            j2 = i - 1
            j1 = j2
            while True:
                j1 = j1 - 1
                n1 = self._get_lexeme(j1)
                n2 = self._get_lexeme(j1 + 1)
                if j1 < 0 or self.matrix[n1][n2] == '<':
                    break
            for x in range(j1 + 1, i):
                print(self.lexemes[x])

            j = j1
            for x in range(i, k):
                j += 1
                self.lexemes[j] = self.lexemes[x]
                self.lexemes[j + 1] = 0
            k -= j2 - j1

            if k <= 1:
                print(self._get_lexeme(0))
                break
