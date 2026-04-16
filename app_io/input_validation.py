from matrix import Matrix


def areValidDimensions(numRows: str | int, numCols: str | int):
    try:
        numRows = int(numRows)
        numCols = int(numCols)
        _ = Matrix([[0] * numCols for _ in range(numRows)])
        return True
    except:
        return False


def isValidFloat(value: str | float | int):
    try:
        _ = float(value)
        return True
    except:
        return False
