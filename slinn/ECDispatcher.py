class ECDispatcher:
    def __init__(self) -> None:
        self.functions = {}

    def __getitem__(self, key: int) -> callable:
        if str(key) in self.functions.keys():
            return self.functions[str(key)]
        raise KeyError(f'Error code {key} does not exist')

    def __call__(self, code: int) -> callable:
        if code < 99 or code > 599:
            raise ValueError(f'Error code {code} does not exist')

        def decorator(func):
            self.functions[str(code)] = func
            return func

        return decorator
