import os
import re
from model.abstract_data_types.hash_table import HashTable
from model.abstract_data_types.list import List
from finite_automata.finite_automata import FiniteAutomata
from dotenv import load_dotenv

load_dotenv()

PATH_TOKENS = os.getenv("PATH_TOKENS")


class Scanner:
    def __init__(self, problem_path: str):
        with open(PATH_TOKENS) as file:
            self.__tokens = [line.strip() for line in file.readlines()]
        self.__symbol_table_identifier = HashTable()
        self.__symbol_table_constant = HashTable()
        self.__program_internal_form = List()
        self.__finite_automata = FiniteAutomata()
        with open(problem_path) as file:
            self.__problem_text = file.readlines()
        self.__scan()

    def __scan(self):
        error = "Lexically Correct"
        for index, line in enumerate(self.__problem_text):
            if re.match(r"^\s*$", line):
                continue
            aux_line = line.strip()

            lexemes = self.sequence_to_lexemes(aux_line)
            lexemes = self.concatenate_signed_integers(lexemes)
            for lexeme in lexemes:
                verify_by_fa = self.__finite_automata.verify_lexeme(lexeme)
                if lexeme in self.__tokens:
                    self.__program_internal_form.add(lexeme, -1)
                elif verify_by_fa == "IDENTIFIER":
                    index_id = self.__symbol_table_identifier.add(lexeme)
                    self.__program_internal_form.add(lexeme, index_id)
                elif verify_by_fa == "INTEGER" or re.match("^(\"[^\"]*\")$", lexeme):
                    index_id = self.__symbol_table_constant.add(lexeme)
                    self.__program_internal_form.add(lexeme, index_id)
                else:
                    index_error = self.__problem_text[index].find(lexeme)
                    error = f"Lexical Error! Line {index + 1} Col {index_error + 1}\n"
                    error += self.__problem_text[index][:-1] + "\n"
                    error += " " * index_error + "^" * len(lexeme)
                    break
            else:
                continue
            break
        self.write_to_file_st_pif(error)

    def write_to_file_st_pif(self, error):
        with open("PIF.out", "w") as file:
            file.write(str(self.__program_internal_form) + "\n\n" + error)
        with open("ST.out", "w") as file:
            file.write("IDENTIFIERS:\n" + str(self.__symbol_table_identifier) + "\n\nCONSTANTS:\n" +
                       str(self.__symbol_table_constant))

    def concatenate_signed_integers(self, lexemes):
        i = 0
        result = []
        parentheses = ["]", ")", "}"]
        while i < len(lexemes):
            if (lexemes[i] == "+" or lexemes[i] == "-") and (
                    i == 0 or (i != 0 and lexemes[i - 1] in self.__tokens)) and i + 1 < len(lexemes) \
                    and re.match("^(\d|[1-9]\d*)$", lexemes[i + 1]) and lexemes[i - 1] not in parentheses:
                result.append(lexemes[i] + lexemes[i + 1])
                i += 2
            else:
                result.append(lexemes[i])
                i += 1
        return result

    @staticmethod
    def sequence_to_lexemes(sequence: str) -> list[str]:
        list_of_lexemes = []
        delimiter = [",", ";", "(", ")", "[", "]", "{", "}", " ", "+", "-", "*", "/", "%", ">", "<", "="]
        soft_delimiter = [">", "<", "="]
        start = 0
        end = 0
        last_char = ""
        while end < len(sequence):
            if sequence[end] == "\"":
                if len(last_char) == 0:
                    start = end
                    result = sequence[end + 1:].find("\"")
                    if result == -1:
                        list_of_lexemes.append(sequence[start:])
                        return list_of_lexemes
                    else:
                        end += result + 2
                        if end >= len(sequence):
                            list_of_lexemes.append(sequence[start:end])
                            return list_of_lexemes
                        if sequence[end] in delimiter:
                            list_of_lexemes.append(sequence[start:end])
                            if sequence[end] != " ":
                                list_of_lexemes.append(sequence[end])
                            start = end + 1
                        else:
                            list_of_lexemes.append(sequence[start:end])
                            list_of_lexemes.append(sequence[end:])
                            return list_of_lexemes
                else:
                    list_of_lexemes.append(sequence[start:end + 1])
                    return list_of_lexemes
            else:
                if sequence[end] == " " and len(last_char) == 0:
                    end += 1
                    start = end
                    continue
                if sequence[end] in delimiter:
                    if len(last_char) != 0:
                        last_char = ""
                        list_of_lexemes.append(sequence[start:end])
                    if (sequence[end] in soft_delimiter and end + 1 < len(sequence)
                            and sequence[end + 1] in soft_delimiter):
                        list_of_lexemes.append(sequence[end:end + 2])
                        end += 1
                    elif sequence[end] != " ":
                        list_of_lexemes.append(sequence[end])
                    start = end + 1
                else:
                    last_char = sequence[end]
            end += 1

        return list_of_lexemes
