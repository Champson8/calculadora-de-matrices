from dataclasses import dataclass
from matrix import Matrix
from utils import getUserAction, clearConsole, printTitle
from app_io.input_reading import readManualMatrix, readFileMatrix, readScalar
from constants import CONTROLS, HIDE_CURSOR, SHOW_CURSOR


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


def drawMatrixInMenu(app, targetName: str):
    matrix = {"A": app.matrixA, "B": app.matrixB}[targetName]
    return f"Matriz {targetName}:\n{str(matrix) if matrix is not None else '[]'}\n"


def main():
    app = App()
    print(HIDE_CURSOR)
    while app.isRunning:
        clearConsole()

        match app.currentMenu:

            case "main":
                options = ["Ingresar Matriz", "Ver Matrices"]
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
                    case 1:
                        app.currentMenu = "check_matrices"
                    case 0 | 2 | 3 | 4 | 5:
                        app.currentMenu = "select_unary_target"
                        match choice:
                            case 0:
                                app.nextMenu = "register"
                            case 2:
                                app.nextMenu = "multiply_scalar"
                            case 3:
                                app.nextMenu = "invert"
                            case 4:
                                app.nextMenu = "transpose"
                            case 5:
                                app.nextMenu = "solve"
                    case 6:
                        app.currentMenu = "add"
                    case 7:
                        app.currentMenu = "subtract"
                    case 8:
                        app.currentMenu = "multiply_matrices"

            case "select_unary_target":
                if app.numMatrices == 2 or app.nextMenu == "register":
                    options = ["Matriz A", "Matriz B"]
                    choice = displayInteractiveMenu("seleccionar matriz", options)
                    if choice is None:
                        app.currentMenu = "main"
                        continue
                    else:
                        choice = {0: "A", 1: "B"}[choice]
                elif app.numMatrices == 1:
                    choice = "A" if app.matrixA is not None else "B"
                app.activeTarget = choice
                app.currentMenu = app.nextMenu
                app.nextMenu = None

            case "register":
                options = ["Ingresar Manualmente", "Leer Archivo (matrix.txt)"]
                choice = displayInteractiveMenu("método de lectura de matriz", options)
                if choice == None:
                    app.currentMenu = "main"
                else:
                    matrix = (
                        readManualMatrix(app.activeTarget)
                        if choice == 0
                        else readFileMatrix(app.activeTarget)
                    )
                    if matrix is not None:
                        if app.activeTarget == "A":
                            app.matrixA = matrix
                        else:
                            app.matrixB = matrix
                app.currentMenu = "main"

            case "check_matrices":
                printTitle("matrices")
                drawing = f"{drawMatrixInMenu(app, 'A')}\n{drawMatrixInMenu(app, 'B')}"
                print(drawing, "* ENTER/ESC para regresar", sep="\n")
                if getUserAction() in ["ENTER", "ESCAPE"]:
                    app.currentMenu = "main"

            case "multiply_scalar":
                pass

            case "invert":
                pass

            case "transpose":
                pass

            case "solve":
                pass

            case "add":
                pass

            case "subtract":
                pass

            case "multiply_matrices":
                pass
    print(SHOW_CURSOR)


if __name__ == "__main__":
    main()
