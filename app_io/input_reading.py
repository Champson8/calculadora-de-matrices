from pathlib import Path
from time import sleep
from matrix import Matrix
from constants import HIDE_CURSOR, SHOW_CURSOR
from utils import clearConsole, printTitle, drawMatrix
from .input_validation import areDimensionsValid, isFloatValid


_EXIT_CONTROLS = '\n* "exit" para regresar'


def _clearAndShowTitle(targetName: str):
    clearConsole()
    printTitle(f"ingresar matriz {targetName}")


def _confirmMatrix(matrix: Matrix):
    print(matrix)
    choice = input(_EXIT_CONTROLS + " | ENTER para confirmar\n")
    print(HIDE_CURSOR)
    return choice


def _parseLinesToMatrix(lines: list[str]):
    if not lines:
        return None
    try:
        matrixRows = list(map(lambda line: line.replace("\n", "").split(), lines))
        matrixRows = [[float(x) for x in row] for row in matrixRows]
        matrix = Matrix(matrixRows)
        return matrix
    except:
        return None


def readManualMatrix(targetName: str):
    isValidInput = False
    while not isValidInput:
        print(SHOW_CURSOR)
        _clearAndShowTitle(targetName)

        rows = input("Número de filas: ")
        cols = input("Número de columnas: ")
        isValidInput = areDimensionsValid(rows, cols)
        if not isValidInput:
            print("\nMatriz inválida. Intente de nuevo.")
            print(HIDE_CURSOR)
            sleep(3)

    _clearAndShowTitle(targetName)

    numRows = int(rows)
    numCols = int(cols)
    matrixRows = [["  _  "] * numCols for _ in range(numRows)]
    for i in range(numRows):
        for j in range(numCols):
            matrixRows[i][j] = "[ _ ]"

            while True:
                print(SHOW_CURSOR)
                _clearAndShowTitle(targetName)
                print(drawMatrix(matrixRows))
                value = input(_EXIT_CONTROLS + f"\nValor de ({i+1}, {j+1}): ")
                if value.lower() == "exit":
                    return
                if isFloatValid(value):
                    matrixRows[i][j] = float(value)
                    break
                else:
                    print("\nValor inválido. Intente de nuevo.")
                    print(HIDE_CURSOR)
                    sleep(3)

    print(SHOW_CURSOR)
    _clearAndShowTitle(targetName)

    matrix = Matrix(matrixRows)
    choice = _confirmMatrix(matrix)

    if choice == "exit":
        return None
    else:
        return matrix


def readFileMatrix(targetName: str):
    clearConsole()
    printTitle(f"ingresar matriz {targetName}")
