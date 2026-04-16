from pathlib import Path
from time import sleep
from matrix import Matrix
from constants import HIDE_CURSOR, SHOW_CURSOR, EXIT_CONTROLS
from utils import clearConsole, printTitle, getUserAction


def _showError(message: str):
    print(message)
    print(HIDE_CURSOR)
    sleep(3)


def writeMatrixToFile(matrix: Matrix):
    isPathValid = False
    while not isPathValid:
        print(SHOW_CURSOR)
        clearConsole()
        printTitle("guardar matriz")

        print(EXIT_CONTROLS)
        path = Path(input("Directorio del archivo .txt: ")).resolve()

        if path == "exit":
            print(HIDE_CURSOR)
            return None
        elif path.exists():
            while True:
                print(f"\n{path.name} ya existe.")
                print("* ENTER para sobreescribir | ESC para regresar", HIDE_CURSOR)
                action = getUserAction()
                if action == "ESCAPE":
                    return None
                elif action == "ENTER":
                    break

        print(HIDE_CURSOR, end="\n")

        try:
            if path.suffix != ".txt":
                raise ValueError('La extensión del archivo debe ser ".txt".')
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as error:
            _showError(f"No se pudo crear el archivo: {error}")
            return None

        try:
            lines = list(map(lambda row: " ".join(map(str, row)) + "\n", matrix.rows))
            with open(path, "w", encoding="utf-8") as file:
                file.writelines(lines)
            return path
        except PermissionError:
            _showError(
                "No se tiene permisos suficientes para guardar en este directorio."
            )
            return None
        except Exception as error:
            _showError(f"No se pudo crear el archivo: {error}")
