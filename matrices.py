from dataclasses import dataclass
from functools import cached_property
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

    @cached_property
    def _lup(self):
        return self.lupDecompose()

    @property
    def columns(self):
        return list(map(list, zip(*self.rows)))

    @property
    def isSquare(self):
        return self.numRows == self.numCols

    @property
    def isTriangular(self):
        if not self.isSquare:
            return False
        upperTriangle = [self.rows[i][i + 1 :] for i in range(self.numRows)]
        lowerTriangle = [self.rows[i][: i - self.numRows] for i in range(self.numRows)]
        return all(not any(row) for row in upperTriangle) or all(
            not any(row) for row in lowerTriangle
        )

    @property
    def determinant(self):
        if not self.isSquare:
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
            elif self.numRows == 3:
                return (
                    self[0, 0] * self[1, 1] * self[2, 2]
                    + self[0, 1] * self[1, 2] * self[2, 0]
                    + self[0, 2] * self[1, 0] * self[2, 1]
                ) - (
                    self[0, 2] * self[1, 1] * self[2, 0]
                    + self[0, 1] * self[1, 0] * self[2, 2]
                    + self[0, 0] * self[1, 2] * self[2, 1]
                )
            else:
                if self.isTriangular:
                    det = 1
                    triangleMatrix = self
                else:
                    _, _, U, det = self._lup
                    triangleMatrix = U
                for i in range(self.numRows):
                    det *= triangleMatrix[i, i]
                if isinstance(det, float) and isclose(det, round(det)):
                    det = int(round(det))
                return det

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
        if not self.isSquare:
            raise ValueError("La matriz debe ser de tamaño n * n.")
        if not isinstance(value, int):
            raise TypeError('La potencia debe ser de tipo "int".')
        if value == 0:
            newMatrix = Matrix.identity(self.numRows)
        elif value == -1:
            newMatrix = self.invert()
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
        columnStrWidths = [
            max(len(f"{x:g}") for x in column) for column in self.columns
        ]
        maxColWidth = (
            columnStrWidths[0] if len(columnStrWidths) == 1 else max(*columnStrWidths)
        )
        rowToStr = lambda rowIdx: " ".join(
            map(lambda x: f"{x:g}".rjust(maxColWidth), self.rows[rowIdx])
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
                    if isclose(value, nearestInt, abs_tol=1e-12):
                        self[i, j] = nearestInt
        return self

    def _solveWithLUP(self, L, U, P, b):
        infSolutions = noSolutions = False
        x = P * b

        for i in range(self.numRows - 1):
            for k in range(i + 1, self.numRows):
                if L[k, i] != 0:
                    factor = L[k, i] / L[i, i]
                    L = L.addRows(i, k, -factor)
                    x = x.addRows(i, k, -factor)

        for i in range(self.numRows):
            infSolutions = noSolutions = False
            if U[i, i] == 0:
                if x[i, 0] == 0:
                    infSolutions = True
                else:
                    noSolutions = True
                break

        if infSolutions:
            raise ValueError("La matriz tiene infinitas soluciones.")
        elif noSolutions:
            raise ValueError("La matriz no tiene soluciones.")

        for i in range(self.numRows - 1, 0, -1):
            for k in range(i - 1, -1, -1):
                if U[k, i] != 0:
                    factor = U[k, i] / U[i, i]
                    U = U.addRows(i, k, -factor)
                    x = x.addRows(i, k, -factor)
        for i in range(self.numRows):
            x[i, 0] /= U[i, i]

        return x._cleanFloats_inPlace()

    def swapRows(self, idx1, idx2):
        if any(idx < 0 or idx >= self.numRows for idx in [idx1, idx2]):
            raise IndexError("Índice fuera de rango.")
        newMatrix = Matrix(self.rows)
        for j in range(self.numCols):
            newMatrix[idx1, j], newMatrix[idx2, j] = (
                newMatrix[idx2, j],
                newMatrix[idx1, j],
            )
        return newMatrix

    def addRows(self, idx1, idx2, scalar=1):
        if any(idx < 0 or idx >= self.numRows for idx in [idx1, idx2]):
            raise IndexError("Índice fuera de rango.")
        newMatrix = Matrix(self.rows)
        scaledRow = list(map(lambda x: x * scalar, newMatrix.rows[idx1]))
        for j in range(self.numCols):
            newMatrix[idx2, j] += scaledRow[j]
        return newMatrix

    def invert(self):
        if self.determinant == 0:
            raise ValueError("La matriz no es invertible.")

        P, L, U, _ = self._lup
        inverse = Matrix.zero(self.numRows, self.numCols)

        for j in range(self.numCols):
            identityVector = Matrix([[1 if i == j else 0] for i in range(self.numRows)])
            x = self._solveWithLUP(L, U, P, identityVector)
            for i in range(self.numRows):
                inverse[i, j] = x[i, 0]

        return inverse._cleanFloats_inPlace()

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

            if isclose(maxValue, 0, abs_tol=1e-12):
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
                upper = upper.addRows(k, i, -factor)

        return (
            perm,
            lower._cleanFloats_inPlace(),
            upper._cleanFloats_inPlace(),
            detFactor,
        )

    def solve(self, b):
        P, L, U, _ = self._lup
        x = self._solveWithLUP(L, U, P, b)
        return x
