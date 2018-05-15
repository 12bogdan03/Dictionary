class TextFixer:
    def __init__(self):
        self.symbols_to_change = {'e': 'е', 'y': 'у', 'i': 'і', 'o': 'о',
                                  'p': 'р', 'a': 'а', 'x': 'х', 'c': 'с',
                                  'E': 'е', 'O': 'о', 'P': 'р', 'A': 'а',
                                  'H': 'Н', 'K': 'К', 'X': 'Х', 'C': 'С',
                                  'B': 'В', ' M': 'M', 'T':'Т','I':'І'}

    def fix(self, text: str):
        for eng_s, ukr_s in self.symbols_to_change.items():
            text = text.replace(eng_s, ukr_s)
        return text


if __name__ == '__main__':
    text = 'Teкcт'
    fixer = TextFixer()
    fixed_text = fixer.fix(text)
    print(fixed_text)