class Dictionary:
    def __init__(self):
        self.__data = {}

    def __len__(self):
        return len(self.__data)

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, item):
        return self.__data[item]

    def __iter__(self):
        self.__iteration_items = list(self.__data.items())
        self.__iteration_index = 0
        return self

    def __next__(self):
        if self.__iteration_index < len(self.__iteration_items):
            item = self.__iteration_items[self.__iteration_index]
            self.__iteration_index += 1
            return item
        raise StopIteration
