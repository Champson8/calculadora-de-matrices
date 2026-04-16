from dataclasses import dataclass
from msvcrt import getch
from matrix import Matrix
from utils import clearConsole, printTitle
from app_io.input_reading import readManualMatrix, readFileMatrix
from constants import CONTROLS, HIDE_CURSOR


@dataclass
class App:
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
    app = App()
    print(HIDE_CURSOR)
    while app.isRunning:
        clearConsole()

        match app.currentMenu:

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
                if app.numMatrices >= 1:
                    options += unaryOptions
                if app.numMatrices == 2:
                    options += binaryOptions
                choice = displayInteractiveMenu("calculadora de matrices", options)
                match choice:
                    case None:
                        app.isRunning = False
                    case 0 | 1 | 2 | 3 | 4:
                        app.currentMenu = "select_unary_target"
                        match choice:
                            case 0:
                                app.nextMenu = "register"
                            case 1:
                                app.nextMenu = "multiply_scalar"
                            case 2:
                                app.nextMenu = "invert"
                            case 3:
                                app.nextMenu = "transpose"
                            case 4:
                                app.nextMenu = "solve"
                    case 5:
                        app.currentMenu = "add"
                    case 6:
                        app.currentMenu = "subtract"
                    case 7:
                        app.currentMenu = "multiply_matrices"

            case "select_unary_target":
                options = ["Matriz A", "Matriz B"]
                choice = displayInteractiveMenu("seleccionar matriz", options)
                app.currentMenu = app.nextMenu
                match choice:
                    case None:
                        app.currentMenu = "main"
                    case 0:
                        app.activeTarget = "A"
                    case 1:
                        app.activeTarget = "B"
                app.nextMenu = None

            case "register":
                options = ["Ingresar Manualmente", "Leer Archivo (matrix.txt)"]
                choice = displayInteractiveMenu("método de lectura de matriz", options)
                match choice:
                    case None:
                        app.currentMenu = "main"
                    case 0:
                        matrix = readManualMatrix(app.activeTarget)
                        if matrix is not None:
                            if app.activeTarget == "A":
                                app.matrixA = matrix
                            else:
                                app.matrixB = matrix
                    case 1:
                        matrix = readFileMatrix(app.activeTarget)
                app.currentMenu = "main"


if __name__ == "__main__":
    main()
