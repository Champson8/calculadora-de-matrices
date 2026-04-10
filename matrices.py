from dataclasses import dataclass
from copy import deepcopy


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

    def __getitem__(self, idx):
        if idx < 0 or idx >= self.numRows:
            raise IndexError("Índice fuera de rango.")
        return self.values[idx]

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
                            self.values[i][k] * other.getColumn(j)[k]
                            for k in range(self.numCols)
                        ]
                    )
                    for j in range(other.numCols)
                ]
                for i in range(self.numRows)
            ]
        return Matrix(newValues)

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError('La potencia debe ser de tipo "int".')
        matrixCopy, newMatrix = deepcopy(self), deepcopy(self)
        for _ in range(other - 1):
            newMatrix *= matrixCopy
        return newMatrix

    def __str__(self):
        columnStrWidths = [
            max(len(str(x)) for x in self.getColumn(i)) for i in range(self.numRows)
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

    def getColumn(self, idx):
        if idx < 0 or idx >= self.numCols:
            raise IndexError("Índice fuera de rango.")
        return [self.values[i][idx] for i in range(self.numRows)]

    def transpose(self):
        newValues = [
            [self.values[j][i] for j in range(self.numCols)]
            for i in range(self.numRows)
        ]
        return Matrix(newValues)


a = Matrix.identity(5)
b = Matrix.sequential(4)
print(a)
print(b)
