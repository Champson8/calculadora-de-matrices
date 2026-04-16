from matrix import Matrix


def areDimensionsValid(numRows: str | int, numCols: str | int):
    try:
        numRows = int(numRows)
        numCols = int(numCols)
        _ = Matrix([[0] * numCols for _ in range(numRows)])
        return True
    except:
        return False


def isFloatValid(value: str | float | int):
    try:
        _ = float(value)
        return True
    except:
        return False
