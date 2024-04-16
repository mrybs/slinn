import re


class Preprocessor:
    def __init__(self, open_quote: str = '<%', close_quote: str = '%>') -> None:
        self.open_quote = open_quote
        self.close_quote = close_quote
        self.pattern = lambda element='.*': fr'{self.open_quote}\s*{element}\s*{self.close_quote}'

    def replace(self, text: str, data: dict) -> str:
        for i, dat in enumerate(data):
            i_dat = list(dat)[0]
            text = re.sub(self.pattern(i_dat), dat[i_dat], text)
        return text

    def preprocess(self, text: str, data: dict) -> str:
        return self.clean(self.replace(text, data))

    def clean(self, text: str) -> str:
        return re.sub(self.pattern(), '', text)

    def count(self, text: str) -> int:
        return len(re.match(self.pattern(), text))

    def count_trash(self, text: str, data: dict) -> int:
        i = self.count(text)
        for i, dat in enumerate(data):
            i_dat = list(dat)[0]
            if text != re.sub(self.pattern(), dat[i_dat], text):
                i -= 1
        return i
