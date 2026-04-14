from dataclasses import dataclass
from sys import stdout
from msvcrt import getch


def overwriteConsole(message="\033[H\033[2J\033[3J"):
    stdout.write(message)
    stdout.flush()


def inputToAction(inp):
    pairs = {b"w": "up", b"s": "down", b"\r": "ENTER"}
    extendedPairs = {b"H": "up", b"P": "down"}
    if inp in pairs:
        inp = pairs[inp]
    elif inp in [b"\x00", b"\xe0"]:
        inp = getch()
        if inp in extendedPairs:
            inp = extendedPairs[inp]
    else:
        inp = inp.decode()
    return inp


options = [
    "Ingresar Matriz",
    "Multiplicar Matriz por Escalar",
    "Invertir Matriz",
    "Transponer Matriz",
    "Resolver Sistema de Ecuaciones Lineales",
    "Sumar Matrices",
    "Restar Matrices",
    "Multiplicar Matrices",
]

selected = 0

print("=== CALCULADORA DE MATRICES ===")

while True:
    overwriteConsole()
    for i, option in enumerate(options):
        print(option, "this" if i == selected else "")
    action = inputToAction(getch().lower())
    if action == "up" and selected > 0:
        selected -= 1
    elif action == "down" and selected < len(options) - 1:
        selected += 1
    elif action == "ENTER":
        pass
