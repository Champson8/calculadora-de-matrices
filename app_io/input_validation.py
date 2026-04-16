from matrix import Matrix


def isValidDimensions(numRows: str | int, numCols: str | int):
    try:
        numRows = int(numRows)
        numCols = int(numCols)
        _ = Matrix([[0] * numCols for _ in range(numRows)])
        return True
    except:
        return False
