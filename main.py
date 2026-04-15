from dataclasses import dataclass
from msvcrt import getch
from matrix import Matrix
from utils import clearConsole, printTitle
from constants import CONTROLS, HIDE_CURSOR


@dataclass
class AppState:
    matrixA: Matrix = None
    matrixB: Matrix = None
    currentMenu: str = "main"
    activeTarget: str = None
    nextMenu: str = None
    isRunning: bool = True

    @property
    def numMatrices(self):
        return 2 - [self.matrixA, self.matrixB].count(None)


def getUserAction():
    inp = getch().lower()
    if inp in [b"\x00", b"\xe0"]:
        inp = getch()

    match inp:
        case b"w" | b"H":
            return "UP"
        case b"s" | b"P":
            return "DOWN"
        case b"\r":
            return "ENTER"
        case b"\x1b":
            return "ESCAPE"


def displayInteractiveMenu(title: str, options: list | tuple):
    numOptions = len(options)
    selected = 0

    while True:
        clearConsole()
        printTitle(title)

        for i, option in enumerate(options):
            print(f" > [ {option} ] < " if i == selected else option)

        print(CONTROLS)

        action = getUserAction()

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
                unaryOptions = [
                    "Multiplicar Matriz por Escalar",
                    "Invertir Matriz",
                    "Transponer Matriz",
                    "Resolver Sistema de Ecuaciones Lineales",
                ]
                binaryOptions = [
                    "Sumar Matrices",
                    "Restar Matrices",
                    "Multiplicar Matrices",
                ]
                if state.numMatrices >= 1:
                    options += unaryOptions
                if state.numMatrices == 2:
                    options += binaryOptions
                choice = displayInteractiveMenu("calculadora de matrices", options)
                match choice:
                    case None:
                        state.isRunning = False
                    case 0 | 1 | 2 | 3 | 4:
                        state.currentMenu = "select_unary_target"
                        match choice:
                            case 0:
                                state.nextMenu = "register"
                            case 1:
                                state.nextMenu = "multiply_scalar"
                            case 2:
                                state.nextMenu = "invert"
                            case 3:
                                state.nextMenu = "transpose"
                            case 4:
                                state.nextMenu = "solve"
                    case 5:
                        state.currentMenu = "add"
                    case 6:
                        state.currentMenu = "subtract"
                    case 7:
                        state.currentMenu = "multiply_matrices"

            case "select_unary_target":
                options = ["Matriz A", "Matriz B"]
                choice = displayInteractiveMenu("seleccionar matriz", options)
                state.currentMenu = state.nextMenu
                match choice:
                    case None:
                        state.currentMenu = "main"
                    case 0:
                        state.activeTarget = "A"
                    case 1:
                        state.activeTarget = "B"
                state.nextMenu = None

            case "register":
                pass


if __name__ == "__main__":
    main()
