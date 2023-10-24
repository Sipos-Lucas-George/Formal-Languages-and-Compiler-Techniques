from model.abstract_data_types.hash_table import HashTable
from model.abstract_data_types.dictionary import Dictionary
from dotenv import load_dotenv


class Scanner:
    def __init__(self, file: str):
        with open("symbols.txt") as file:
            self.__symbols = [item.strip() for item in file.readlines()]
        self.__symbol_table_identifier = HashTable()
        self.__symbol_table_constant = HashTable()
        self.__program_internal_form = Dictionary()
        with open(file) as file:
            self.__file = file
        self.__scan()

    def __scan(self):
        pass
