from collections import defaultdict
from parser.grammar import Grammar


class Parser:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first_sets = defaultdict(set)
        self.__follow_sets = defaultdict(set)

    def print_first_sets(self):
        for key, value in self.__first_sets.items():
            print(f"{str(key):<20}", *sorted(list(value)))

    def print_follow_sets(self):
        for key, value in self.__follow_sets.items():
            print(f"{str(key):<20}", *sorted(list(value)))

    def build_first_sets(self):
        while True:
            prev_first_sets = {key: value.copy() for key, value in self.__first_sets.items()}

            for production in self.__grammar.get_productions().items():
                non_terminal = production[0]
                right_symbols = production[1]
                for right_symbol in right_symbols:
                    i = 0
                    while i < len(right_symbol):
                        symbol = right_symbol[i]

                        if symbol in self.__grammar.get_terminals():
                            self.__first_sets[non_terminal].add(symbol)
                            break
                        elif symbol in self.__grammar.get_non_terminals():
                            self.__first_sets[non_terminal].update(self.__first_sets[symbol] - {'epsilon'})
                            if 'epsilon' not in self.__first_sets[symbol]:
                                break

                        i += 1
                    else:
                        self.__first_sets[non_terminal].add('epsilon')

            if prev_first_sets == self.__first_sets:
                break

    def compute_follow_sets(self):
        non_terminals = self.__grammar.get_non_terminals()
        self.__follow_sets[self.__grammar.get_start_symbol()].add('$')

        while True:
            prev_follow_sets = {key: value.copy() for key, value in self.__follow_sets.items()}

            for production in self.__grammar.get_productions().items():
                left, right_list = production[0], production[1]
                for right in right_list:
                    for j in range(len(right)):
                        symbol = right[j]
                        if symbol in non_terminals:
                            if j == len(right) - 1:
                                self.__follow_sets[symbol].update(self.__follow_sets[left])
                            else:
                                next_symbols_first = set()
                                for s in right[j + 1:]:
                                    next_symbols_first.update(self.__first_sets[s]
                                                              if s in non_terminals else s)
                                if "epsilon" in next_symbols_first:
                                    self.__follow_sets[symbol].update(self.__follow_sets[left])
                                self.__follow_sets[symbol].update(next_symbols_first - {"epsilon"})

            if prev_follow_sets == self.__follow_sets:
                break
