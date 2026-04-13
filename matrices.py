from dataclasses import dataclass
from random import randint
from collections import Counter
from math import isclose


@dataclass
class Matrix:
    rows: list[list[int]]

    def __post_init__(self):
        self.numRows = len(self.rows)

        if self.numRows == 0:
            raise ValueError("La matriz no puede estar vacía.")

        self.numCols = len(self.rows[0])

        if self.numRows == 1 and self.numCols == 1:
            raise ValueError("La matriz no puede ser un único número.")

        areColsSameSize = all(len(row) == self.numCols for row in self.rows)
        hasEmptyCols = any(len(row) == 0 for row in self.rows)

        if not areColsSameSize:
            raise ValueError(
                "La matriz debe tener el mismo número de columnas en cada fila."
            )
        if hasEmptyCols:
            raise ValueError("La matriz no puede tener columnas vacías.")

        self.rows = [list(row) for row in self.rows]

        self._cleanFloats_inPlace()

    @classmethod
    def identity(cls, size):
        rows = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        return cls(rows)

    @classmethod
    def zero(cls, numRows, numCols):
        rows = [[0 for _ in range(numCols)] for _ in range(numRows)]
        return cls(rows)

    @classmethod
    def sequential(cls, numRows, numCols):
        rows = [
            [i * numCols + j for j in range(1, numCols + 1)] for i in range(numRows)
        ]
        return cls(rows)

    @classmethod
    def random(cls, numRows, numCols, maxValue=9):
        rows = [
            [randint(-maxValue, maxValue) for _ in range(numCols)]
            for _ in range(numRows)
        ]
        return cls(rows)

    @property
    def columns(self):
        return [
            [self.rows[i][j] for i in range(self.numRows)] for j in range(self.numCols)
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
                for v in self.rows + list(self.columns[i] for i in range(self.numRows))
            )
            isDetZero = isDetZero or (
                len(Counter(map(tuple, self.rows)))
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
                ) - (
                    self[0, 2] * self[1, 1] * self[2, 0]
                    + self[0, 1] * self[1, 0] * self[2, 2]
                    + self[0, 0] * self[1, 2] * self[2, 1]
                )

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx < 0 or idx >= self.numRows:
                raise IndexError("Índice fuera de rango.")
            return self.rows[idx]
        elif isinstance(idx, tuple):
            if (
                idx[0] < 0
                or idx[0] >= self.numRows
                or idx[1] < 0
                or idx[1] >= self.numCols
            ):
                raise IndexError("Índice fuera de rango.")
            return self.rows[idx[0]][idx[1]]
        else:
            raise TypeError('Índice debe ser de tipo "int" o "tuple".')

    def __setitem__(self, idx, value):
        if not isinstance(idx, tuple):
            raise TypeError('Índice debe ser de tipo "tuple".')
        if idx[0] < 0 or idx[0] >= self.numRows or idx[1] < 0 or idx[1] >= self.numCols:
            raise IndexError("Índice fuera de rango.")
        if isinstance(value, int | float):
            self.rows[idx[0]][idx[1]] = value
        else:
            raise TypeError('El valor asignado debe ser de tipo "int" o "float".')

    def __add__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Las matrices sumadas deben ser del mismo tamaño.")
        newRows = [
            [self.rows[i][j] + other.rows[i][j] for j in range(self.numCols)]
            for i in range(self.numRows)
        ]
        return Matrix(newRows)

    def __sub__(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Las matrices restadas deben ser del mismo tamaño.")
        return self + (other * -1)

    def __mul__(self, other):
        if isinstance(other, int | float):
            newRows = [
                [self.rows[i][j] * other for j in range(self.numCols)]
                for i in range(self.numRows)
            ]
        elif isinstance(other, Matrix):
            if self.numCols != other.numRows:
                raise ValueError(
                    "Las matrices multiplicadas deben ser de tamaños m * n y n * p."
                )
            newRows = [
                [
                    sum(
                        [
                            self.rows[i][k] * other.columns[j][k]
                            for k in range(self.numCols)
                        ]
                    )
                    for j in range(other.numCols)
                ]
                for i in range(self.numRows)
            ]
        return Matrix(newRows)

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
            matrixCopy, newMatrix = Matrix(self.rows), Matrix(self.rows)
            for _ in range(value - 1):
                newMatrix *= matrixCopy
        return newMatrix

    def __str__(self):
        columnStrWidths = [max(len(str(x)) for x in column) for column in self.columns]
        maxColWidth = (
            columnStrWidths[0] if len(columnStrWidths) == 1 else max(*columnStrWidths)
        )
        rowToStr = lambda rowIdx: " ".join(
            map(lambda x: str(x).rjust(maxColWidth), self.rows[rowIdx])
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

    def _cleanFloats_inPlace(self):
        for i in range(self.numRows):
            for j in range(self.numCols):
                value = self[i, j]
                if isinstance(value, float):
                    nearestInt = round(value)
                    if isclose(value, nearestInt):
                        self[i, j] = nearestInt
        return self

    def round(self, decimals=3):
        newRows = [
            [round(self[i, j], decimals) for j in range(self.numCols)]
            for i in range(self.numRows)
        ]
        return Matrix(newRows)

    def swapRows(self, idx1, idx2):
        newMatrix = Matrix(self.rows)
        for j in range(self.numCols):
            newMatrix[idx1, j], newMatrix[idx2, j] = (
                newMatrix[idx2, j],
                newMatrix[idx1, j],
            )
        return newMatrix

    def swapColumns(self, idx1, idx2):
        newMatrix = Matrix(self.rows)
        col1, col2 = self.columns[idx1], self.columns[idx2]
        for i in range(self.numRows):
            newMatrix[i, idx1], newMatrix[i, idx2] = col2[i], col1[i]
        return newMatrix

    def transpose(self):
        return Matrix(self.columns)

    def lupDecompose(self):
        lower = Matrix.identity(self.numRows)
        upper = Matrix(self.rows)
        perm = Matrix.identity(self.numRows)

        numPivots = min(self.numRows, self.numCols)

        detFactor = 1

        for k in range(numPivots):
            currColumnAbs = list(map(abs, upper.columns[k][k:]))
            maxValue = max(currColumnAbs)
            pivotRow = currColumnAbs.index(maxValue) + k

            if isclose(maxValue, 0):
                continue

            if pivotRow != k:
                detFactor *= -1
                upper = upper.swapRows(k, pivotRow)
                perm = perm.swapRows(k, pivotRow)
                for j in range(k):
                    lower[k, j], lower[pivotRow, j] = lower[pivotRow, j], lower[k, j]

            for i in range(k + 1, self.numRows):
                factor = upper[i, k] / upper[k, k]
                lower[i, k] = factor
                for j in range(k, self.numCols):
                    upper[i, j] -= upper[k, j] * factor

        return (
            perm,
            lower._cleanFloats_inPlace(),
            upper._cleanFloats_inPlace(),
            detFactor,
        )
