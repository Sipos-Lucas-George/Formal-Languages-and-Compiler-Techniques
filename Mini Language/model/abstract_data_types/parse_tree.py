class ParseTree:
    def __init__(self):
        self.__index = 0
        self.__tree = {}

    def add(self, symbol, parent: int):
        self.__index += 1
        if self.__index == 1:
            self.__tree[1] = [symbol, 0, 0]
            return
        self.__tree[self.__index] = [symbol, parent, self.__index - 1] if self.__tree[self.__index - 1][1] == parent \
            else [symbol, parent, 0]

    def clear(self):
        self.__index = 0
        self.__tree.clear()

    def __str__(self):
        result = f"{'INDEX':<20}{'SYMBOL':<20}{'PARENT':<20}{'RIGHT SIBLING':<20}\n"
        for key, values in self.__tree.items():
            result += f"{str(key):<20}"
            for value in values:
                result += f"{str(value):<20}"
            result += "\n"
