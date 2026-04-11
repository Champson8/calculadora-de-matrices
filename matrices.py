from dataclasses import dataclass
from copy import deepcopy
from random import randint
from collections import Counter


@dataclass
class Matrix:
    values: list[list[int]]

    def __post_init__(self):
        self.numRows = len(self.values)
        self.numCols = len(self.values[0])

        if self.numRows == 1 and self.numCols == 1:
            raise ValueError("La matriz no debe ser un único número.")

        areColsSameSize = all(len(row) == self.numCols for row in self.values)
        hasEmptyCols = any(len(row) == 0 for row in self.values)

        if not areColsSameSize:
            raise ValueError(
                "La matriz debe tener el mismo número de columnas en cada fila."
            )
        if hasEmptyCols:
            raise ValueError("La matriz no debe tener columnas vacías.")

    @classmethod
    def identity(cls, size):
        values = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        return cls(values)

    @classmethod
    def sequential(cls, size):
        values = [[i * size + j for j in range(1, size + 1)] for i in range(size)]
        return cls(values)

    @classmethod
    def random(cls, size, maxValue=9):
        values = [
            [randint(-maxValue, maxValue) for _ in range(size)] for _ in range(size)
        ]
        return cls(values)

    @property
    def columns(self):
        return [
            [self.values[i][j] for i in range(self.numRows)]
            for j in range(self.numCols)
        ]

    @property
    def determinant(self):
        if self.numRows != self.numCols:
            raise ValueError("La matriz debe ser cuadrada para poseer determinante.")
        if self.numRows == 2:
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        else:
            isDetZero = any(
                v == [0] * self.numRows
                for v in self.values
                + list(self.columns[i] for i in range(self.numRows))
            )
            isDetZero = isDetZero or (
                len(Counter(map(tuple, self.values)))
                + len(Counter(map(tuple, self.columns)))
                != self.numRows * 2
            )
            if isDetZero:
                return 0
            if self.numRows == 3:
                return (
                    self[0, 0] * self[1, 1] * self[2, 2]
                    + self[0, 1] * self[1, 2] * self[2, 0]
                    + self[0, 2] * self[1, 0] * self[2, 1]
                    - self[0, 2] * self[1, 1] * self[2, 0]
                    - self[0, 1] * self[1, 0] * self[2, 2]
                    - self[0, 0] * self[1, 2] * self[2, 1]
                )

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx < 0 or idx >= self.numRows:
                raise IndexError("Índice fuera de rango.")
            return self.values[idx]
        elif isinstance(idx, tuple):
            if (
                idx[0] < 0
                or idx[0] >= self.numRows
                or idx[1] < 0
                or idx[1] >= self.numCols
            ):
                raise IndexError("Índice fuera de rango.")
            return self.values[idx[0]][idx[1]]
        else:
            raise TypeError('Índice debe ser de tipo "int" o "tuple".')

    def __setitem__(self, idx, value):
        if not isinstance(idx, tuple):
            raise TypeError('Índice debe ser de tipo "tuple".')
        if idx[0] < 0 or idx[0] >= self.numRows or idx[1] < 0 or idx[1] >= self.numCols:
            raise IndexError("Índice fuera de rango.")
        if isinstance(value, int | float):
            self.values[idx[0]][idx[1]] = value
        else:
            raise TypeError('El valor asignado debe ser de tipo "int" o "float".')

    def __add__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Las matrices sumadas deben ser del mismo tamaño.")
        newValues = [
            [self.values[i][j] + other.values[i][j] for j in range(self.numCols)]
            for i in range(self.numRows)
        ]
        return Matrix(newValues)

    def __sub__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Las matrices restadas deben ser del mismo tamaño.")
        return self + (other * -1)

    def __mul__(self, other):
        if isinstance(other, int | float):
            newValues = [
                [self.values[i][j] * other for j in range(self.numCols)]
                for i in range(self.numRows)
            ]
        elif isinstance(other, Matrix):
            if self.numCols != other.numRows:
                raise ValueError(
                    "Las matrices multiplicadas deben ser de tamaños m * n y n * p."
                )
            newValues = [
                [
                    sum(
                        [
                            self.values[i][k] * other.columns[j][k]
                            for k in range(self.numCols)
                        ]
                    )
                    for j in range(other.numCols)
                ]
                for i in range(self.numRows)
            ]
        return Matrix(newValues)

    def __pow__(self, value):
        if self.numRows != self.numCols:
            raise ValueError("La matriz debe ser de tamaño n * n.")
        if not isinstance(value, int):
            raise TypeError('La potencia debe ser de tipo "int".')
        if value == 0:
            newMatrix = Matrix.identity(self.numRows)
        elif value == -1:
            pass  # TODO: add .invert() method
        elif value < -1:
            raise ValueError(
                "La matriz debe ser elevada a una potencia mayor o igual que -1."
            )
        else:
            matrixCopy, newMatrix = deepcopy(self), deepcopy(self)
            for _ in range(value - 1):
                newMatrix *= matrixCopy
        return newMatrix

    def __str__(self):
        columnStrWidths = [
            max(len(str(x)) for x in self.columns[i]) for i in range(self.numRows)
        ]
        maxColWidth = (
            columnStrWidths[0] if len(columnStrWidths) == 1 else max(*columnStrWidths)
        )
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

    def transpose(self):
        newValues = [
            [self.values[j][i] for j in range(self.numCols)]
            for i in range(self.numRows)
        ]
        return Matrix(newValues)
