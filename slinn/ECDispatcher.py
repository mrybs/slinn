class ECDispatcher:
    def __init__(self):
        self.functions = {}

    def __getitem__(self, key: int):
        if str(key) in self.functions.keys():
            return self.functions[str(key)]
        
    def __call__(self, code: int):
        if code < 99 or code > 599:
            raise ValueError(f'Error code {code} does not exist')
        def decorator(func):
            self.functions[str(code)] = func
            return func
        return decorator