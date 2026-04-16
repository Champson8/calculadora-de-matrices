from sys import stdout


def clearConsole():
    stdout.write("\033[H\033[2J\033[3J")
    stdout.flush()


def printTitle(title: str):
    print(f"=== {title.upper()} ===\n")


def drawMatrix(rows):
    formatValue = lambda value: value if isinstance(value, str) else f"{value:g}"
    columnStrWidths = [
        max(len(formatValue(x)) for x in column)
        for column in list(map(list, zip(*rows)))
    ]
    maxColWidth = max(columnStrWidths)
    rowToStr = lambda rowIdx: " ".join(
        map(lambda x: formatValue(x).rjust(maxColWidth), rows[rowIdx])
    )
    if len(rows) == 1:
        drawing = f"[ {rowToStr(0)} ]"
    else:
        drawing = [f"┌ {rowToStr(0)} ┐"]
        for i in range(1, len(rows) - 1):
            drawing.append(f"│ {rowToStr(i)} │")
        drawing.append(f"└ {rowToStr(len(rows) - 1)} ┘")
        drawing = "\n".join(drawing)
    return drawing
