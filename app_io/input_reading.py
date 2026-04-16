from time import sleep
from constants import HIDE_CURSOR, SHOW_CURSOR
from utils import clearConsole, printTitle
from .input_validation import isValidDimensions


def readManualMatrix(targetName: str):
    def clearAndShowTitle():
        clearConsole()
        printTitle(f"ingresar matriz {targetName}")

    isValidInput = False
    while not isValidInput:
        print(SHOW_CURSOR)
        clearAndShowTitle()

        rows = input("Número de filas: ")
        cols = input("Número de columnas: ")
        isValidInput = isValidDimensions(rows, cols)
        if not isValidInput:
            print("\nMatriz inválida. Intente de nuevo.")
            print(HIDE_CURSOR)
        sleep(3)

    clearAndShowTitle()


def readFileMatrix(targetName: str):
    clearConsole()
    printTitle(f"ingresar matriz {targetName}")
