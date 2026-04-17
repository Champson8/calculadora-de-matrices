from pathlib import Path
from time import sleep
from matrix import Matrix
from constants import HIDE_CURSOR, SHOW_CURSOR, EXIT_CONTROLS
from utils import getUserAction, clearConsole, printTitle, drawMatrix, showError
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


def readManualMatrix(title: str, numRows: int = None, numCols: int = None):
    isInputValid = numRows and numCols
    while not isInputValid:
        print(SHOW_CURSOR)
        _clearAndShowTitle(title)

        rows = input("Número de filas: ")
        cols = input("Número de columnas: ")
        isInputValid = areDimensionsValid(rows, cols)
        if not isInputValid:
            showError("\nMatriz inválida. Intente de nuevo.")

    _clearAndShowTitle(title)

    numRows = numRows or int(rows)
    numCols = numCols or int(cols)
    matrixRows = [["  _  "] * numCols for _ in range(numRows)]
    for i in range(numRows):
        for j in range(numCols):
            matrixRows[i][j] = "[ _ ]"

            while True:
                print(SHOW_CURSOR)
                _clearAndShowTitle(title)
                print(drawMatrix(matrixRows), "\n" + EXIT_CONTROLS, sep="\n")
                value = input(f"Valor de ({i+1}, {j+1}): ")
                if value.lower() == "exit":
                    print(HIDE_CURSOR)
                    return None
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
    else:
        showError("Archivo no encontrado. Compruebe el directorio.")
        return None

    if matrix is not None:
        action = _confirmMatrix(matrix)
        if action == "ESCAPE":
            return None
        elif action == "ENTER":
            return matrix
    else:
        showError("Matriz inválida. Compruebe el archivo.")
        return None


def readScalar(title: str):
    while True:
        print(SHOW_CURSOR)
        _clearAndShowTitle(title)
        value = input("Escalar: ")
        if isFloatValid(value):
            return float(value)
        else:
            showError("\nEscalar inválido. Intente de nuevo.")
