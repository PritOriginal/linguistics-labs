class OperatorPrecedence:
    def __init__(self, lexemes, lexemesMap, identifiersMap):
        self.lexemes = lexemes
        self.lexemesMap = lexemesMap
        self.identifiersMap = identifiersMap

        self.initMatrix()

    def initMatrix(self):
        with open('gramma_operator_precedence.md', 'r', encoding='utf8') as f:
            matrix = {}
            header = []
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
                        # print(lexeme, data)
                        matrix_row = {}
                        for i, l in enumerate(data):
                            if l != '':
                                matrix_row[header[i]] = l
                        if lexeme == 'ид':
                            lexeme_num = 0
                        elif lexeme == 'конст':
                            lexeme_num = 1
                        else:
                            lexeme_num = self.lexemesMap[lexeme]
                        matrix[lexeme_num] = matrix_row
            print(matrix)