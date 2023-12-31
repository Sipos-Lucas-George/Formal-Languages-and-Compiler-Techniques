SIZE = 1000
NULL_PAIR = [-1, -1]


class HashTable:
    def __init__(self):
        self.__capacity = SIZE
        self.__size = 0
        self.__data = [[] for _ in range(self.__capacity)]

    def __len__(self):
        return self.__size

    def __getitem__(self, item):
        return self.__data[item]

    def __str__(self):
        return f"{'Position':<15} Value\n" + "\n".join([f"{str(entry[0]):15} {entry[1]}"
                                                        for entry in self.get_as_list()])

    def __hash(self, key):
        key = str(key)
        index = 0
        if key.startswith("-"):
            key = "a" + key[1:]
        for i, c in enumerate(key, start=1):
            if c == "_":
                index += (30 * i)
            elif "a" <= c <= "z":
                index += ((ord(c) - ord("a")) * i)
            elif "A" <= c <= "z":
                index += ((ord(c) - ord("A")) * i)
            else:
                index += ((ord(c) - ord("0")) * i)

        return index % self.__capacity

    def add(self, elem):
        self.__size += 1
        index = self.__hash(elem)
        if len(self.__data[index]) == 0:
            self.__data[index].append(elem)
            return [index, 0]
        else:
            i = 0
            while i < len(self.__data[index]) and self.__data[index][i] != elem:
                i += 1
            if i < len(self.__data[index]):
                self.__size -= 1
                return [index, i]
            self.__data[index].append(elem)
            return [index, i]

    def find(self, elem):
        index = self.__hash(elem)
        if len(self.__data[index]) == 0:
            return NULL_PAIR
        else:
            for i, x in enumerate(self.__data[index]):
                if x == elem:
                    return [index, i]
            return NULL_PAIR

    def remove(self, elem):
        self.__size -= 1
        index = self.__hash(elem)
        i = -1
        if len(self.__data[index]) != 0:
            for j, x in enumerate(self.__data[index]):
                if x == elem:
                    self.__data[index] = self.__data[index][:j] + self.__data[index][j + 1:]
                    i = j
        if i == -1:
            self.__size += 1
            return False
        return True

    def size(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def get_all(self):
        return self.__data

    def get_as_list(self):
        result = []
        for index_hash, item_list in enumerate(self.__data):
            if len(item_list) == 0:
                continue
            for index_position, item in enumerate(item_list):
                result.append([[index_hash, index_position], item])
        return result
