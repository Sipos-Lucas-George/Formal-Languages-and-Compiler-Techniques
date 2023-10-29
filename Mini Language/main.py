import os

from scanner.scanner import Scanner
from dotenv import load_dotenv

load_dotenv()

P1 = os.getenv("P1")
P2 = os.getenv("P2")
P3 = os.getenv("P3")
P4 = os.getenv("P4")

if __name__ == "__main__":
    Scanner(P2)

