class Dictionary:
    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def __getitem__(self, item):
        return self.__data[item]

    def __str__(self):
        return f"{'Index':<15} {'Value'}\n" + '\n'.join([f"{str(entry[1]):<15} {entry[0]}" for entry in self.__data])

    def add(self, token, index):
        self.__data.append((token, index))
