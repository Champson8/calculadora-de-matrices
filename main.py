from dataclasses import dataclass
from sys import stdout
from msvcrt import getch
from matrix import Matrix

TITLE = "=== CALCULADORA DE MATRICES ==="

options = [
    "Ingresar Matriz",
    "Multiplicar Matriz por Escalar",
    "Invertir Matriz",
    "Transponer Matriz",
    "Resolver Sistema de Ecuaciones Lineales",
    "Sumar Matrices",
    "Restar Matrices",
    "Multiplicar Matrices",
]


@dataclass
class AppState:
    matrixA: Matrix = None
    matrixB: Matrix = None
    currentMenu: str = "main"
    isRunning: bool = True

    @property
    def hasOneMatrix(self):
        return bool(self.matrixA) ^ bool(self.matrixB)

    @property
    def hasNoMatrices(self):
        return not self.matrixA and not self.matrixB


def clearConsole():
    stdout.write("\033[H\033[2J\033[3J")
    stdout.flush()


def inputToAction(inp):
    pairs = {b"w": "UP", b"s": "DOWN", b"\r": "ENTER", b"\x1b": "ESCAPE"}
    extendedPairs = {b"H": "UP", b"P": "DOWN"}
    if inp in pairs:
        inp = pairs[inp]
    elif inp in [b"\x00", b"\xe0"]:
        inp = getch()
        if inp in extendedPairs:
            inp = extendedPairs[inp]
    else:
        inp = inp.decode()
    return inp


def main():
    state = AppState()
    selected = 0
    while state.isRunning:
        overwriteConsole()
        for i, option in enumerate(options):
            print(option, "this" if i == selected else "")
        action = inputToAction(getch().lower())
        if action == "up" and selected > 0:
            selected -= 1
        elif action == "down" and selected < len(options) - 1:
            selected += 1
        elif action == "ENTER":
            pass


if __name__ == "__main__":
    main()
