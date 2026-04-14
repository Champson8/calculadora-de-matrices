from dataclasses import dataclass
from sys import stdout
from msvcrt import getch
from matrix import Matrix

TITLE = "=== CALCULADORA DE MATRICES ===\n"
HIDE_CURSOR = "\033[?25l"


@dataclass
class AppState:
    matrixA: Matrix = None
    matrixB: Matrix = None
    currentMenu: str = "main"
    isRunning: bool = True

    @property
    def numMatrices(self):
        return 2 - [self.matrixA, self.matrixB].count(None)


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


def displayInteractiveMenu(options):
    numOptions = len(options)
    selected = 0

    while True:
        clearConsole()
        print(TITLE)

        for i, option in enumerate(options):
            print(f" > [ {option} ] < " if i == selected else option)

        action = inputToAction(getch().lower())

        match action:
            case "UP":
                selected = (selected - 1) % numOptions
            case "DOWN":
                selected = (selected + 1) % numOptions
            case "ENTER":
                return selected
            case "ESCAPE":
                return None


def main():
    state = AppState()
    print(HIDE_CURSOR)
    while state.isRunning:
        clearConsole()

        match state.currentMenu:

            case "main":
                options = ["Ingresar Matriz"]
                binaryOptions = [
                    "Sumar Matrices",
                    "Restar Matrices",
                    "Multiplicar Matrices",
                ]
                unaryOptions = [
                    "Multiplicar Matriz por Escalar",
                    "Invertir Matriz",
                    "Transponer Matriz",
                    "Resolver Sistema de Ecuaciones Lineales",
                ]
                if state.numMatrices >= 1:
                    options += unaryOptions
                if state.numMatrices == 2:
                    options += binaryOptions
                choice = displayInteractiveMenu(options)


if __name__ == "__main__":
    main()
