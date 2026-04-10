from dataclasses import dataclass


@dataclass
class Matrix:
    values: list[list[int]]

    def __post_init__(self):
        self.numRows = len(self.values)
        self.numCols = len(self.values[0])
        colsAreSameSize = all(len(row) == self.numCols for row in self.values)
        hasEmptyCols = any(len(row) == 0 for row in self.values)

        if not colsAreSameSize:
            raise ValueError(
                "La matriz debe tener el mismo número de columnas en cada fila."
            )
        if hasEmptyCols:
            raise ValueError("La matriz no debe tener columnas vacías.")

    def __getitem__(self, idx):
        if idx < 0 or idx >= self.numRows:
            raise IndexError("Índice fuera de rango.")
        return self.values[idx]

    def __setitem__(self, idx, value):
        if not isinstance(idx, tuple):
            raise TypeError('Índice debe de ser de tipo "tuple".')
        if idx[0] < 0 or idx[0] >= self.numRows or idx[1] < 0 or idx[1] >= self.numCols:
            raise IndexError("Índice fuera de rango.")
        if isinstance(value, int | float):
            self.values[idx[0]][idx[1]] = value
        else:
            raise TypeError('El valor asignado debe ser de tipo "int" o "float".')

    def __str__(self):
        columnStrWidths = [
            max(len(str(x)) for x in self.getColumn(i)) for i in range(self.numRows)
        ]
        maxColWidth = max(*columnStrWidths)
        rowToStr = lambda rowIdx: " ".join(
            map(lambda x: str(x).rjust(maxColWidth), self.values[rowIdx])
        )
        if self.numRows == 1:
            drawing = f"[ {rowToStr(0)} ]"
        else:
            drawing = [f"┌ {rowToStr(0)} ┐"]
            for i in range(1, self.numRows - 1):
                drawing.append(f"│ {rowToStr(i)} │")
            drawing.append(f"└ {rowToStr(self.numRows - 1)} ┘")
            drawing = "\n".join(drawing)
        return drawing

    def getColumn(self, idx):
        if idx < 0 or idx >= self.numCols:
            raise IndexError("Índice fuera de rango.")
        return [self.values[i][idx] for i in range(self.numRows)]
