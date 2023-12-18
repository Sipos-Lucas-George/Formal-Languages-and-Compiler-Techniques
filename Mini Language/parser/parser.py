from collections import defaultdict
from parser.grammar import Grammar
from model.abstract_data_types.parse_tree import ParseTree


class Parser:
    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first_sets = defaultdict(set)
        self.__follow_sets = defaultdict(set)
        self.__parsing_table = {}
        self.__parse_tree = ParseTree()

    def print_first_sets(self):
        for key, value in self.__first_sets.items():
            print(f"{str(key):<20}", *sorted(list(value)))

    def print_follow_sets(self):
        for key, value in self.__follow_sets.items():
            print(f"{str(key):<20}", *sorted(list(value)))

    def print_parsing_table(self):
        for key, value in self.__parsing_table.items():
            print(f"{str(key):<30}", value)

    def print_parse_tree(self):
        print(self.__parse_tree)

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
                                for s in right[j + 1:j + 2]:
                                    next_symbols_first.update(self.__first_sets[s]
                                                              if s in non_terminals else s)
                                if "epsilon" in next_symbols_first:
                                    self.__follow_sets[symbol].update(self.__follow_sets[left])
                                self.__follow_sets[symbol].update(next_symbols_first - {"epsilon"})

            if prev_follow_sets == self.__follow_sets:
                break

    def compute_parsing_table(self):
        i = 0
        terminals = self.__grammar.get_terminals()
        for non_terminal, production_rules in self.__grammar.get_productions().items():
            for production_rule in production_rules:
                i += 1
                if production_rule[0] == 'epsilon':
                    for follow in self.__follow_sets[non_terminal]:
                        self.__parsing_table[(non_terminal, follow)] = (production_rule, i)
                else:
                    if production_rule[0] in terminals:
                        self.__parsing_table[(non_terminal, production_rule[0])] = (production_rule, i)
                        continue
                    for first in self.__first_sets.get(non_terminal, production_rule[0]):
                        if first == 'epsilon':
                            continue
                        self.__parsing_table[(non_terminal, first)] = (production_rule, i)

    def parse(self, input_string):
        terminals = self.__grammar.get_terminals()
        stack = [(self.__grammar.get_start_symbol(), 0)]

        while stack and input_string:
            top_symbol = stack[-1]
            next_input_symbol = input_string[0]

            if top_symbol in terminals:
                if top_symbol == next_input_symbol:
                    stack.pop()
                    input_string = input_string[1:]
                else:
                    return f"Error the program broke at {next_input_symbol} and {input_string}"
            elif top_symbol[0] not in terminals:
                if (top_symbol[0], next_input_symbol) in self.__parsing_table:
                    production_rule = self.__parsing_table[(top_symbol[0], next_input_symbol)][0][::-1]
                    stack.pop()
                    parent = self.__parse_tree.get_parent(list(top_symbol))
                    for symbol in production_rule:
                        stack.append(symbol if symbol in terminals else (symbol, parent))
                    self.__parse_tree.add(production_rule, parent)
                else:
                    return f"Error the program broke at {next_input_symbol} and {input_string}"
            else:
                return f"Error the program broke at {next_input_symbol} and {input_string}"

        if not stack and not input_string:
            return "Parsing successful!"
        else:
            return "Error the program broke at input string or stack"

    @staticmethod
    def error():
        print("Error in parsing..change later")
