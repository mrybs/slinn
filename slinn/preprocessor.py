import re
from slinn import utils


class Preprocessor:

    """
    Pages preprocessor
    """
    
    def __init__(self, open_quote: str = '<%', close_quote: str = '%>') -> None:
        self.open_quote = open_quote
        self.close_quote = close_quote
        self.pattern = lambda element='.*': fr'{self.open_quote}\s*{element}\s*{self.close_quote}'

    def replace(self, text: str, data: dict) -> str:
        for zaloop in re.findall(fr'{self.open_quote}\s*for\s*\w+\s*in\s*\w+\s*{self.close_quote}[\x00-\xff]+{self.open_quote}\s*end\s*{self.close_quote}', text):
            loop = zaloop.replace(re.search(fr'{self.open_quote}\s*end\s*{self.close_quote}', zaloop).group(0), '', 1)
            header = re.search(fr'{self.open_quote}\s*for\s*\w+\s*in\s*\w+\s*{self.close_quote}', loop).group(0)
            iterator = header.replace(re.search(fr'{self.open_quote}\s*for\s*', header).group(0), '', 1)\
                             .replace(re.search(fr'\s*in\s*\w+\s*{self.close_quote}', header).group(0), '', 1)
            iterable = header.replace(re.search(fr'{self.open_quote}\s*for\s*\w+\s*in\s*', header).group(0), '', 1)\
                             .replace(re.search(fr'\s*{self.close_quote}', header).group(0), '', 1)
            loop = loop.replace(header, '', 1)
            looped = ""
            for it in data[iterable]:
                ll = loop
                print(fr'{self.open_quote}\s*{iterator}(\.\w+)?\s*{self.close_quote}', ll.encode(), re.findall(fr'{self.open_quote}\s*{iterator}(\.\w+)?\s*{self.close_quote}', ll, re.MULTILINE))
                while zai := re.search(fr'{self.open_quote}\s*{iterator}(\.\w+)?\s*{self.close_quote}', ll):
                    zai = zai.group(0)
                    i = zai.replace('<%', '', 1).replace('%>', '', 1).strip().removeprefix(iterator+'.')
                    print('zai', zai, 'loop', loop.encode())
                    ll = ll.replace(zai, utils.representate(getattr(it, i, it)), 1)
                    print(ll)
                    print(i)
                looped += ll
            del data[iterable]
            text = text.replace(zaloop, looped)
        for key in data:
            text = re.sub(self.pattern(key), utils.representate(data[key]), text)
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
