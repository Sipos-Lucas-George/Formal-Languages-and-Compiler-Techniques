import os

from scanner.scanner import Scanner
from finite_automata.finite_automata import FiniteAutomata
from dotenv import load_dotenv
from parser.grammar import Grammar

load_dotenv()

P1 = os.getenv("P1")
P2 = os.getenv("P2")
P3 = os.getenv("P3")
P4 = os.getenv("P4")

if __name__ == "__main__":
    Scanner(P2)
    # FiniteAutomata().secrete_program()
    g = Grammar()
    print(g.cfg_check())
    g.print_non_terminals()
    g.print_terminals()
    g.print_productions()
    g.print_productions_for_non_terminal("statement")
