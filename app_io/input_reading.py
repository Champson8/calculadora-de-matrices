from pathlib import Path
from time import sleep
from matrix import Matrix
from constants import HIDE_CURSOR, SHOW_CURSOR
from utils import getUserAction, clearConsole, printTitle, drawMatrix
from .input_validation import areDimensionsValid, isFloatValid


def _clearAndShowTitle(title: str):
    clearConsole()
    printTitle(title)


def _confirmMatrix(matrix: Matrix):
    print(
        matrix, "\n* ENTER para confirmar | ESC para regresar\n", HIDE_CURSOR, sep="\n"
    )
    return getUserAction()


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


def readManualMatrix(title: str):
    EXIT_CONTROLS = '\n* "exit" para regresar'

    isValidInput = False
    while not isValidInput:
        print(SHOW_CURSOR)
        _clearAndShowTitle(title)

        rows = input("Número de filas: ")
        cols = input("Número de columnas: ")
        isValidInput = areDimensionsValid(rows, cols)
        if not isValidInput:
            print("\nMatriz inválida. Intente de nuevo.")
            print(HIDE_CURSOR)
            sleep(3)

    _clearAndShowTitle(title)

    numRows = int(rows)
    numCols = int(cols)
    matrixRows = [["  _  "] * numCols for _ in range(numRows)]
    for i in range(numRows):
        for j in range(numCols):
            matrixRows[i][j] = "[ _ ]"

            while True:
                print(SHOW_CURSOR)
                _clearAndShowTitle(title)
                print(drawMatrix(matrixRows))
                value = input(EXIT_CONTROLS + f"\nValor de ({i+1}, {j+1}): ")
                if value.lower() == "exit":
                    print(HIDE_CURSOR)
                    return
                if isFloatValid(value):
                    matrixRows[i][j] = float(value)
                    break
                else:
                    print("\nValor inválido. Intente de nuevo.")
                    print(HIDE_CURSOR)
                    sleep(3)

    print(SHOW_CURSOR)
    _clearAndShowTitle(title)

    matrix = Matrix(matrixRows)
    action = _confirmMatrix(matrix)

    if action == "ESCAPE":
        return None
    elif action == "ENTER":
        return matrix


def readFileMatrix(title: str):
    print(SHOW_CURSOR)
    _clearAndShowTitle(title)

    file = Path(__file__).parent / ".." / "resources" / "matrices" / "matrix.txt"
    matrix = None

    if file.is_file():
        with open(file.resolve()) as readFile:
            matrix = _parseLinesToMatrix(readFile.readlines())

    if matrix is not None:
        action = _confirmMatrix(matrix)
        if action == "ESCAPE":
            return None
        elif action == "ENTER":
            return matrix
    else:
        print("Matriz inválida. Compruebe el archivo.")
        print(HIDE_CURSOR)
        sleep(3)
        return None


def readScalar(title: str):
    while True:
        print(SHOW_CURSOR)
        _clearAndShowTitle(title)
        value = input("Escalar: ")
        if isFloatValid(value):
            return float(value)
        else:
            print("\nEscalar inválido. Intente de nuevo.")
            print(HIDE_CURSOR)
            sleep(3)
