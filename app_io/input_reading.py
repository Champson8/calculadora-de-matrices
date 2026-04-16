from time import sleep
from matrix import Matrix
from constants import HIDE_CURSOR, SHOW_CURSOR
from utils import clearConsole, printTitle, drawMatrix
from .input_validation import areValidDimensions, isValidFloat


def readManualMatrix(targetName: str):
    EXIT_CONTROLS = '\n* "exit" para salir'

    def clearAndShowTitle():
        clearConsole()
        printTitle(f"ingresar matriz {targetName}")

    isValidInput = False
    while not isValidInput:
        print(SHOW_CURSOR)
        clearAndShowTitle()

        rows = input("Número de filas: ")
        cols = input("Número de columnas: ")
        isValidInput = areValidDimensions(rows, cols)
        if not isValidInput:
            print("\nMatriz inválida. Intente de nuevo.")
            print(HIDE_CURSOR)
            sleep(3)

    clearAndShowTitle()

    numRows = int(rows)
    numCols = int(cols)
    matrixRows = [["  _  "] * numCols for _ in range(numRows)]
    for i in range(numRows):
        for j in range(numCols):
            matrixRows[i][j] = "[ _ ]"

            while True:
                print(SHOW_CURSOR)
                clearAndShowTitle()
                print(drawMatrix(matrixRows))
                value = input(EXIT_CONTROLS + f"\nValor de ({i+1}, {j+1}): ")
                if value.lower() == "exit":
                    return
                if isValidFloat(value):
                    matrixRows[i][j] = float(value)
                    break
                else:
                    print("\nValor inválido. Intente de nuevo.")
                    print(HIDE_CURSOR)
                    sleep(3)

    print(SHOW_CURSOR)
    clearAndShowTitle()

    matrix = Matrix(matrixRows)
    print(matrix)

    choice = input(EXIT_CONTROLS + " | ENTER para confirmar\n")
    print(HIDE_CURSOR)
    if choice == "exit":
        return
    else:
        return matrix


def readFileMatrix(targetName: str):
    clearConsole()
    printTitle(f"ingresar matriz {targetName}")
