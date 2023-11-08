import os
from dotenv import load_dotenv

load_dotenv()

PATH_FA = os.getenv("PATH_FA")


class FiniteAutomata:
    def __init__(self):
        with open(PATH_FA) as file:
            lines = file.readlines()
        self.__fa_elements = {}
        index, type_fa = 0, ""
        for line in lines:
            if index == 3 and line.find(",") == -1:
                index += 1
            if index == 0:
                type_fa = line.strip()
                self.__fa_elements[type_fa] = {}
                self.__fa_elements[type_fa]["transitions"] = {}
            if index == 1:
                self.__fa_elements[type_fa]["states"] = line.strip().split(",")
            elif index == 2:
                self.__fa_elements[type_fa]["alphabet"] = line.strip().split(",")
            elif index == 3:
                elements = line.strip().split(",")
                self.__fa_elements[type_fa]["transitions"][(elements[0], elements[-1])] = elements[1:-1]
                continue
            elif index == 4:
                self.__fa_elements[type_fa]["initial_state"] = line.strip()
            elif index == 5:
                self.__fa_elements[type_fa]["final_state"] = line.strip()
                index = 0
                continue
            index += 1

    def display_states(self):
        print("States:")
        for key in self.__fa_elements.keys():
            print(key)
            print(self.__fa_elements[key]["states"])
            print()

    def display_alphabet(self):
        print("Alphabet:")
        for key in self.__fa_elements.keys():
            print(key)
            print(self.__fa_elements[key]["alphabet"])
            print()

    def display_transitions(self):
        print("Transitions:")
        for key in self.__fa_elements.keys():
            print(key)
            for state, transition in self.__fa_elements[key]["transitions"].items():
                print(f"{state[0]} -> {', '.join(transition)} -> {state[1]}")
            print()

    def display_initial_state(self):
        print("Initial State:")
        for key in self.__fa_elements.keys():
            print(key)
            print(self.__fa_elements[key]["initial_state"])
            print()

    def display_final_states(self):
        print("Final States:")
        for key in self.__fa_elements.keys():
            print(key)
            print(self.__fa_elements[key]["final_state"])
            print()

    def recursive_fa(self, current_state, transitions, final_state, lexeme, index):
        if current_state == final_state and len(lexeme) == index:
            return True
        if current_state != final_state and len(lexeme) == index:
            return False
        made_transition = False
        for transition, valid_tokens in transitions.items():
            if transition[0] == current_state and lexeme[index] in valid_tokens:
                made_transition = made_transition or self.recursive_fa(transition[1], transitions, final_state, lexeme, index + 1)
            if made_transition is True:
                return True
        if made_transition is False:
            return False

    def verify_lexeme(self, lexeme):
        for type_fa, elements in self.__fa_elements.items():
            accepted_by_fa = self.recursive_fa(elements["initial_state"], elements["transitions"],
                                               elements["final_state"], lexeme, 0)
            if accepted_by_fa:
                return type_fa
        return "UNKNOWN"

    @staticmethod
    def print_menu():
        print("Menu:")
        print("m. Print menu")
        print("1. Display States")
        print("2. Display Alphabet")
        print("3. Display Transitions")
        print("4. Display Initial State")
        print("5. Display Final States")
        print("6. Check if a sequence is accepted")
        print("x. Exit")
        print()

    def secrete_program(self):
        command_dictionary = {
            "m": self.print_menu,
            "x": exit,
            "1": self.display_states,
            "2": self.display_alphabet,
            "3": self.display_transitions,
            "4": self.display_initial_state,
            "5": self.display_final_states,
        }
        self.print_menu()
        while True:
            command = input("Enter your choice: ")
            print()
            if command == "6":
                self.verify_lexeme(input("Enter lexeme: "))
            elif command in command_dictionary:
                command_dictionary[command]()
            else:
                print("Invalid command!", end="\n\n")
