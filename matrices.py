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
