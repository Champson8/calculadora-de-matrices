from sys import stdout


def clearConsole():
    stdout.write("\033[H\033[2J\033[3J")
    stdout.flush()


def printTitle(title: str):
    print(f"=== {title.upper()} ===\n")
