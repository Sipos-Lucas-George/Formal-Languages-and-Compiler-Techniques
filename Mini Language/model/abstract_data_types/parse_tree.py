class ParseTree:
    def __init__(self):
        self.__index = 0
        self.__tree = {}

    def add(self, symbols, parent: int):
        if self.__index == 0:
            self.__tree[1] = [symbols[0], 0, 0]
            self.__index += 1
            return
        for i, symbol in enumerate(symbols):
            self.__index += 1
            self.__tree[self.__index] = [symbol, parent, self.__index - 1] if i != 0 \
                else [symbol, parent, 0]

    def get_parent(self, top_symbol):
        if self.__index == 0:
            return 0
        for index, element in self.__tree.items():
            if element[:2] == top_symbol:
                return index

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
        return result
